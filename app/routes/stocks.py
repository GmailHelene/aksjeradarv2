import math
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from ..services.data_service import DataService
from ..services.analysis_service import AnalysisService
from flask_login import current_user
from ..utils.subscription import subscription_required
from ..utils.trial import trial_required
from datetime import datetime, timedelta

stocks = Blueprint('stocks', __name__)

@stocks.route('/')
@trial_required
def index():
    """Show a list of popular stocks"""
    try:
        # Get most active stocks with limits for a quick overview
        oslo_stocks = DataService.get_oslo_bors_overview(limit=5)
        global_stocks = DataService.get_global_stocks_overview(limit=5)
        crypto_data = DataService.get_crypto_overview(limit=5)
        currency_data = DataService.get_currency_overview()
        
        # Mix all stock types into a single dict for the template
        all_stocks = {}
        all_stocks.update(oslo_stocks)
        all_stocks.update(global_stocks)
        all_stocks.update(crypto_data)
        all_stocks.update(currency_data)
        
        return render_template(
            'stocks/list.html',
            stocks=all_stocks,
            market_types={
                'oslo': list(oslo_stocks.keys()),
                'global': list(global_stocks.keys()),
                'crypto': list(crypto_data.keys()),
                'currency': list(currency_data.keys())
            },
            title="Markedsoversikt"
        )
    except Exception as e:
        current_app.logger.error(f"Error in stocks index: {str(e)}")
        flash("En feil oppstod ved henting av markedsdata. Vennligst prøv igjen senere.", "error")
        return render_template('stocks/list.html', title="Markedsoversikt")

@stocks.route('/details/<ticker>')
@trial_required
def details(ticker):
    """Show details for a specific stock"""
    try:
        stock_info = DataService.get_stock_info(ticker)
        stock_data = DataService.get_stock_data(ticker, period='1mo', interval='1d')
        
        return render_template(
            'stocks/details.html',
            ticker=ticker,
            stock=stock_info,
            historical_data=stock_data
        )
    except Exception as e:
        current_app.logger.error(f"Error in stock details for {ticker}: {str(e)}")
        flash(f"Kunne ikke hente data for {ticker}. Vennligst prøv igjen senere.", "error")
        return redirect(url_for('stocks.index'))

@stocks.route('/search')
@trial_required
def search():
    """Search for stocks"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    
    try:
        results = DataService.search_stocks(query)
        return jsonify(results)
    except Exception as e:
        current_app.logger.error(f"Error in stock search: {str(e)}")
        return jsonify({'error': 'Søket feilet. Vennligst prøv igjen.'}), 500

@stocks.route('/list/oslo')
@trial_required
def oslo_list():
    """List all Oslo Børs stocks"""
    try:
        stocks = DataService.get_oslo_bors_overview()
        return render_template(
            'stocks/list.html',
            stocks=stocks,
            market_type="oslo",
            title="Oslo Børs"
        )
    except Exception as e:
        current_app.logger.error(f"Error in Oslo Børs list: {str(e)}")
        flash("Kunne ikke hente Oslo Børs data. Vennligst prøv igjen senere.", "error")
        return render_template('stocks/list.html', stocks={}, title="Oslo Børs", market_type="oslo")

@stocks.route('/list/global')
@trial_required
def global_list():
    """List global stocks"""
    try:
        stocks = DataService.get_global_stocks_overview()
        return render_template(
            'stocks/list.html',
            stocks=stocks,
            market_type="global",
            title="Globale markeder"
        )
    except Exception as e:
        current_app.logger.error(f"Error in global stocks list: {str(e)}")
        flash("Kunne ikke hente globale markedsdata. Vennligst prøv igjen senere.", "error")
        return render_template('stocks/list.html', stocks={}, title="Globale markeder", market_type="global")

@stocks.route('/list/crypto')
@trial_required
def crypto_list():
    """List cryptocurrencies"""
    try:
        stocks = DataService.get_crypto_overview()
        return render_template(
            'stocks/crypto.html',
            stocks=stocks,
            market_type="crypto",
            title="Kryptovaluta"
        )
    except Exception as e:
        current_app.logger.error(f"Error in crypto list: {str(e)}")
        flash("Kunne ikke hente kryptovalutadata. Vennligst prøv igjen senere.", "error")
        return render_template('stocks/crypto.html', stocks={}, title="Kryptovaluta", market_type="crypto")

@stocks.route('/list/currency')
@trial_required
def currency_list():
    """List currency pairs"""
    try:
        stocks = DataService.get_currency_overview()
        return render_template(
            'stocks/currency.html',
            stocks=stocks,
            market_type="currency",
            title="Valutakurser"
        )
    except Exception as e:
        current_app.logger.error(f"Error in currency list: {str(e)}")
        flash("Kunne ikke hente valutadata. Vennligst prøv igjen senere.", "error")
        return render_template('stocks/currency.html', stocks={}, title="Valutakurser", market_type="currency")

@stocks.route('/api/stock/<ticker>')
def api_stock_data(ticker):
    """API endpoint for stock data"""
    try:
        period = request.args.get('period', '1d')
        interval = request.args.get('interval', '1m')
        data = DataService.get_stock_data(ticker, period, interval)
        return jsonify(data)
    except Exception as e:
        current_app.logger.error(f"Error in stock API for {ticker}: {str(e)}")
        return jsonify({'error': 'Kunne ikke hente aksjedata'}), 500

@stocks.route('/compare')
@trial_required
def compare():
    """Compare multiple stocks"""
    try:
        tickers = request.args.getlist('ticker')
        if not tickers:
            return render_template('stocks/compare.html')
        
        stocks_data = {}
        for ticker in tickers:
            try:
                stock_info = DataService.get_stock_info(ticker)
                stock_data = DataService.get_stock_data(ticker, period='6mo', interval='1d')
                stocks_data[ticker] = {
                    'info': stock_info,
                    'data': stock_data
                }
            except Exception as e:
                current_app.logger.error(f"Error getting data for {ticker}: {str(e)}")
        
        return render_template(
            'stocks/compare.html',
            stocks=stocks_data,
            tickers=tickers
        )
    except Exception as e:
        current_app.logger.error(f"Error in stock comparison: {str(e)}")
        flash("Kunne ikke sammenligne aksjene. Vennligst prøv igjen senere.", "error")
        return render_template('stocks/compare.html')
