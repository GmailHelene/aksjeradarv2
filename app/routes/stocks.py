from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app.services.data_service import DataService
from app.services.analysis_service import AnalysisService
from flask_login import current_user
from datetime import datetime, timedelta

stocks = Blueprint('stocks', __name__)

@stocks.route('/')
def index():
    """Show a list of popular stocks"""
    # Get most active stocks
    oslo_stocks = DataService.get_oslo_bors_overview()
    global_stocks = DataService.get_global_stocks_overview()
    
    return render_template(
        'stocks/index.html',
        oslo_stocks=oslo_stocks,
        global_stocks=global_stocks
    )

@stocks.route('/details/<ticker>')
def details(ticker):
    """Show details for a specific stock"""
    try:
        # Get stock data
        stock_info = DataService.get_stock_info(ticker)
        stock_data = DataService.get_stock_data(ticker)
        technical_analysis = AnalysisService.get_technical_analysis(ticker)
        
        # Get historical data for chart
        historical_data = DataService.get_stock_data(ticker, period='1y')
        
        # Format data for chart
        chart_data = []
        if not historical_data.empty:
            for date, row in historical_data.iterrows():
                chart_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(row['Open'], 2),
                    'high': round(row['High'], 2),
                    'low': round(row['Low'], 2),
                    'close': round(row['Close'], 2),
                    'volume': int(row['Volume'])
                })
        
        return render_template(
            'stocks/details.html',
            ticker=ticker,
            stock_info=stock_info,
            stock_data=stock_data,
            technical_analysis=technical_analysis,
            chart_data=chart_data
        )
    except Exception as e:
        flash(f"Error fetching data for {ticker}: {str(e)}", "danger")
        return redirect(url_for('stocks.index'))

@stocks.route('/search')
def search():
    """Search for stocks"""
    query = request.args.get('query', '')
    if not query:
        return redirect(url_for('stocks.index'))
    
    results = DataService.search_ticker(query)
    return render_template('stocks/search.html', results=results, query=query)

@stocks.route('/list/oslo')
def oslo_list():
    """List all Oslo Børs stocks"""
    oslo_stocks = DataService.get_oslo_bors_overview()
    return render_template('stocks/list.html', stocks=oslo_stocks, title="Oslo Børs")

@stocks.route('/list/global')
def global_list():
    """List popular global stocks"""
    global_stocks = DataService.get_global_stocks_overview()
    return render_template('stocks/list.html', stocks=global_stocks, title="Global Markets")

@stocks.route('/list/crypto')
def crypto_list():
    """List popular cryptocurrencies"""
    crypto = DataService.get_crypto_overview()
    return render_template('stocks/list.html', stocks=crypto, title="Cryptocurrencies")

# Add this fallback route to handle the old URL pattern
@stocks.route('/list')
def list():
    """Redirect to oslo_list as a fallback"""
    return redirect(url_for('stocks.oslo_list'))

@stocks.route('/compare')
def compare():
    """Compare multiple stocks"""
    tickers = request.args.get('tickers', '').split(',')
    tickers = [t.strip() for t in tickers if t.strip()]
    
    if not tickers:
        return render_template('stocks/compare_form.html')
    
    comparison_data = {}
    chart_data = {}
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    for ticker in tickers:
        try:
            info = DataService.get_stock_info(ticker)
            data = DataService.get_stock_data(ticker, period='1y')
            technical = AnalysisService.get_technical_indicators(data)
            
            if not data.empty:
                # Current data
                comparison_data[ticker] = {
                    'name': info.get('shortName', ticker),
                    'last_price': round(data['Close'].iloc[-1], 2),
                    'change_percent': round(((data['Close'].iloc[-1] / data['Close'].iloc[-2]) - 1) * 100, 2),
                    'rsi': round(technical.get('rsi', 0), 2),
                    'volume': int(data['Volume'].iloc[-1]),
                    'year_high': round(data['High'].max(), 2),
                    'year_low': round(data['Low'].min(), 2)
                }
                
                # Chart data
                chart_data[ticker] = {
                    'dates': data.index.strftime('%Y-%m-%d').tolist(),
                    'prices': data['Close'].tolist()
                }
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
    
    return render_template(
        'stocks/compare.html',
        tickers=tickers,
        comparison_data=comparison_data,
        chart_data=chart_data
    )

@stocks.route('/api/stock/<ticker>')
def api_stock_data(ticker):
    """API endpoint for stock data"""
    try:
        stock_data = DataService.get_stock_data(ticker)
        if stock_data.empty:
            return jsonify({'error': 'No data found for ticker'})
        
        data = {
            'ticker': ticker,
            'last_price': stock_data['Close'].iloc[-1],
            'open': stock_data['Open'].iloc[-1],
            'high': stock_data['High'].iloc[-1],
            'low': stock_data['Low'].iloc[-1],
            'volume': stock_data['Volume'].iloc[-1],
            'date': stock_data.index[-1].strftime('%Y-%m-%d')
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})
