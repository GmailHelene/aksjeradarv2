import yfinance as yf
from pycoingecko import CoinGeckoAPI
from forex_python.converter import CurrencyRates
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Initialize API clients
cg = CoinGeckoAPI()
cr = CurrencyRates()

# Define stock tickers
OSLO_BORS_TICKERS = [
    'EQNR.OL', 'DNB.OL', 'AKSO.OL', 'YAR.OL', 'TEL.OL',
    'MOWI.OL', 'NHY.OL', 'ORK.OL', 'SALM.OL', 'BWLPG.OL',
    'AKRBP.OL', 'SUBC.OL', 'SCHA.OL', 'GJF.OL', 'KONGB.OL'
]

GLOBAL_TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META',
    'NVDA', 'TSLA', 'JPM', 'V', 'WMT',
    'JNJ', 'PG', 'MA', 'UNH', 'HD'
]

class DataService:
    @staticmethod
    def get_stock_data(ticker, period='1d', interval='1m'):
        """Get real stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            return df
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def get_oslo_bors_overview(limit=20):
        """Get overview of Oslo Børs stocks with guaranteed fields"""
        stocks = []
        try:
            for ticker in OSLO_BORS_TICKERS[:limit]:
                try:
                    stock_data = DataService.get_stock_data(ticker)
                    info = DataService.get_real_stock_info(ticker)
                    
                    if stock_data.empty and not info:
                        continue
                        
                    stock = {
                        'ticker': ticker,
                        'name': info.get('shortName', ticker),
                        'price': info.get('regularMarketPrice', 0.0) if stock_data.empty else stock_data['Close'].iloc[-1],
                        'change': info.get('regularMarketChange', 0.0) if stock_data.empty else stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0],
                        'change_percent': info.get('regularMarketChangePercent', 0.0) if stock_data.empty else ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0] * 100),
                        'volume': info.get('volume', 0) if stock_data.empty else int(stock_data['Volume'].iloc[-1]),
                        'market_cap': info.get('marketCap', 0)
                    }
                    
                    # Format numbers properly
                    stock['price'] = round(float(stock['price']), 2)
                    stock['change'] = round(float(stock['change']), 2)
                    stock['change_percent'] = round(float(stock['change_percent']), 2)
                    stock['volume'] = int(stock['volume'])
                    stock['market_cap'] = int(stock['market_cap'])
                    
                    stocks.append(stock)
                    
                except Exception as e:
                    logger.error(f"Error processing {ticker}: {str(e)}")
                    continue
                
        except Exception as e:
            logger.error(f"Error getting Oslo Børs overview: {str(e)}")
        
        return stocks

    @staticmethod
    def get_global_stocks_overview(limit=20):
        """Get overview of global stocks with guaranteed fields"""
        stocks = []
        try:
            for ticker in GLOBAL_TICKERS[:limit]:
                try:
                    stock_data = DataService.get_stock_data(ticker)
                    info = DataService.get_real_stock_info(ticker)
                    
                    if stock_data.empty and not info:
                        continue
                        
                    stock = {
                        'ticker': ticker,
                        'name': info.get('shortName', ticker),
                        'price': info.get('regularMarketPrice', 0.0) if stock_data.empty else stock_data['Close'].iloc[-1],
                        'change': info.get('regularMarketChange', 0.0) if stock_data.empty else stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0],
                        'change_percent': info.get('regularMarketChangePercent', 0.0) if stock_data.empty else ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / stock_data['Close'].iloc[0] * 100),
                        'volume': info.get('volume', 0) if stock_data.empty else int(stock_data['Volume'].iloc[-1]),
                        'market_cap': info.get('marketCap', 0)
                    }
                    
                    # Format numbers properly
                    stock['price'] = round(float(stock['price']), 2)
                    stock['change'] = round(float(stock['change']), 2)
                    stock['change_percent'] = round(float(stock['change_percent']), 2)
                    stock['volume'] = int(stock['volume'])
                    stock['market_cap'] = int(stock['market_cap'])
                    
                    stocks.append(stock)
                    
                except Exception as e:
                    logger.error(f"Error processing {ticker}: {str(e)}")
                    continue
                
        except Exception as e:
            logger.error(f"Error getting global stocks overview: {str(e)}")
        
        return stocks

    @staticmethod
    def get_crypto_list(page=1, per_page=100):
        """Get real cryptocurrency data with guaranteed fields"""
        try:
            cryptos = cg.get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=per_page,
                page=page,
                sparkline=False
            )
            
            formatted_cryptos = []
            for idx, crypto in enumerate(cryptos, start=(page-1)*per_page + 1):
                formatted_cryptos.append({
                    "rank": idx,
                    "name": crypto.get('name', f"Crypto {idx}"),
                    "symbol": crypto.get('symbol', '').upper() or f"CRYPTO{idx}",
                    "image": crypto.get('image', '/static/images/default-crypto.png'),
                    "current_price": round(float(crypto.get('current_price', 0.0)), 2),
                    "price_change_percentage_24h": round(float(crypto.get('price_change_percentage_24h', 0.0)), 2),
                    "market_cap": int(crypto.get('market_cap', 0)),
                    "total_volume": int(crypto.get('total_volume', 0)),
                    "circulating_supply": int(crypto.get('circulating_supply', 0))
                })
            
            return formatted_cryptos
        except Exception as e:
            logger.error(f"Error fetching cryptocurrency data: {str(e)}")
            return []

    @staticmethod
    def get_currency_list():
        """Get real currency exchange rates with guaranteed fields"""
        try:
            currencies = [
                'EUR', 'GBP', 'JPY', 'CHF', 'AUD', 'CAD', 'NOK', 'SEK', 'DKK', 
                'NZD', 'SGD', 'HKD', 'CNY', 'INR', 'BRL', 'ZAR'
            ]
            base = 'USD'  # Always use USD as base for consistency
            
            rates = []
            for curr in currencies:
                try:
                    rate = cr.get_rate(base, curr)
                    # Get yesterday's rate for comparison
                    yesterday = datetime.now() - timedelta(days=1)
                    prev_rate = cr.get_rate(base, curr, yesterday)
                    
                    if not rate or not prev_rate:
                        continue
                        
                    change = rate - prev_rate
                    change_percent = (change / prev_rate) * 100

                    rates.append({
                        'symbol': curr,
                        'name': f"{curr}/{base}",
                        'rate': round(rate, 4),
                        'change': round(change, 4),
                        'change_percent': round(change_percent, 2),
                        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                except Exception as e:
                    logger.error(f"Error fetching rate for {curr}: {str(e)}")
                    continue

            return rates
        except Exception as e:
            logger.error(f"Error fetching currency rates: {str(e)}")
            return []

    @staticmethod
    def get_real_stock_info(ticker):
        """Get real stock info from Yahoo Finance"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'ticker': ticker,
                'shortName': info.get('shortName', ticker),
                'longName': info.get('longName', info.get('shortName', ticker)),
                'sector': info.get('sector', 'Diverse'),
                'regularMarketPrice': info.get('regularMarketPrice', 0.0),
                'marketCap': info.get('marketCap', 0),
                'volume': info.get('volume', 0),
                'country': info.get('country', "Norway" if ".OL" in ticker else "USA"),
                'currency': info.get('currency', 'NOK' if '.OL' in ticker else 'USD')
            }
            
        except Exception as e:
            logger.error(f"Error fetching info for {ticker}: {str(e)}")
            return None

    @staticmethod
    def get_market_overview():
        """Get overview of different markets for the dashboard"""
        try:
            # Get a few top stocks from each market
            oslo_stocks = DataService.get_oslo_bors_overview(limit=5)
            global_stocks = DataService.get_global_stocks_overview(limit=5)
            cryptos = DataService.get_crypto_list(per_page=5)
            currencies = DataService.get_currency_list()[:5] if DataService.get_currency_list() else []
            
            return {
                'oslo_stocks': oslo_stocks,
                'global_stocks': global_stocks,
                'cryptos': cryptos,
                'currencies': currencies
            }
        except Exception as e:
            logger.error(f"Error getting market overview: {str(e)}")
            return {
                'oslo_stocks': [],
                'global_stocks': [],
                'cryptos': [],
                'currencies': []
            }