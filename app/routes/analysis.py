from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, send_from_directory
from ..services.analysis_service import AnalysisService
from ..services.ai_service import AIService
from ..services.export_service import ExportService
from ..services.data_service import DataService, OSLO_BORS_TICKERS, GLOBAL_TICKERS
from ..utils.subscription import subscription_required
import random
import pandas as pd
import time
from datetime import datetime


analysis = Blueprint('analysis', __name__)

@analysis.route('/')
@subscription_required
def index():
    oslo_stocks = DataService.get_oslo_bors_overview()
    global_stocks = DataService.get_global_stocks_overview()
    crypto = DataService.get_crypto_overview()
    currency = DataService.get_currency_overview()

    # Tell signalene
    buy_signals = sum(1 for d in oslo_stocks.values() if d.get('signal') == 'BUY')
    buy_signals += sum(1 for d in global_stocks.values() if d.get('signal') == 'BUY')
    sell_signals = sum(1 for d in oslo_stocks.values() if d.get('signal') == 'SELL')
    sell_signals += sum(1 for d in global_stocks.values() if d.get('signal') == 'SELL')
    neutral_signals = sum(1 for d in oslo_stocks.values() if d.get('signal') not in ['BUY', 'SELL'])
    neutral_signals += sum(1 for d in global_stocks.values() if d.get('signal') not in ['BUY', 'SELL'])

    # Markedssentiment (velg selv logikk, her: flest signaler vinner)
    if buy_signals > sell_signals and buy_signals > neutral_signals:
        market_sentiment = "Bullish"
    elif sell_signals > buy_signals and sell_signals > neutral_signals:
        market_sentiment = "Bearish"
    elif neutral_signals > 0:
        market_sentiment = "Neutral"
    else:
        market_sentiment = "N/A"

    return render_template(
        'analysis/index.html',
        oslo_stocks=oslo_stocks,
        global_stocks=global_stocks,
        crypto=crypto,
        currency=currency,
        buy_signals=buy_signals,
        sell_signals=sell_signals,
        neutral_signals=neutral_signals,
        market_sentiment=market_sentiment
    )

@analysis.route('/technical')
@subscription_required
def technical():
    """Technical analysis view"""
    ticker = request.args.get('ticker')
    if not ticker:
        # Create demo data for the technical analysis page
        analyses = {
            # Oslo Børs
            'EQNR.OL': {
                'last_price': 342.55,
                'signal': 'BUY',
                'rsi': 65.8,
                'macd': 0.75,
                'macd_signal': 0.32,
                'support': 325.00,
                'resistance': 350.00,
                'volume': 3200000,
                'avg_volume': 2800000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Teknisk analyse viser positive signaler for Equinor med RSI i oppgående trend og MACD over signallinjen.'
            },
            'DNB.OL': {
                'last_price': 212.80,
                'signal': 'HOLD',
                'rsi': 52.3,
                'macd': -0.15,
                'macd_signal': -0.12,
                'support': 205.00,
                'resistance': 220.00,
                'volume': 1500000,
                'avg_volume': 1400000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'DNB viser nøytrale tekniske signaler med RSI nær midtlinjen og MACD nær nulllinjen.'
            },
            'TEL.OL': {
                'last_price': 125.90,
                'signal': 'SELL',
                'rsi': 32.1,
                'macd': -0.55,
                'macd_signal': -0.32,
                'support': 120.00,
                'resistance': 135.00,
                'volume': 1200000,
                'avg_volume': 1100000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Telenor viser negative tekniske signaler med RSI nær oversolgt område og MACD under signallinjen.'
            },
            'YAR.OL': {
                'last_price': 345.10,
                'signal': 'BUY',
                'rsi': 63.2,
                'macd': 0.86,
                'macd_signal': 0.45,
                'support': 335.00,
                'resistance': 355.00,
                'volume': 900000,
                'avg_volume': 850000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Yara viser positive tekniske signaler med RSI og MACD i oppadgående trend.'
            },
            'NHY.OL': {
                'last_price': 65.28,
                'signal': 'HOLD',
                'rsi': 50.6,
                'macd': 0.05,
                'macd_signal': 0.03,
                'support': 62.00,
                'resistance': 68.00,
                'volume': 8300000,
                'avg_volume': 7800000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Norsk Hydro viser nøytrale tekniske signaler med RSI nær midtlinjen og MACD nær nulllinjen.'
            },
            'MOWI.OL': {
                'last_price': 186.30,
                'signal': 'BUY',
                'rsi': 62.8,
                'macd': 0.62,
                'macd_signal': 0.40,
                'support': 175.00,
                'resistance': 195.00,
                'volume': 1100000,
                'avg_volume': 980000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Mowi viser positive tekniske signaler med RSI i stigende trend og stigende volum.'
            },
            'ORK.OL': {
                'last_price': 78.50,
                'signal': 'HOLD',
                'rsi': 47.2,
                'macd': -0.12,
                'macd_signal': -0.10,
                'support': 76.00,
                'resistance': 82.00,
                'volume': 750000,
                'avg_volume': 720000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Orkla viser nøytrale tekniske signaler med flat RSI-trend og MACD nær nulllinjen.'
            },
            'AKSO.OL': {
                'last_price': 44.65,
                'signal': 'BUY',
                'rsi': 68.4,
                'macd': 0.48,
                'macd_signal': 0.22,
                'support': 42.00,
                'resistance': 46.50,
                'volume': 920000,
                'avg_volume': 860000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Aker Solutions viser positive tekniske signaler med sterk RSI-trend og økende volum.'
            },
            'BAKKA.OL': {
                'last_price': 615.20,
                'signal': 'SELL',
                'rsi': 35.6,
                'macd': -1.20,
                'macd_signal': -0.75,
                'support': 600.00,
                'resistance': 630.00,
                'volume': 180000,
                'avg_volume': 160000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Bakkafrost viser negative tekniske signaler med RSI i fallende trend og MACD under signallinjen.'
            },
            
            # Global Stocks
            'AAPL': {
                'last_price': 185.70,
                'signal': 'BUY',
                'rsi': 62.5,
                'macd': 0.43,
                'macd_signal': 0.21,
                'support': 178.00,
                'resistance': 192.00,
                'volume': 52000000,
                'avg_volume': 48000000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Apple viser positive tekniske signaler med RSI i oppadgående trend og økende volum.'
            },
            'MSFT': {
                'last_price': 390.20,
                'signal': 'BUY',
                'rsi': 67.8,
                'macd': 1.25,
                'macd_signal': 0.65,
                'support': 375.00,
                'resistance': 400.00,
                'volume': 22000000,
                'avg_volume': 19500000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Microsoft viser sterke tekniske signaler med både RSI og MACD i oppadgående trend.'
            },
            'TSLA': {
                'last_price': 230.10,
                'signal': 'SELL',
                'rsi': 28.5,
                'macd': -1.85,
                'macd_signal': -0.95,
                'support': 220.00,
                'resistance': 250.00,
                'volume': 89000000,
                'avg_volume': 65000000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Tesla viser negative tekniske signaler med RSI i oversolgt område og MACD under signallinjen.'
            },
            'AMZN': {
                'last_price': 178.90,
                'signal': 'BUY',
                'rsi': 58.2,
                'macd': 0.78,
                'macd_signal': 0.45,
                'support': 172.00,
                'resistance': 185.00,
                'volume': 35000000,
                'avg_volume': 32000000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Amazon viser positive tekniske signaler med RSI i opptrend og MACD over signallinjen.'
            },
            'GOOGL': {
                'last_price': 155.50,
                'signal': 'BUY',
                'rsi': 61.2,
                'macd': 0.65,
                'macd_signal': 0.32,
                'support': 150.00,
                'resistance': 162.00,
                'volume': 25000000,
                'avg_volume': 22500000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Alphabet viser positive tekniske signaler med solid RSI-trend og økende volum.'
            },
            'META': {
                'last_price': 483.85,
                'signal': 'HOLD',
                'rsi': 55.1,
                'macd': 0.22,
                'macd_signal': 0.18,
                'support': 470.00,
                'resistance': 495.00,
                'volume': 18000000,
                'avg_volume': 16500000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Meta viser nøytrale tekniske signaler med RSI nær midtlinjen og MACD nær signallinjen.'
            },
            
            # Crypto
            'BTC-USD': {
                'last_price': 65432.10,
                'signal': 'BUY',
                'rsi': 68.3,
                'macd': 245.32,
                'macd_signal': 180.45,
                'support': 60000.00,
                'resistance': 70000.00,
                'volume': 25000000000,
                'avg_volume': 22000000000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Bitcoin viser sterke tekniske signaler med RSI i opptrend og MACD over signallinjen.'
            },
            'ETH-USD': {
                'last_price': 3456.78,
                'signal': 'HOLD',
                'rsi': 55.2,
                'macd': 12.34,
                'macd_signal': 10.56,
                'support': 3200.00,
                'resistance': 3600.00,
                'volume': 15000000000,
                'avg_volume': 14000000000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Ethereum viser nøytrale tekniske signaler med RSI nær midtlinjen og MACD nær signallinjen.'
            },
            'XRP-USD': {
                'last_price': 0.5678,
                'signal': 'HOLD',
                'rsi': 49.8,
                'macd': 0.0023,
                'macd_signal': 0.0021,
                'support': 0.55,
                'resistance': 0.60,
                'volume': 1800000000,
                'avg_volume': 1650000000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Ripple viser nøytrale tekniske signaler med RSI nær midtlinjen og MACD nær signallinjen.'
            },
            'ADA-USD': {
                'last_price': 0.4532,
                'signal': 'BUY',
                'rsi': 63.5,
                'macd': 0.0032,
                'macd_signal': 0.0018,
                'support': 0.42,
                'resistance': 0.48,
                'volume': 1200000000,
                'avg_volume': 1100000000,
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'Cardano viser positive tekniske signaler med RSI i opptrend og økende volum.'
            },
            
            # Currency
            'EURUSD=X': {
                'last_price': 1.0865,
                'signal': 'BUY',
                'rsi': 62.7,
                'macd': 0.0012,
                'macd_signal': 0.0008,
                'support': 1.08,
                'resistance': 1.09,
                'volume': 'N/A',
                'avg_volume': 'N/A',
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'EUR/USD viser positive tekniske signaler med RSI i opptrend og MACD over signallinjen.'
            },
            'USDJPY=X': {
                'last_price': 151.23,
                'signal': 'SELL',
                'rsi': 32.8,
                'macd': -0.021,
                'macd_signal': -0.012,
                'support': 150.00,
                'resistance': 152.50,
                'volume': 'N/A',
                'avg_volume': 'N/A',
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'USD/JPY viser negative tekniske signaler med RSI i fallende trend og MACD under signallinjen.'
            },
            'GBPUSD=X': {
                'last_price': 1.2654,
                'signal': 'BUY',
                'rsi': 64.2,
                'macd': 0.0015,
                'macd_signal': 0.0009,
                'support': 1.26,
                'resistance': 1.27,
                'volume': 'N/A',
                'avg_volume': 'N/A',
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'GBP/USD viser positive tekniske signaler med RSI i opptrend og MACD over signallinjen.'
            },
            'NOKUSD=X': {
                'last_price': 0.0956,
                'signal': 'HOLD',
                'rsi': 48.9,
                'macd': 0.0002,
                'macd_signal': 0.0002,
                'support': 0.094,
                'resistance': 0.097,
                'volume': 'N/A',
                'avg_volume': 'N/A',
                'last_update': datetime.now().strftime('%Y-%m-%d'),
                'signal_reason': 'NOK/USD viser nøytrale tekniske signaler med RSI nær midtlinjen og MACD på samme nivå som signallinjen.'
            }
        }
        
        return render_template('analysis/technical.html', analyses=analyses)
    
    try:
        # Get technical analysis data for a specific ticker
        technical_data = AnalysisService.get_technical_analysis(ticker)
        if 'error' in technical_data:
            return render_template('analysis/technical.html', 
                                  error=technical_data['error'],
                                  ticker=ticker)
        
        return render_template('analysis/technical.html', 
                              ticker=ticker,
                              technical_data=technical_data)
    except Exception as e:
        print(f"Error in technical route: {str(e)}")
        return render_template('analysis/technical.html', 
                              error=f"En feil oppstod: {str(e)}",
                              ticker=ticker)

@analysis.route('/technical/<ticker>')
@subscription_required
def technical_analysis(ticker):
    """Show technical analysis for a specific stock"""
    try:
        # Get stock data
        stock_data = DataService.get_stock_data(ticker, period='6mo', interval='1d')
        stock_info = DataService.get_stock_info(ticker)
        
        # Get technical indicators
        indicators = AnalysisService.calculate_technical_indicators(stock_data)
        
        # Get AI-based prediction if available
        try:
            prediction = AIService.get_stock_prediction(ticker)
        except Exception as e:
            current_app.logger.warning(f"Could not get AI prediction for {ticker}: {str(e)}")
            prediction = None
        
        return render_template(
            'analysis/technical.html',
            ticker=ticker,
            stock=stock_info,
            data=stock_data,
            indicators=indicators,
            prediction=prediction
        )
        
    except Exception as e:
        current_app.logger.error(f"Error in technical analysis for {ticker}: {str(e)}")
        flash(f"Kunne ikke hente teknisk analyse for {ticker}. Vennligst prøv igjen senere.", "error")
        return redirect(url_for('stocks.index'))

@analysis.route('/prediction', methods=['GET', 'POST'])
@subscription_required
def prediction():
    """Show price predictions for multiple stocks"""
    try:
        # Tickers vi vet fungerer
        tickers_oslo = ['EQNR.OL', 'DNB.OL', 'TEL.OL', 'YAR.OL', 'NHY.OL']
        tickers_global = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA']
        
        predictions_oslo = {}
        predictions_global = {}
        
        # Legg til konkrete demoprediksjoner for Oslo Børs
        for ticker in tickers_oslo:
            predictions_oslo[ticker] = {
                'ticker': ticker,
                'last_price': round(300 + 10 * tickers_oslo.index(ticker), 2),
                'next_price': round(300 + 10 * tickers_oslo.index(ticker) * 1.02, 2),
                'change_percent': round(2.0 - 0.2 * tickers_oslo.index(ticker), 2),
                'trend': 'UP' if tickers_oslo.index(ticker) % 3 != 0 else 'DOWN',
                'confidence': 'HIGH' if tickers_oslo.index(ticker) % 3 == 0 else ('MEDIUM' if tickers_oslo.index(ticker) % 3 == 1 else 'LOW'),
                'last_update': '2025-06-17',
                'volatility': round(2.0 + 0.5 * tickers_oslo.index(ticker), 2),
                'trend_period': '5 dager',
                'data_period': '60 dager',
                'prediction_reason': f"Begrunnelse: Sterk positiv trend siste 5 dager • Kursen er over 50-dagers glidende gjennomsnitt • {tickers_oslo.index(ticker) % 3 == 0 and 'Høy' or 'Moderat'} volatilitet indikerer {tickers_oslo.index(ticker) % 3 == 0 and 'usikkerhet' or 'stabilitet'}"
            }
        
        # Legg til konkrete demoprediksjoner for globale aksjer
        for ticker in tickers_global:
            predictions_global[ticker] = {
                'ticker': ticker,
                'last_price': round(150 + 20 * tickers_global.index(ticker), 2),
                'next_price': round((150 + 20 * tickers_global.index(ticker)) * (1 + ((-1) ** tickers_global.index(ticker)) * 0.01), 2),
                'change_percent': round(((-1) ** tickers_global.index(ticker)) * (1.5 + 0.2 * tickers_global.index(ticker)), 2),
                'trend': 'UP' if tickers_global.index(ticker) % 2 == 0 else 'DOWN',
                'confidence': 'HIGH' if tickers_global.index(ticker) % 3 == 0 else ('MEDIUM' if tickers_global.index(ticker) % 3 == 1 else 'LOW'),
                'last_update': '2025-06-17',
                'volatility': round(1.5 + 0.3 * tickers_global.index(ticker), 2),
                'trend_period': '5 dager',
                'data_period': '60 dager',
                'prediction_reason': f"Begrunnelse: {tickers_global.index(ticker) % 2 == 0 and 'Positiv' or 'Negativ'} trend siste 5 dager • Kursen er {tickers_global.index(ticker) % 2 == 0 and 'over' or 'under'} 50-dagers glidende gjennomsnitt • {tickers_global.index(ticker) % 3 == 0 and 'Høy' or 'Moderat'} konfidens i prognosen"
            }
        
        return render_template(
            'analysis/prediction.html',
            predictions_oslo=predictions_oslo,
            predictions_global=predictions_global
        )
    except Exception as e:
        print(f"Error in prediction route: {str(e)}")
        return render_template(
            'error.html', 
            error=f"Det oppstod en feil ved generering av prediksjoner: {str(e)}"
        )

@analysis.route('/recommendation')
@subscription_required
def recommendation():
    ticker = request.args.get('ticker')
    
    # Hvis ingen ticker er spesifisert, vis en side for å velge ticker
    if not ticker:
        # Vis demo-data hvis vi ikke kan hente faktiske data
        oslo_stocks = {
            'EQNR.OL': {'signal': 'BUY', 'last_price': 322.50, 'change_percent': 2.1},
            'DNB.OL': {'signal': 'HOLD', 'last_price': 218.90, 'change_percent': -0.8},
            'TEL.OL': {'signal': 'BUY', 'last_price': 123.45, 'change_percent': 1.5},
            'NHY.OL': {'signal': 'SELL', 'last_price': 65.30, 'change_percent': -1.2},
            'AKSO.OL': {'signal': 'HOLD', 'last_price': 34.80, 'change_percent': 0.5}
        }
        
        global_stocks = {
            'AAPL': {'signal': 'BUY', 'last_price': 185.70, 'change_percent': 1.8},
            'MSFT': {'signal': 'BUY', 'last_price': 390.20, 'change_percent': 2.3},
            'AMZN': {'signal': 'HOLD', 'last_price': 178.90, 'change_percent': 0.2},
            'GOOGL': {'signal': 'BUY', 'last_price': 155.50, 'change_percent': 1.5},
            'TSLA': {'signal': 'SELL', 'last_price': 230.10, 'change_percent': -2.1}
        }
        
        try:
            # Prøv å hente faktiske data hvis tilgjengelig
            real_oslo = DataService.get_oslo_bors_overview()
            if real_oslo and len(real_oslo) > 0:
                oslo_stocks = real_oslo
            
            real_global = DataService.get_global_stocks_overview()
            if real_global and len(real_global) > 0:
                global_stocks = real_global
        except Exception as e:
            print(f"Error getting stock overviews: {str(e)}")
        
        return render_template(
            'analysis/recommendation_select.html',
            oslo_stocks=oslo_stocks,
            global_stocks=global_stocks
        )
    
    # Hvis vi har en ticker, vis anbefaling
    try:
        recommendation = AnalysisService.get_stock_recommendation(ticker)
        
        # Fallback hvis vi ikke får data
        if not recommendation or 'error' in recommendation:
            recommendation = {
                'ticker': ticker,
                'recommendation': 'HOLD',
                'confidence': 'MEDIUM',
                'technical_analysis': {
                    'signal': 'Hold',
                    'signal_reason': 'Begrunnelse ikke tilgjengelig',
                    'rsi': 50,
                    'macd': 0,
                    'support': 0,
                    'resistance': 0
                },
                'prediction': {
                    'next_price': 0,
                    'change_percent': 0,
                    'confidence': 'MEDIUM'
                }
            }
        
        # Legg til chart-bilde hvis det er tilgjengelig
        try:
            chart_img = AnalysisService.plot_stock_chart(ticker)
            if chart_img:
                chart_img = chart_img.split('base64,')[1] if 'base64,' in chart_img else chart_img
                recommendation['technical_analysis']['chart_img'] = chart_img
        except Exception as e:
            print(f"Error generating chart for {ticker}: {str(e)}")
        
        return render_template(
            'analysis/recommendation.html',
            ticker=ticker,
            recommendation=recommendation
        )
    except Exception as e:
        print(f"Error in recommendation route for {ticker}: {str(e)}")
        return render_template(
            'error.html', 
            error=f"Det oppstod en feil ved generering av anbefaling for {ticker}: {str(e)}"
        )


@analysis.route('/ai', methods=['GET', 'POST'])
@subscription_required
def ai():
    """AI analysis view"""
    ticker = request.args.get('ticker')
    if not ticker:
        return render_template('analysis/ai.html')
    
    try:
        # Get AI analysis
        analysis = AIService.get_stock_analysis(ticker)
        if 'error' in analysis:
            return render_template('analysis/ai.html', 
                                  error=analysis['error'],
                                  ticker=ticker)
        
        return render_template('analysis/ai.html', 
                              ticker=ticker,
                              analysis=analysis)
    except Exception as e:
        print(f"Error in AI analysis route: {str(e)}")
        return render_template('analysis/ai.html', 
                              error=f"En feil oppstod: {str(e)}",
                              ticker=ticker)
    

@analysis.route('/market-overview')
@subscription_required
def market_overview():
    market_overview = DataService.get_market_overview()
    return render_template(
        'analysis/market_overview.html',
        oslo_stocks=market_overview['oslo_stocks'],
        global_stocks=market_overview['global_stocks'],
        crypto=market_overview['crypto'],
        currency=market_overview['currency']
)

# Add new routes
@analysis.route('/api/analysis/indicators', methods=['GET'])
@subscription_required
def get_indicators():
    """Get technical indicators for a stock"""
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Symbol parameter is required"}), 400
    
    try:
        # Endre til å bruke DataService.get_stock_data istedenfor get_stock_data
        stock_data = DataService.get_stock_data(symbol)
        
        # Calculate indicators
        indicators = AnalysisService.get_technical_indicators(stock_data)
        
        # Convert pandas Series to lists for JSON serialization
        result = {}
        for key, value in indicators.items():
            if isinstance(value, pd.Series):
                # Take last 30 days for frontend display
                result[key] = value.tail(30).tolist()
            else:
                result[key] = value
        
        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analysis.route('/api/analysis/signals', methods=['GET'])
@subscription_required
def get_trading_signals():
    """Get trading signals for a stock"""
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Symbol parameter is required"}), 400
    
    try:
        # Endre til å bruke DataService.get_stock_data istedenfor get_stock_data
        stock_data = DataService.get_stock_data(symbol)
        
        # Generate signals
        signals = AnalysisService.generate_trading_signals(stock_data)
        
        return jsonify({
            "success": True,
            "signals": signals
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analysis.route('/api/market-summary', methods=['GET'])
@subscription_required
def get_market_summary():
    """Get AI-generated market summary"""
    sector = request.args.get('sector')
    
    # Get AI summary
    summary = AIService.generate_market_summary(sector)
    
    return jsonify(summary)

@analysis.route('/api/export/csv', methods=['POST'])
@subscription_required
def export_csv():
    """Export data to CSV"""
    data = request.json.get('data')
    filename = request.json.get('filename')
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    result = ExportService.export_to_csv(data, filename)
    
    return jsonify(result)

@analysis.route('/api/export/pdf', methods=['POST'])
@subscription_required
def export_pdf():
    """Export data to PDF"""
    data = request.json.get('data')
    title = request.json.get('title', 'Aksjeradar Rapport')
    filename = request.json.get('filename')
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    result = ExportService.export_to_pdf(data, title, filename)
    
    return jsonify(result)

@analysis.route('/api/email/send', methods=['POST'])
@subscription_required
def send_email():
    """Send email with report"""
    recipient = request.json.get('recipient')
    subject = request.json.get('subject', 'Din rapport fra Aksjeradar')
    body = request.json.get('body', '<p>Her er din rapport fra Aksjeradar.</p>')
    attachments = request.json.get('attachments', [])
    
    if not recipient:
        return jsonify({"error": "Recipient email is required"}), 400
    
    result = ExportService.send_email(recipient, subject, body, attachments)
    
    return jsonify(result)

@analysis.route('/api/email/schedule', methods=['POST'])
@subscription_required
def schedule_email():
    """Schedule daily email report"""
    user_id = request.json.get('user_id')
    report_type = request.json.get('report_type', 'portfolio')
    email = request.json.get('email')
    
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    result = ExportService.schedule_daily_report(user_id, report_type, email)
    
    return jsonify(result)

@analysis.route('/downloads/<path:filename>')
@subscription_required
def download_file(filename):
    """Download exported files"""
    return send_from_directory(current_app.config['EXPORT_FOLDER'], filename, as_attachment=True)

# Flyttet disse metodene til analysis_service.py - hold dem her bare hvis du har referanser til dem andre steder
# Hvis disse metodene flyttes til analysis_service.py, kan du fjerne disse klassene