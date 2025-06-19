from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from ..extensions import db
from ..models.portfolio import Portfolio, PortfolioStock, StockTip
from ..models.stock import Watchlist, WatchlistStock
from ..services.data_service import DataService
from ..services.analysis_service import AnalysisService
from ..services.ai_service import AIService
from datetime import datetime, timedelta

portfolio = Blueprint('portfolio', __name__)

@portfolio.route('/')
@login_required
def index():
    """Show user's portfolio"""
    try:
        # For ikke-innloggede brukere, vis en demo-portefølje
        if not current_user.is_authenticated:
            return render_template('portfolio/login_required.html')
            
        # Hent brukerens portefølje
        user_portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
        
        if not user_portfolio:
            # Opprett en ny portefølje hvis brukeren ikke har en
            user_portfolio = Portfolio(user_id=current_user.id, name="Min portefølje")
            db.session.add(user_portfolio)
            db.session.commit()
            
        # Hent aksjer i porteføljen
        portfolio_stocks = PortfolioStock.query.filter_by(portfolio_id=user_portfolio.id).all()
        
        # Hent gjeldende markedsdata for aksjene
        stocks_data = {}
        for ps in portfolio_stocks:
            stock_data = DataService.get_single_stock_data(ps.ticker)
            if stock_data:
                stocks_data[ps.ticker] = stock_data
                stocks_data[ps.ticker]['quantity'] = ps.quantity
                stocks_data[ps.ticker]['purchase_price'] = ps.purchase_price
                # Beregn gevinst/tap
                if 'last_price' in stock_data and stock_data['last_price'] != 'N/A':
                    current_value = float(stock_data['last_price']) * ps.quantity
                    purchase_value = ps.purchase_price * ps.quantity
                    stocks_data[ps.ticker]['profit_loss'] = current_value - purchase_value
                    stocks_data[ps.ticker]['profit_loss_percent'] = ((current_value / purchase_value) - 1) * 100 if purchase_value > 0 else 0
                
        # Beregn porteføljens totalverdi
        total_value = sum(float(data['last_price']) * data['quantity'] 
                           for ticker, data in stocks_data.items() 
                           if data['last_price'] != 'N/A')
        
        return render_template(
            'portfolio/index.html',
            portfolio=user_portfolio,
            stocks=stocks_data,
            total_value=total_value
        )
    except Exception as e:
        print(f"Error in portfolio index: {str(e)}")
        return render_template('error.html', error=f"Det oppstod en feil: {str(e)}")

@portfolio.route('/create', methods=['GET', 'POST'])
@login_required
def create_portfolio():
    """Create a new portfolio"""
    if request.method == 'POST':
        name = request.form.get('name')
        portfolio = Portfolio(name=name, user_id=current_user.id)
        db.session.add(portfolio)
        db.session.commit()
        flash('Portefølje opprettet!', 'success')
        return redirect(url_for('portfolio.index'))
    return render_template('portfolio/create.html')

@portfolio.route('/view/<int:id>')
def view_portfolio(id):
    """View a specific portfolio"""
    portfolio = Portfolio.query.get_or_404(id)

    # Fjern eierskapssjekk for å la alle se
    stocks_data = []
    total_value = 0
    total_investment = 0

    for stock in portfolio.stocks:
        current_data = DataService.get_stock_data(stock.ticker, period='1d')
        if not current_data.empty:
            current_price = current_data['Close'].iloc[-1]
            value = current_price * stock.quantity
            investment = stock.purchase_price * stock.quantity
            gain_loss = (current_price - stock.purchase_price) * stock.quantity
            gain_loss_percent = ((current_price / stock.purchase_price) - 1) * 100 if stock.purchase_price > 0 else 0

            stocks_data.append({
                'ticker': stock.ticker,
                'quantity': stock.quantity,
                'purchase_price': stock.purchase_price,
                'current_price': current_price,
                'value': value,
                'investment': investment,
                'gain_loss': gain_loss,
                'gain_loss_percent': gain_loss_percent
            })

            total_value += value
            total_investment += investment

    total_gain_loss = total_value - total_investment
    total_gain_loss_percent = ((total_value / total_investment) - 1) * 100 if total_investment > 0 else 0

    tickers = [stock.ticker for stock in portfolio.stocks]
    ai_recommendation = AIService.get_ai_portfolio_recommendation(tickers) if tickers else None

    return render_template('portfolio/view.html',
                           portfolio=portfolio,
                           stocks=stocks_data,
                           total_value=total_value,
                           total_investment=total_investment,
                           total_gain_loss=total_gain_loss,
                           total_gain_loss_percent=total_gain_loss_percent,
                           ai_recommendation=ai_recommendation)

@portfolio.route('/portfolio/<int:id>/add', methods=['GET', 'POST'])
@login_required
def add_stock_to_portfolio(id):
    """Add a stock to a specific portfolio"""
    portfolio = Portfolio.query.get_or_404(id)

    # Sjekk eierskap
    if portfolio.user_id != current_user.id:
        flash('Du har ikke tilgang til denne porteføljen', 'danger')
        return redirect(url_for('portfolio.index'))

    if request.method == 'POST':
        ticker = request.form.get('ticker')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        if not ticker or not quantity or not price:
            flash('Alle felt er påkrevd', 'danger')
            return redirect(url_for('portfolio.add_stock_to_portfolio', id=id))

        try: 
            quantity = float(quantity)
            price = float(price)
        except ValueError:
            flash('Antall og pris må være tall', 'danger')
            return redirect(url_for('portfolio.add_stock_to_portfolio', id=id))

        existing_stock = PortfolioStock.query.filter_by(portfolio_id=id, ticker=ticker).first()

        if existing_stock:
            total_value = (existing_stock.quantity * existing_stock.purchase_price) + (quantity * price)
            total_quantity = existing_stock.quantity + quantity
            existing_stock.purchase_price = total_value / total_quantity if total_quantity > 0 else 0
            existing_stock.quantity = total_quantity
        else:
            stock = PortfolioStock(
                portfolio_id=id,
                ticker=ticker,
                quantity=quantity,
                purchase_price=price
            )
            db.session.add(stock)
 
        db.session.commit()
        flash('Aksje lagt til i porteføljen', 'success')
        return redirect(url_for('portfolio.view_portfolio', id=id))

    return render_template('portfolio/add_stock_to_portfolio.html', portfolio=portfolio)

@portfolio.route('/portfolio/<int:id>/remove/<int:stock_id>', methods=['POST'])
@login_required
def remove_stock_from_portfolio(id, stock_id):
    """Remove a stock from a specific portfolio"""
    portfolio = Portfolio.query.get_or_404(id)

    # Sjekk eierskap
    if portfolio.user_id != current_user.id:
        flash('Du har ikke tilgang til denne porteføljen', 'danger')
        return redirect(url_for('portfolio.index'))

    stock = PortfolioStock.query.get_or_404(stock_id)

    if stock.portfolio_id != id:
        flash('Aksjen tilhører ikke denne porteføljen', 'danger')
        return redirect(url_for('portfolio.view_portfolio', id=id))

    db.session.delete(stock)
    db.session.commit()

    flash('Aksje fjernet fra porteføljen', 'success')
    return redirect(url_for('portfolio.view_portfolio', id=id))

@portfolio.route('/watchlist')
@login_required
def watchlist():
    """Show user's watchlist"""
    watchlist = Watchlist.query.filter_by(user_id=current_user.id).first()
    stocks = []
    if watchlist:
        for ws in watchlist.stocks:
            # Hent sanntidsdata for aksjen
            stock_data = DataService.get_stock_data(ws.ticker, period='2d')
            last_price = None
            change_percent = None
            if not stock_data.empty and len(stock_data) > 1:
                last_price = stock_data['Close'].iloc[-1]
                prev_price = stock_data['Close'].iloc[-2]
                change_percent = ((last_price - prev_price) / prev_price) * 100 if prev_price else None
            # Hent navn fra info
            info = DataService.get_stock_info(ws.ticker)
            name = info.get('longName', ws.ticker)
            stocks.append({
                'ticker': ws.ticker,
                'name': name,
                'last_price': last_price,
                'change_percent': change_percent
            })
    return render_template('portfolio/watchlist.html', stocks=stocks)

@portfolio.route('/watchlist/create', methods=['GET', 'POST'])
@login_required
def create_watchlist():
    """Create a new watchlist"""
    if request.method == 'POST':
        name = request.form.get('name')
        user_id = current_user.id
        watchlist = Watchlist(name=name, user_id=user_id)
        db.session.add(watchlist)
        db.session.commit()
        flash('Favorittliste opprettet!', 'success')
        return redirect(url_for('portfolio.watchlist'))
    return render_template('portfolio/create_watchlist.html')

@portfolio.route('/watchlist/<int:id>/add', methods=['GET', 'POST'])
@login_required
def add_to_watchlist(id):
    """Add a stock to a watchlist"""
    watchlist = Watchlist.query.get_or_404(id)

    # Sjekk eierskap
    if watchlist.user_id != current_user.id:
        flash('Du har ikke tilgang til denne favorittlisten', 'danger')
        return redirect(url_for('portfolio.watchlist'))

    if request.method == 'POST':
        ticker = request.form.get('ticker')

        if not ticker:
            flash('Ticker er påkrevd', 'danger')
            return redirect(url_for('portfolio.add_to_watchlist', id=id))

        existing = WatchlistStock.query.filter_by(watchlist_id=id, ticker=ticker).first()

        if existing:
            flash('Aksjen er allerede i favorittlisten', 'warning')
        else:
            stock = WatchlistStock(watchlist_id=id, ticker=ticker)
            db.session.add(stock)
            db.session.commit()
            flash('Aksje lagt til i favorittlisten', 'success')

        return redirect(url_for('portfolio.watchlist'))

    return render_template('portfolio/add_to_watchlist.html', watchlist=watchlist)

@portfolio.route('/tips')
def stock_tips():
    """Show stock tips for the user"""
    try:
        # Get stock tips
        all_tips = StockTip.query.order_by(StockTip.created_at.desc()).limit(10).all()
        
        # If there are no tips, create some demo tips
        if not all_tips:
            demo_tips = [
                {
                    'ticker': 'EQNR.OL',
                    'tip_type': 'BUY',
                    'confidence': 'HIGH',
                    'analysis': 'Equinor viser sterk teknisk styrke med RSI over 60 og MACD i positiv trend. Oljeprisen er stabil over $80 per fat, noe som støtter driften.',
                    'created_at': datetime.now()
                },
                {
                    'ticker': 'DNB.OL',
                    'tip_type': 'BUY',
                    'confidence': 'MEDIUM',
                    'analysis': 'DNB viser solid inntjeningsvekst og teknisk analyse indikerer et gjennombrudd over motstandsnivået på 210 NOK.',
                    'created_at': datetime.now() - timedelta(days=1)
                },
                {
                    'ticker': 'AAPL',
                    'tip_type': 'BUY',
                    'confidence': 'HIGH',
                    'analysis': 'Apple har sterk teknisk støtte og lansering av nye produkter forventes å drive inntektsvekst i kommende kvartal.',
                    'created_at': datetime.now() - timedelta(days=2)
                },
                {
                    'ticker': 'TSLA',
                    'tip_type': 'HOLD',
                    'confidence': 'MEDIUM',
                    'analysis': 'Tesla viser blandede signaler. Veksten fortsetter, men verdsettelsen er høy og konkurransen tiltar i EV-sektoren.',
                    'created_at': datetime.now() - timedelta(days=3)
                },
                {
                    'ticker': 'TEL.OL',
                    'tip_type': 'SELL',
                    'confidence': 'MEDIUM',
                    'analysis': 'Telenor viser svake tekniske signaler med RSI under 40 og fallende volum. Konkurransen i telekom-sektoren presser marginene.',
                    'created_at': datetime.now() - timedelta(days=4)
                }
            ]
            
            # Use demo tips instead of database tips
            return render_template('portfolio/tips.html', tips=demo_tips, demo_mode=True)
            
        return render_template('portfolio/tips.html', tips=all_tips, demo_mode=False)
    except Exception as e:
        print(f"Error in stock tips route: {str(e)}")
        return render_template('error.html', error=f"Det oppstod en feil: {str(e)}")

@portfolio.route('/tips/add', methods=['GET', 'POST'])
@login_required
def add_tip():
    """Add a stock tip"""
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        tip_type = request.form.get('tip_type')
        confidence = request.form.get('confidence')
        analysis = request.form.get('analysis')
        tip = StockTip(
            ticker=ticker,
            tip_type=tip_type,
            confidence=confidence,
            analysis=analysis,
            user_id=current_user.id
        )
        db.session.add(tip)
        db.session.commit()
        flash('Aksjetips lagt til', 'success')
        return redirect(url_for('portfolio.stock_tips'))
    ticker = request.args.get('ticker', '')
    return render_template('portfolio/add_tip.html', ticker=ticker)

@portfolio.route('/tips/feedback/<int:tip_id>', methods=['POST'])
@login_required
def tip_feedback(tip_id):
    """Submit feedback for a stock tip"""
    tip = StockTip.query.get_or_404(tip_id)
    feedback = request.form.get('feedback')
    tip.feedback = feedback
    db.session.commit()
    flash('Tilbakemelding lagret!', 'success')
    return redirect(url_for('portfolio.stock_tips'))

@portfolio.route('/add/<ticker>')
@login_required
def quick_add_stock(ticker):
    """Quickly add a stock to the user's portfolio"""
    stock_info = DataService.get_stock_info(ticker)
    if not stock_info:
        flash(f"Aksje {ticker} ble ikke funnet.", "danger")
        return redirect(url_for('main.index'))

    # Finn eller opprett brukerens første portefølje
    portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
    if not portfolio:
        portfolio = Portfolio(name="Min portefølje", user_id=current_user.id)
        db.session.add(portfolio)
        db.session.commit()

    # Sjekk om aksjen allerede finnes i porteføljen
    existing_stock = PortfolioStock.query.filter_by(portfolio_id=portfolio.id, ticker=ticker).first()
    if existing_stock:
        # Øk antall aksjer med 1
        existing_stock.quantity += 1
    else:
        # Legg til ny aksje med 1 aksje og dagens pris som snittpris
        avg_price = stock_info.get('regularMarketPrice') or 0
        stock = PortfolioStock(
            portfolio_id=portfolio.id,
            ticker=ticker,
            quantity=1,
            purchase_price=avg_price
        )
        db.session.add(stock)

    db.session.commit()
    flash(f"Aksje {ticker} lagt til i din portefølje!", "success")
    return redirect(url_for('portfolio.index'))

@portfolio.route('/add', methods=['GET', 'POST'])
@login_required
def add_stock():
    """Add a stock to the user's default portfolio"""
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        quantity = float(request.form.get('quantity', 0))
        purchase_price = float(request.form.get('purchase_price', 0))
        
        if not ticker or quantity <= 0 or purchase_price <= 0:
            flash('Alle felt må fylles ut korrekt.', 'danger')
            return redirect(url_for('portfolio.add_stock'))
        
        # Hent brukerens portefølje
        user_portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
        if not user_portfolio:
            user_portfolio = Portfolio(name="Min portefølje", user_id=current_user.id)
            db.session.add(user_portfolio)
            db.session.commit()
        
        # Sjekk om aksjen allerede finnes i porteføljen
        existing_stock = PortfolioStock.query.filter_by(portfolio_id=user_portfolio.id, ticker=ticker).first()
        if existing_stock:
            # Beregn ny gjennomsnittspris
            total_value = (existing_stock.quantity * existing_stock.purchase_price) + (quantity * purchase_price)
            total_quantity = existing_stock.quantity + quantity
            existing_stock.purchase_price = total_value / total_quantity
            existing_stock.quantity = total_quantity
        else:
            # Legg til ny aksje
            portfolio_stock = PortfolioStock(
                portfolio_id=user_portfolio.id,
                ticker=ticker,
                quantity=quantity,
                purchase_price=purchase_price
            )
            db.session.add(portfolio_stock)
        
        db.session.commit()
        flash(f'{ticker} lagt til i porteføljen.', 'success')
        return redirect(url_for('portfolio.index'))
    
    return render_template('portfolio/add_stock.html')

@portfolio.route('/edit/<ticker>', methods=['GET', 'POST'])
@login_required
def edit_stock(ticker):
    """Edit a stock in the user's portfolio"""
    # Hent brukerens portefølje
    user_portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
    if not user_portfolio:
        flash('Du har ingen portefølje ennå.', 'warning')
        return redirect(url_for('portfolio.index'))
    
    # Finn aksjen
    portfolio_stock = PortfolioStock.query.filter_by(
        portfolio_id=user_portfolio.id,
        ticker=ticker
    ).first_or_404()
    
    if request.method == 'POST':
        quantity = float(request.form.get('quantity', 0))
        purchase_price = float(request.form.get('purchase_price', 0))
        
        if quantity <= 0 or purchase_price <= 0:
            flash('Alle felt må fylles ut korrekt.', 'danger')
            return redirect(url_for('portfolio.edit_stock', ticker=ticker))
        
        # Oppdater aksjen
        portfolio_stock.quantity = quantity
        portfolio_stock.purchase_price = purchase_price
        db.session.commit()
        
        flash(f'{ticker} oppdatert i porteføljen.', 'success')
        return redirect(url_for('portfolio.index'))
    
    return render_template('portfolio/edit_stock.html', stock=portfolio_stock)

@portfolio.route('/remove/<ticker>')
@login_required
def remove_stock(ticker):
    """Remove a stock from the user's portfolio"""
    # Hent brukerens portefølje
    user_portfolio = Portfolio.query.filter_by(user_id=current_user.id).first()
    if not user_portfolio:
        flash('Du har ingen portefølje ennå.', 'warning')
        return redirect(url_for('portfolio.index'))
    
    # Finn aksjen
    portfolio_stock = PortfolioStock.query.filter_by(
        portfolio_id=user_portfolio.id,
        ticker=ticker
    ).first_or_404()
    
    # Slett aksjen
    db.session.delete(portfolio_stock)
    db.session.commit()
    
    flash(f'{ticker} fjernet fra porteføljen.', 'success')
    return redirect(url_for('portfolio.index'))

# Helper method to get stock data
def get_single_stock_data(ticker):
    """Get data for a single stock"""
    try:
        # Hent gjeldende data
        stock_data = DataService.get_stock_data(ticker, period='1d')
        if stock_data.empty:
            return None
            
        # Teknisk analyse
        ta_data = AnalysisService.get_technical_analysis(ticker)
        
        # Sett sammen data
        last_price = stock_data['Close'].iloc[-1]
        change = 0
        change_percent = 0
        
        if len(stock_data) > 1:
            prev_price = stock_data['Close'].iloc[-2]
            change = last_price - prev_price
            change_percent = (change / prev_price) * 100 if prev_price > 0 else 0
        
        return {
            'ticker': ticker,
            'last_price': round(last_price, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'signal': ta_data.get('signal', 'Hold') if ta_data else 'Hold',
            'rsi': ta_data.get('rsi', 'N/A') if ta_data else 'N/A',
            'volume': ta_data.get('volume', 'N/A') if ta_data else 'N/A'
        }
    except Exception as e:
        print(f"Error getting data for {ticker}: {str(e)}")
        return None