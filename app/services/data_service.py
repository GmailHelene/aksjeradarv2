import yfinance as yf
import pandas as pd
import requests
import time
import os
from datetime import datetime, timedelta
import numpy as np

# Forsøk å importere NewsApiClient, men håndter feil hvis den ikke finnes
try:
    from newsapi import NewsApiClient
    HAS_NEWSAPI = True
except ImportError:
    HAS_NEWSAPI = False
    print("NewsAPI not available. Using sample data for market news.")

# Oslo Børs ticker symbols
OSLO_BORS_TICKERS = [
    "EQNR.OL", "DNB.OL", "NHY.OL", "YAR.OL", "TEL.OL", "ORK.OL", "MOWI.OL", "SALM.OL", "TGS.OL", "SUBC.OL",
    "AKSO.OL", "AKERBP.OL", "PGS.OL", "STB.OL", "KOG.OL", "ELK.OL", "NOD.OL", "SCATC.OL", "BWLPG.OL", "GOGL.OL",
    "ODF.OL", "FRO.OL", "HAFNI.OL", "MPC.OL", "SASNO.OL", "NAS.OL", "NRC.OL", "AFG.OL", "BONHR.OL", "DNO.OL",
    "GSF.OL", "LPG.OL", "QFR.OL", "SCHA.OL", "SNI.OL", "TOM.OL", "VOW.OL", "WWI.OL", "ZAL.OL", "XXL.OL"
]

# Global tickers
GLOBAL_TICKERS = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA", "BRK-B", "JPM", "V",
    "UNH", "HD", "PG", "MA", "LLY", "AVGO", "XOM", "MRK", "ABBV", "COST",
    "PEP", "KO", "CVX", "WMT", "BAC", "DIS", "ADBE", "CSCO", "PFE", "T",
    "NKE", "MCD", "ORCL", "CRM", "ABT", "CMCSA", "TMO", "ACN", "DHR", "TXN",
    "LIN", "NEE", "WFC", "BMY", "PM", "HON", "AMGN", "UNP", "UPS", "LOW", "QCOM"
]

# Crypto tickers (for søk)
CRYPTO_TICKERS = [
    "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "AVAX-USD", "DOT-USD", "LINK-USD",
    "MATIC-USD", "TRX-USD", "LTC-USD", "BCH-USD", "XLM-USD", "ATOM-USD", "ETC-USD", "FIL-USD", "ICP-USD", "APT-USD",
    "HBAR-USD", "VET-USD", "NEAR-USD", "OP-USD", "GRT-USD", "AAVE-USD", "SAND-USD", "MANA-USD", "XTZ-USD", "EGLD-USD"
]

class DataService:
    @staticmethod
    def get_stock_data(ticker, period='1mo', interval='1d', max_retries=3, retry_delay=2):
        """
        Get historical stock data with rate limiting handling
        """
        # Sjekk om tickeren er i en "blacklist" av kjente ugyldige tickers
        invalid_tickers = ['MET-A', '^OSEBX']
        if ticker in invalid_tickers:
            print(f"Skipping known invalid ticker: {ticker}")
            return pd.DataFrame()  # Return empty dataframe
            
        for attempt in range(max_retries):
            try:
                # Set auto_adjust explicitly to avoid warning
                data = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
                
                # Check if data is empty properly
                if data.empty:
                    print(f"No data found for {ticker} on attempt {attempt+1}")
                    time.sleep(retry_delay)
                    continue
                    
                return data
            except Exception as e:
                print(f"Error downloading {ticker} on attempt {attempt+1}: {str(e)}")
                time.sleep(retry_delay)
        
        # If we reach here, all attempts failed
        print(f"Failed to fetch data for {ticker} after {max_retries} attempts")
        return pd.DataFrame()  # Return empty dataframe

    @staticmethod
    def get_stock_info(ticker):
        """Get detailed information about a stock"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return info
        except Exception as e:
            print(f"Error fetching info for {ticker}: {e}")
            return {}

    @staticmethod
    def get_multiple_stocks_data(tickers):
        """Get data for multiple stocks"""
        result = {}
        skipped_tickers = []
        
        for ticker in tickers:
            try:
                data = DataService.get_stock_data(ticker)
                if data.empty:
                    print(f"Skipping {ticker} due to empty data")
                    skipped_tickers.append(ticker)
                    continue
                    
                if len(data) > 1:
                    # Konverter eksplisitt til Python typer med .item()
                    last_close = float(data['Close'].iloc[-1])
                    prev_close = float(data['Close'].iloc[-2])
                else:
                    last_close = float(data['Close'].iloc[-1])
                    prev_close = float(data['Open'].iloc[-1])
                
                # Nå er verdiene native Python typer, ikke pandas Series eller numpy typer
                change = last_close - prev_close
                change_percent = (change / prev_close) * 100 if prev_close > 0 else 0
                
                signal = "BUY" if change_percent > 0 else "SELL"
                
                result[ticker] = {
                    'name': ticker,
                    'last_price': last_close,
                    'change': change,
                    'change_percent': change_percent,
                    'signal': signal,
                    'data': data
                }
            except Exception as e:
                print(f"Error processing {ticker}: {str(e)}")
                skipped_tickers.append(ticker)
                result[ticker] = {
                    'name': ticker,
                    'last_price': 'N/A',
                    'change': 'N/A',
                    'change_percent': 'N/A',
                    'signal': 'N/A',
                    'error': str(e)
                }
    
        if skipped_tickers:
            print(f"Skipped tickers: {', '.join(skipped_tickers)}")
            
        return result

    @staticmethod
    def get_oslo_bors_overview():
        """Get overview of Oslo Børs stocks"""
        tickers = ['EQNR.OL', 'DNB.OL', 'MOWI.OL', 'TEL.OL', 'YAR.OL']
        return DataService.get_multiple_stocks_data(tickers)

    @staticmethod
    def get_global_stocks_overview():
        """Get overview of global stocks"""
        tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
        return DataService.get_multiple_stocks_data(tickers)

    @staticmethod
    def get_crypto_overview():
        """Get overview of cryptocurrencies"""
        tickers = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'SOL-USD', 'DOGE-USD']
        return DataService.get_multiple_stocks_data(tickers)

    @staticmethod
    def search_ticker(query):
        """Search for ticker symbols"""
        all_tickers = OSLO_BORS_TICKERS + GLOBAL_TICKERS + CRYPTO_TICKERS
        return [ticker for ticker in all_tickers if query.upper() in ticker.upper()]

    @staticmethod
    def get_single_stock_data(ticker):
        """Get data for a single stock"""
        result = DataService.get_multiple_stocks_data([ticker])
        return result.get(ticker, {})

    @staticmethod
    def get_currency_overview():
        """Get the latest currency exchange rates"""
        url = "https://api.exchangerate.host/latest"
        params = {"base": "USD", "symbols": "NOK,EUR,SEK,GBP"}
        try:
            r = requests.get(url, params=params, timeout=10)
            data = r.json()
            rates = data.get("rates", {})
            # Sjekk at date finnes, ellers bruk dagens dato
            date = data.get("date")
            if not date:
                from datetime import date as dt 
                date = dt.today().isoformat()
            y_url = "https://api.exchangerate.host/" + date
            y_params = {"base": "USD", "symbols": "NOK,EUR,SEK,GBP"}
            y_r = requests.get(y_url, params=y_params, timeout=10)
            y_data = y_r.json()
            y_rates = y_data.get("rates", {})
            result = {}
            for symbol, price in rates.items():
                prev = y_rates.get(symbol)
                change = ((price - prev) / prev * 100) if prev else None
                signal = None
                if change is not None:
                    signal = "BUY" if change > 0 else "SELL"
                result[f"USD/{symbol}"] = {
                    "name": f"USD/{symbol}",
                    "last_price": price,
                    "change_percent": change,
                    "signal": signal
                }
            return result
        except Exception as e:
            print("Error fetching currency:", e)
            return {}

    @staticmethod
    def get_market_sentiment(stocks):
        """Get the current market sentiment"""
        signals = [d.get('signal') for d in stocks.values() if d.get('signal')]
        if not signals:
            return "Neutral"
        if signals.count('Buy') > signals.count('Sell'):
            return "Bullish"
        elif signals.count('Sell') > signals.count('Buy'):
            return "Bearish"
        else:
            return "Neutral"

    @staticmethod
    def get_ai_analysis_data():
        """Hent AI-basert analyse for utvalgte aksjer og kryptovalutaer."""
        # Dummy-data, bytt ut med ekte AI-analyse senere
        return {
            "EQNR.OL": {"name": "Equinor", "last_price": 300, "change_percent": 1.2, "signal": "Buy"},
            "NHY.OL": {"name": "Norsk Hydro", "last_price": 80, "change_percent": -0.5, "signal": "Hold"},
            "BTC": {"name": "Bitcoin", "last_price": 67000, "change_percent": 2.1, "signal": "Buy"},
            "AAPL": {"name": "Apple", "last_price": 190, "change_percent": 0.8, "signal": "Buy"},
        }

    @staticmethod
    def get_market_overview():
        """Returnerer samlet markedsoversikt for Oslo Børs, globale aksjer, krypto og valuta."""
        return {
            "oslo_stocks": DataService.get_oslo_bors_overview(),
            "global_stocks": DataService.get_global_stocks_overview(),
            "crypto": DataService.get_crypto_overview(),
            "currency": DataService.get_currency_overview()
        }

    @staticmethod
    def get_market_news(keywords="finance,stocks,market", days=3, max_articles=5):
        """
        Get recent market news from NewsAPI or return sample data
        """
        # Hvis NewsAPI ikke er tilgjengelig, bruk eksempeldata
        if not HAS_NEWSAPI:
            return DataService.get_sample_market_news()
        
        try:
            # Initialize NewsAPI with your API key
            api_key = os.environ.get('NEWS_API_KEY')
            if not api_key:
                # Fall back to sample data if no API key
                return DataService.get_sample_market_news()
                
            newsapi = NewsApiClient(api_key=api_key)
            
            # Calculate date range
            today = datetime.now()
            from_date = (today - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # Get news
            news_response = newsapi.get_everything(
                q=keywords,
                from_param=from_date,
                to=today.strftime('%Y-%m-%d'),
                language='en',
                sort_by='publishedAt',
                page_size=max_articles
            )
            
            # Format results
            if news_response['status'] == 'ok':
                articles = []
                for article in news_response['articles'][:max_articles]:
                    articles.append({
                        'title': article['title'],
                        'summary': article['description'],
                        'date': article['publishedAt'].split('T')[0],  # Format date
                        'source': article['source']['name'],
                        'url': article['url']
                    })
                return articles
            else:
                return DataService.get_sample_market_news()
        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return DataService.get_sample_market_news()

    @staticmethod
    def get_sample_market_news():
        """Return sample market news when API is unavailable"""
        return [
            {
                'title': 'Fed holder renten uendret',
                'summary': 'Den amerikanske sentralbanken holder styringsrenten uendret, men signaliserer mulige rentekutt senere i år.',
                'date': '2024-06-15',
                'source': 'Reuters'
            },
            {
                'title': 'Oljeprisen stiger på OPEC-nyheter',
                'summary': 'Oljeprisen stiger etter at OPEC+ kunngjorde at de vil opprettholde produksjonskutt ut året.',
                'date': '2024-06-14',
                'source': 'Bloomberg'
            },
            {
                'title': 'Teknologiaksjer leder oppgangen',
                'summary': 'Teknologiaksjer leder an i markedsoppgangen denne uken, drevet av positive resultater og AI-optimisme.',
                'date': '2024-06-13',
                'source': 'CNBC'
            }
        ]

    @staticmethod
    def get_currency_data():
        """Get currency exchange data"""
        try:
            # Prøv å hente data fra Yahoo Finance
            currencies = ['USDNOK=X', 'EURNOK=X', 'GBPNOK=X', 'JPYNOK=X', 'SEKNOK=X', 'DKKNOK=X']
            data = {}
            
            for currency in currencies:
                try:
                    # Prøv å hente data fra Yahoo Finance           
                    currency_data = DataService.get_stock_data(currency, period='2d')
                    if not currency_data.empty and len(currency_data) > 1:
                        last_price = float(currency_data['Close'].iloc[-1])
                        prev_price = float(currency_data['Close'].iloc[-2])
                        change = last_price - prev_price
                        change_percent = (change / prev_price) * 100 if prev_price else 0
                        
                        data[currency] = {
                            'ticker': currency,
                            'last_price': round(last_price, 4),
                            'change': round(change, 4),
                            'change_percent': round(change_percent, 2)
                        }
                except Exception as e:
                    print(f"Error getting data for {currency}: {str(e)}")
            
            # Hvis vi ikke fikk noen data, bruk demo-data
            if not data:
                raise Exception("No currency data available")
                
            return data
        except Exception as e:
            print(f"Error getting currency data: {str(e)}")
            # Fallback til demo-data
            return {
                'USDNOK=X': {'ticker': 'USDNOK=X', 'last_price': 10.5623, 'change': 0.0324, 'change_percent': 0.31},
                'EURNOK=X': {'ticker': 'EURNOK=X', 'last_price': 11.4389, 'change': -0.0215, 'change_percent': -0.19},
                'GBPNOK=X': {'ticker': 'GBPNOK=X', 'last_price': 13.5682, 'change': 0.0478, 'change_percent': 0.35},
                'JPYNOK=X': {'ticker': 'JPYNOK=X', 'last_price': 0.0712, 'change': -0.0008, 'change_percent': -1.11},
                'SEKNOK=X': {'ticker': 'SEKNOK=X', 'last_price': 1.0145, 'change': 0.0012, 'change_percent': 0.12},
                'DKKNOK=X': {'ticker': 'DKKNOK=X', 'last_price': 1.5321, 'change': -0.0043, 'change_percent': -0.28}
            }
    
    @staticmethod
    def get_crypto_data():
        """Get cryptocurrency data"""
        try:
            # Try to fetch data from Yahoo Finance
            cryptos = ['BTC-USD', 'ETH-USD', 'ADA-USD', 'SOL-USD', 'DOGE-USD']
            data = {}
            
            for crypto in cryptos:
                try:
                    crypto_data = DataService.get_stock_data(crypto, period='1d')
                    # Fix: Check if dataframe is empty properly
                    if not crypto_data.empty:
                        last_price = float(crypto_data['Close'].iloc[-1])
                        change = 0
                        change_percent = 0
                        if len(crypto_data) > 1:
                            prev_close = float(crypto_data['Close'].iloc[-2])
                            change = last_price - prev_close
                            change_percent = (change / prev_close) * 100
                        
                        data[crypto] = {
                            'last_price': round(last_price, 2),
                            'change': round(change, 2),
                            'change_percent': round(change_percent, 2)
                        }
                except Exception as e:
                    print(f"Error getting data for {crypto}: {str(e)}")
            
            # Return fallback data if no data was collected
            if not data:
                print("No crypto data available")
                # Return demo data
                return {
                    'BTC-USD': {'last_price': 65432.10, 'change': 876.54, 'change_percent': 1.35},
                    'ETH-USD': {'last_price': 3456.78, 'change': -123.45, 'change_percent': -3.45},
                    'ADA-USD': {'last_price': 1.23, 'change': 0.05, 'change_percent': 4.23},
                    'SOL-USD': {'last_price': 87.65, 'change': 3.21, 'change_percent': 3.8},
                    'DOGE-USD': {'last_price': 0.123, 'change': -0.002, 'change_percent': -1.6}
                }
            
            return data
        except Exception as e:
            print(f"Error getting crypto data: {str(e)}")
            # Return demo data in case of error
            return {
                'BTC-USD': {'last_price': 65432.10, 'change': 876.54, 'change_percent': 1.35},
                'ETH-USD': {'last_price': 3456.78, 'change': -123.45, 'change_percent': -3.45},
                'ADA-USD': {'last_price': 1.23, 'change': 0.05, 'change_percent': 4.23},
                'SOL-USD': {'last_price': 87.65, 'change': 3.21, 'change_percent': 3.8},
                'DOGE-USD': {'last_price': 0.123, 'change': -0.002, 'change_percent': -1.6}
            }
    
    @staticmethod
    def get_popular_stocks(sort_by='name'):
        """Get popular stocks data with sorting"""
        try:
            # Extended list of Oslo Børs stocks
            oslo_tickers = [
                'EQNR.OL', 'DNB.OL', 'NHY.OL', 'YAR.OL', 'TEL.OL', 
                'AKER.OL', 'AKERBP.OL', 'MOWI.OL', 'ORK.OL', 'SALM.OL',
                'TGS.OL', 'SUBC.OL', 'AKSO.OL', 'STB.OL', 'KOG.OL', 
                'ELK.OL', 'NOD.OL', 'SCATC.OL', 'BWLPG.OL', 'GOGL.OL',
                'ODF.OL', 'FRO.OL', 'HAFNI.OL', 'MPC.OL', 'SASNO.OL'
            ]
            
            stocks = []
            for ticker in oslo_tickers:
                try:
                    stock_data = DataService.get_stock_data(ticker, period='1d')
                    if not stock_data.empty:
                        # Get company name
                        ticker_obj = yf.Ticker(ticker)
                        try:
                            name = ticker_obj.info.get('shortName', ticker)
                            # Clean up name if it contains date information
                            if isinstance(name, str) and 'dtype:' in name:
                                name = name.split(',')[0]
                        except:
                            name = ticker
                            
                        # Get last price and change
                        last_price = float(stock_data['Close'].iloc[-1])
                        change = 0
                        change_percent = 0
                        
                        if len(stock_data) > 1:
                            prev_close = float(stock_data['Close'].iloc[-2])
                            change = last_price - prev_close
                            change_percent = (change / prev_close) * 100
                        
                        # Get volume and format it to millions
                        volume = float(stock_data['Volume'].iloc[-1]) / 1000000 if 'Volume' in stock_data.columns else None
                        
                        # Estimate market cap (very rough calculation)
                        market_cap = None
                        if hasattr(ticker_obj, 'info') and 'marketCap' in ticker_obj.info:
                            market_cap = float(ticker_obj.info['marketCap']) / 1000000000  # Convert to billions
                        
                        stocks.append({
                            'ticker': ticker,
                            'name': name,
                            'price': round(last_price, 2),
                            'change': round(change, 2),
                            'change_percent': round(change_percent, 2),
                            'volume': round(volume, 1) if volume is not None else None,
                            'market_cap': round(market_cap, 1) if market_cap is not None else None
                        })
                except Exception as e:
                    print(f"Error getting data for {ticker}: {str(e)}")
            
            # If we didn't get any stocks, return demo data
            if not stocks:
                print("Using demo stock data")
                return [
                    {'ticker': 'EQNR.OL', 'name': 'Equinor', 'price': 342.55, 'change': 5.60, 'change_percent': 1.66, 'volume': 3.2, 'market_cap': 1089.5},
                    {'ticker': 'DNB.OL', 'name': 'DNB Bank', 'price': 212.80, 'change': -1.20, 'change_percent': -0.56, 'volume': 1.5, 'market_cap': 329.8},
                    {'ticker': 'NHY.OL', 'name': 'Norsk Hydro', 'price': 65.28, 'change': 0.42, 'change_percent': 0.65, 'volume': 8.3, 'market_cap': 134.5},
                    {'ticker': 'YAR.OL', 'name': 'Yara International', 'price': 345.10, 'change': 7.30, 'change_percent': 2.16, 'volume': 0.9, 'market_cap': 88.7},
                    {'ticker': 'TEL.OL', 'name': 'Telenor', 'price': 125.90, 'change': -0.60, 'change_percent': -0.47, 'volume': 1.2, 'market_cap': 176.3}
                ]
            
            # Sort the stocks
            if sort_by == 'price':
                stocks.sort(key=lambda x: x.get('price', 0) or 0, reverse=True)
            elif sort_by == 'change':
                stocks.sort(key=lambda x: x.get('change_percent', 0) or 0, reverse=True)
            elif sort_by == 'volume':
                stocks.sort(key=lambda x: x.get('volume', 0) or 0, reverse=True)
            else:  # sort by name
                stocks.sort(key=lambda x: x.get('name', '') or '')
                
            return stocks
        except Exception as e:
            print(f"Error getting popular stocks: {str(e)}")
            # Return backup demo data
            return [
                {'ticker': 'EQNR.OL', 'name': 'Equinor', 'price': 342.55, 'change': 5.60, 'change_percent': 1.66, 'volume': 3.2, 'market_cap': 1089.5},
                {'ticker': 'DNB.OL', 'name': 'DNB Bank', 'price': 212.80, 'change': -1.20, 'change_percent': -0.56, 'volume': 1.5, 'market_cap': 329.8},
                {'ticker': 'NHY.OL', 'name': 'Norsk Hydro', 'price': 65.28, 'change': 0.42, 'change_percent': 0.65, 'volume': 8.3, 'market_cap': 134.5},
                {'ticker': 'YAR.OL', 'name': 'Yara International', 'price': 345.10, 'change': 7.30, 'change_percent': 2.16, 'volume': 0.9, 'market_cap': 88.7},
                {'ticker': 'TEL.OL', 'name': 'Telenor', 'price': 125.90, 'change': -0.60, 'change_percent': -0.47, 'volume': 1.2, 'market_cap': 176.3}
            ]