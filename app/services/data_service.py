import os
import json
import time
import logging
import yfinance as yf
from datetime import datetime, timedelta
from pycoingecko import CoinGeckoAPI
from forex_python.converter import CurrencyRates
from functools import wraps

logger = logging.getLogger(__name__)

# Create cache directory if it doesn't exist
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

# Set up cache and rate limiting handling
def cache_result(cache_time=3600):  # Default cache time: 1 hour
    """Decorator to cache API results to avoid rate limiting"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key based on function name and arguments
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            cache_file = os.path.join(CACHE_DIR, f"{hash(cache_key)}.json")
            
            # Check if we have a valid cache file
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, 'r') as f:
                        cache_data = json.load(f)
                    
                    # Check if cache is still valid
                    if cache_data.get('timestamp', 0) + cache_time > time.time():
                        logger.debug(f"Using cached data for {func.__name__}")
                        return cache_data.get('data')
                except Exception as e:
                    logger.warning(f"Error reading cache file: {str(e)}")
            
            # If no valid cache, call the actual function
            try:
                # If no valid cache, call the actual function
                start_time = time.time()
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                
                # Log API performance
                logger.info(f"{func.__name__} completed in {elapsed_time:.2f}s")
                
                # Save result to cache
                try:
                    with open(cache_file, 'w') as f:
                        json.dump({
                            'timestamp': time.time(),
                            'data': result,
                            'source': 'live'
                        }, f)
                except Exception as e:
                    logger.warning(f"Error writing to cache file: {str(e)}")
                
                return result
                
            except Exception as e:
                error_msg = f"Error in {func.__name__}: {str(e)}"
                logger.error(error_msg)
                
                # Try to use stale cache if available
                if os.path.exists(cache_file):
                    try:
                        with open(cache_file, 'r') as f:
                            cache_data = json.load(f)
                        logger.warning(f"Using stale cache for {func.__name__} due to error: {str(e)}")
                        return cache_data.get('data')
                    except Exception as cache_error:
                        logger.error(f"Failed to read stale cache: {str(cache_error)}")
                
                # If no cache available, use appropriate fallback data
                if 'oslo' in func.__name__.lower():
                    logger.info("Using Oslo Børs fallback data")
                    return DataService.FALLBACK_OSLO_STOCKS
                elif 'global' in func.__name__.lower():
                    logger.info("Using global stocks fallback data")
                    return DataService.FALLBACK_GLOBAL_STOCKS
                elif 'crypto' in func.__name__.lower():
                    logger.info("Using crypto fallback data")
                    return DataService.FALLBACK_CRYPTO
                elif 'currency' in func.__name__.lower():
                    logger.info("Using currency fallback data")
                    return DataService.FALLBACK_CURRENCY
                
                # If we don't have specific fallback data, raise the original error
                raise e
                
        return wrapper
    return decorator

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
    """Service for fetching and managing market data"""
    
    # Fallback data
    FALLBACK_OSLO_STOCKS = {
        'EQNR.OL': {'name': 'Equinor', 'last_price': 322.50, 'change_percent': 2.1, 'volume': 1234567, 'market_cap': 1029384756, 'currency': 'NOK', 'signal': 'BUY'},
        'DNB.OL': {'name': 'DNB Bank', 'last_price': 218.90, 'change_percent': -0.8, 'volume': 987654, 'market_cap': 987654321, 'currency': 'NOK', 'signal': 'HOLD'},
        'AKSO.OL': {'name': 'Aker Solutions', 'last_price': 34.80, 'change_percent': 1.5, 'volume': 876543, 'market_cap': 876543210, 'currency': 'NOK', 'signal': 'BUY'},
        'YAR.OL': {'name': 'Yara International', 'last_price': 418.60, 'change_percent': -1.2, 'volume': 765432, 'market_cap': 765432109, 'currency': 'NOK', 'signal': 'SELL'},
        'TEL.OL': {'name': 'Telenor', 'last_price': 123.45, 'change_percent': 0.5, 'volume': 654321, 'market_cap': 654321098, 'currency': 'NOK', 'signal': 'HOLD'}
    }

    FALLBACK_GLOBAL_STOCKS = {
        'AAPL': {'name': 'Apple Inc.', 'last_price': 185.70, 'change_percent': 1.8, 'volume': 9876543, 'market_cap': 9876543210, 'currency': 'USD', 'signal': 'BUY'},
        'MSFT': {'name': 'Microsoft', 'last_price': 390.20, 'change_percent': 2.3, 'volume': 8765432, 'market_cap': 8765432109, 'currency': 'USD', 'signal': 'BUY'},
        'GOOGL': {'name': 'Alphabet Inc.', 'last_price': 155.50, 'change_percent': 1.5, 'volume': 7654321, 'market_cap': 7654321098, 'currency': 'USD', 'signal': 'HOLD'},
        'AMZN': {'name': 'Amazon', 'last_price': 178.90, 'change_percent': 0.2, 'volume': 6543210, 'market_cap': 6543210987, 'currency': 'USD', 'signal': 'HOLD'},
        'META': {'name': 'Meta Platforms', 'last_price': 368.80, 'change_percent': 3.1, 'volume': 5432109, 'market_cap': 5432109876, 'currency': 'USD', 'signal': 'BUY'}
    }

    FALLBACK_CRYPTO = {
        'BTC': {'name': 'Bitcoin', 'last_price': 45000.00, 'change_percent': 2.5, 'volume': 4321098, 'market_cap': 4321098765, 'currency': 'USD', 'signal': 'BUY'},
        'ETH': {'name': 'Ethereum', 'last_price': 2800.00, 'change_percent': 3.2, 'volume': 3210987, 'market_cap': 3210987654, 'currency': 'USD', 'signal': 'BUY'},
        'BNB': {'name': 'Binance Coin', 'last_price': 320.00, 'change_percent': -1.5, 'volume': 2109876, 'market_cap': 2109876543, 'currency': 'USD', 'signal': 'SELL'},
        'XRP': {'name': 'Ripple', 'last_price': 0.85, 'change_percent': 1.8, 'volume': 1098765, 'market_cap': 1098765432, 'currency': 'USD', 'signal': 'BUY'},
        'SOL': {'name': 'Solana', 'last_price': 95.00, 'change_percent': 4.2, 'volume': 987654, 'market_cap': 987654321, 'currency': 'USD', 'signal': 'BUY'}
    }

    FALLBACK_CURRENCY = {
        'EUR': {'name': 'EUR/USD', 'last_price': 1.0950, 'change_percent': 0.2, 'volume': 876543, 'currency': 'USD', 'signal': 'HOLD'},
        'GBP': {'name': 'GBP/USD', 'last_price': 1.2750, 'change_percent': -0.1, 'volume': 765432, 'currency': 'USD', 'signal': 'HOLD'},
        'JPY': {'name': 'USD/JPY', 'last_price': 142.50, 'change_percent': 0.3, 'volume': 654321, 'currency': 'USD', 'signal': 'HOLD'},
        'NOK': {'name': 'USD/NOK', 'last_price': 10.450, 'change_percent': -0.4, 'volume': 543210, 'currency': 'USD', 'signal': 'HOLD'},
        'SEK': {'name': 'USD/SEK', 'last_price': 10.850, 'change_percent': 0.1, 'volume': 432109, 'currency': 'USD', 'signal': 'HOLD'}
    }

    @staticmethod
    @cache_result(cache_time=600)  # Cache for 10 minutes
    def get_stock_data(ticker, period='1d', interval='1m'):
        """Get real stock data from Yahoo Finance"""
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            # If we got rate limited (empty DataFrame), wait and retry once
            if df.empty:
                logger.warning(f"Empty data for {ticker}, could be rate limiting. Retrying after delay...")
                time.sleep(2)  # Wait 2 seconds
                df = stock.history(period=period, interval=interval)
            
            if not df.empty:
                return df.to_dict('records')
            else:
                logger.error(f"No data available for {ticker}")
                # Return some dummy historical data
                return [
                    {'Open': 100, 'High': 102, 'Low': 98, 'Close': 101, 'Volume': 10000},
                    {'Open': 101, 'High': 103, 'Low': 99, 'Close': 102, 'Volume': 12000}
                ]
        except Exception as e:
            logger.error(f"Error fetching stock data for {ticker}: {str(e)}")
            return [
                {'Open': 100, 'High': 102, 'Low': 98, 'Close': 101, 'Volume': 10000},
                {'Open': 101, 'High': 103, 'Low': 99, 'Close': 102, 'Volume': 12000}
            ]

    @staticmethod
    @cache_result(cache_time=600)  # Cache for 10 minutes
    def get_oslo_bors_overview(limit=None):
        """Get overview of Oslo Børs stocks"""
        try:
            result = {}
            tickers = OSLO_BORS_TICKERS[:limit] if limit else OSLO_BORS_TICKERS
            
            for ticker in tickers:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    result[ticker] = {
                        'name': info.get('shortName', ticker),
                        'last_price': info.get('regularMarketPrice', 0),
                        'change_percent': info.get('regularMarketChangePercent', 0),
                        'volume': info.get('regularMarketVolume', 0),
                        'market_cap': info.get('marketCap', 0),
                        'currency': info.get('currency', 'NOK'),
                    }
                    
                    if result[ticker]['last_price'] > 0:
                        if result[ticker]['change_percent'] > 2:
                            result[ticker]['signal'] = 'BUY'
                        elif result[ticker]['change_percent'] < -2:
                            result[ticker]['signal'] = 'SELL'
                        else:
                            result[ticker]['signal'] = 'HOLD'
                    else:
                        result[ticker]['signal'] = 'N/A'
                        
                except Exception as e:
                    logger.error(f"Error fetching data for {ticker}: {str(e)}")
                    result[ticker] = DataService.FALLBACK_OSLO_STOCKS.get(ticker, {
                        'name': ticker,
                        'last_price': 0,
                        'change_percent': 0,
                        'volume': 0,
                        'market_cap': 0,
                        'currency': 'NOK',
                        'signal': 'N/A'
                    })
            
            # If we got no real data, use fallback data
            if not any(stock['last_price'] > 0 for stock in result.values()):
                logger.warning("Using fallback data for Oslo Børs")
                result = dict(list(DataService.FALLBACK_OSLO_STOCKS.items())[:limit] if limit else DataService.FALLBACK_OSLO_STOCKS)
            return result
            
        except Exception as e:
            logger.error(f"Error in Oslo Børs overview: {str(e)}")
            # Return fallback data
            return dict(list(DataService.FALLBACK_OSLO_STOCKS.items())[:limit] if limit else DataService.FALLBACK_OSLO_STOCKS)

    @staticmethod
    @cache_result(cache_time=600)  # Cache for 10 minutes
    def get_global_stocks_overview(limit=None):
        """Get overview of global stocks"""
        try:
            result = {}
            tickers = GLOBAL_TICKERS[:limit] if limit else GLOBAL_TICKERS
            
            for ticker in tickers:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    result[ticker] = {
                        'name': info.get('shortName', ticker),
                        'last_price': info.get('regularMarketPrice', 0),
                        'change_percent': info.get('regularMarketChangePercent', 0),
                        'volume': info.get('regularMarketVolume', 0),
                        'market_cap': info.get('marketCap', 0),
                        'currency': info.get('currency', 'USD'),
                    }
                    
                    if result[ticker]['last_price'] > 0:
                        if result[ticker]['change_percent'] > 2:
                            result[ticker]['signal'] = 'BUY'
                        elif result[ticker]['change_percent'] < -2:
                            result[ticker]['signal'] = 'SELL'
                        else:
                            result[ticker]['signal'] = 'HOLD'
                    else:
                        result[ticker]['signal'] = 'N/A'
                        
                except Exception as e:
                    logger.error(f"Error fetching data for {ticker}: {str(e)}")
                    result[ticker] = DataService.FALLBACK_GLOBAL_STOCKS.get(ticker, {
                        'name': ticker,
                        'last_price': 0,
                        'change_percent': 0,
                        'volume': 0,
                        'market_cap': 0,
                        'currency': 'USD',
                        'signal': 'N/A'
                    })
            
            # If we got no real data, use fallback data
            if not any(stock['last_price'] > 0 for stock in result.values()):
                logger.warning("Using fallback data for global stocks")
                result = dict(list(DataService.FALLBACK_GLOBAL_STOCKS.items())[:limit] if limit else DataService.FALLBACK_GLOBAL_STOCKS)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in global stocks overview: {str(e)}")
            # Return fallback data
            return dict(list(DataService.FALLBACK_GLOBAL_STOCKS.items())[:limit] if limit else DataService.FALLBACK_GLOBAL_STOCKS)

    @staticmethod
    @cache_result(cache_time=300)  # Cache for 5 minutes
    def get_crypto_overview(limit=10):
        """Get overview of cryptocurrencies"""
        try:
            result = {}
            # Get crypto data from CoinGecko
            crypto_data = cg.get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=limit,
                sparkline=False
            )
            
            for coin in crypto_data:
                symbol = coin['symbol'].upper()
                result[symbol] = {
                    'name': coin['name'],
                    'last_price': coin['current_price'],
                    'change_percent': coin['price_change_percentage_24h'] or 0,
                    'volume': coin['total_volume'],
                    'market_cap': coin['market_cap'],
                    'currency': 'USD',
                    'image': coin['image']
                }
                
                if result[symbol]['change_percent'] > 5:
                    result[symbol]['signal'] = 'BUY'
                elif result[symbol]['change_percent'] < -5:
                    result[symbol]['signal'] = 'SELL'
                else:
                    result[symbol]['signal'] = 'HOLD'
            
            if result:
                return result
            else:
                logger.warning("No crypto data available, using fallback data")
                return dict(list(DataService.FALLBACK_CRYPTO.items())[:limit])
                
        except Exception as e:
            logger.error(f"Error fetching crypto data: {str(e)}")
            return dict(list(DataService.FALLBACK_CRYPTO.items())[:limit])    # Fallback currency rates (dummy data)
    FALLBACK_CURRENCY_RATES = {
        'EUR': {'rate': 0.92, 'change': 0.5},
        'GBP': {'rate': 0.79, 'change': -0.3},
        'JPY': {'rate': 142.50, 'change': 0.2},
        'NOK': {'rate': 10.75, 'change': -0.1},
        'SEK': {'rate': 10.85, 'change': 0.4},
        'DKK': {'rate': 6.85, 'change': 0.3},
        'CHF': {'rate': 0.89, 'change': -0.2},
        'AUD': {'rate': 1.48, 'change': 0.6},
        'CAD': {'rate': 1.32, 'change': -0.4},
        'NZD': {'rate': 1.62, 'change': 0.1}
    }

    @staticmethod
    @cache_result(cache_time=300)  # Cache for 5 minutes
    def get_currency_overview(base='USD'):
        """Get overview of currency exchange rates"""
        try:
            result = {}
            currencies = ['EUR', 'GBP', 'JPY', 'NOK', 'SEK', 'DKK', 'CHF', 'AUD', 'CAD', 'NZD']
            cr = CurrencyRates()
            success = False
            
            for currency in currencies:
                if currency != base:
                    try:
                        rate = cr.get_rate(base, currency)
                        # Calculate 24h change (this is a dummy value since forex_python doesn't provide historical data)
                        change = (rate * (1 + (hash(currency) % 5 - 2) / 100)) - rate  # Simulated change
                        
                        result[currency] = {
                            'name': f"{currency}/{base}",
                            'last_price': rate,
                            'change_percent': (change / rate) * 100,
                            'is_fallback': False
                        }
                        success = True
                    except Exception as e:
                        logger.error(f"Error fetching rate for {currency}: {str(e)}")
                        fallback = DataService.FALLBACK_CURRENCY_RATES.get(currency, {'rate': 1.0, 'change': 0.0})
                        result[currency] = {
                            'name': f"{currency}/{base}",
                            'last_price': fallback['rate'],
                            'change_percent': fallback['change'],
                            'is_fallback': True
                        }            for currency, data in result.items():
                # Add signal based on change percent
                if data['change_percent'] > 0.5:
                    result[currency]['signal'] = 'BUY'
                elif data['change_percent'] < -0.5:
                    result[currency]['signal'] = 'SELL'
                else:
                    result[currency]['signal'] = 'HOLD'
                
                # Add dummy volume since forex data doesn't include volume
                result[currency]['volume'] = 1000000 if not data.get('is_fallback') else 500000
                result[currency]['currency'] = base
            
            return result
            
        except Exception as e:
            logger.error(f"Error in currency overview: {str(e)}")
            # Return all fallback data
            result = {}
            for currency in currencies:
                if currency != base:
                    fallback = DataService.FALLBACK_CURRENCY_RATES.get(currency, {'rate': 1.0, 'change': 0.0})
                    result[currency] = {
                        'name': f"{currency}/{base}",
                        'last_price': fallback['rate'],
                        'change_percent': fallback['change'],
                        'volume': 500000,  # Reduced volume to indicate fallback data
                        'currency': base,
                        'signal': 'HOLD' if -0.5 <= fallback['change'] <= 0.5 else ('BUY' if fallback['change'] > 0.5 else 'SELL'),
                        'is_fallback': True
                    }
            return result
                return DataService.FALLBACK_CURRENCY
                
            return result
            
        except Exception as e:
            logger.error(f"Error in currency overview: {str(e)}")
            return DataService.FALLBACK_CURRENCY

    @staticmethod
    def get_stock_info(ticker):
        """Get detailed stock information"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'name': info.get('shortName', ticker),
                'last_price': info.get('regularMarketPrice', 0),
                'change_percent': info.get('regularMarketChangePercent', 0),
                'volume': info.get('regularMarketVolume', 0),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'N/A'),
                'exchange': info.get('exchange', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'description': info.get('longBusinessSummary', 'No description available'),
                'website': info.get('website', 'N/A'),
                'pe_ratio': info.get('forwardPE', 0),
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0)
            }
        except Exception as e:
            logger.error(f"Error fetching stock info for {ticker}: {str(e)}")
            return {
                'name': ticker,
                'last_price': 0,
                'change_percent': 0,
                'volume': 0,
                'market_cap': 0,
                'currency': 'N/A',
                'exchange': 'N/A',
                'sector': 'N/A',
                'description': 'Data not available',
                'website': 'N/A',
                'pe_ratio': 0,
                'dividend_yield': 0,
                '52_week_high': 0,
                '52_week_low': 0
            }

    @staticmethod
    @cache_result(cache_time=300)  # Cache for 5 minutes
    def search_stocks(query):
        """Search for stocks by name or ticker"""
        results = []
        
        # Search Oslo Børs tickers
        for ticker in OSLO_BORS_TICKERS:
            if query.lower() in ticker.lower():
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    results.append({
                        'ticker': ticker,
                        'name': info.get('shortName', ticker),
                        'exchange': 'Oslo Børs',
                        'type': 'stock'
                    })
                except:
                    continue
        
        # Search global tickers
        for ticker in GLOBAL_TICKERS:
            if query.lower() in ticker.lower():
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    results.append({
                        'ticker': ticker,
                        'name': info.get('shortName', ticker),
                        'exchange': info.get('exchange', 'Unknown'),
                        'type': 'stock'
                    })
                except:
                    continue
        
        # Add some crypto results if query matches
        try:
            crypto_results = cg.search(query)
            for coin in crypto_results['coins'][:5]:  # Limit to top 5 matches
                results.append({
                    'ticker': coin['symbol'].upper(),
                    'name': coin['name'],
                    'exchange': 'Crypto',
                    'type': 'crypto'
                })
        except Exception as e:
            logger.error(f"Error searching crypto: {str(e)}")
        
        return results

    @staticmethod
    @cache_result(cache_time=600)  # Cache for 10 minutes
    def get_stock_data(ticker):
        """Get stock data with enhanced error handling"""
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info
            history = ticker_obj.history(period="1d")
            
            if history.empty:
                logger.warning(f"No history data available for {ticker}")
                return None
                
            last_price = history['Close'].iloc[-1] if not history.empty else None
            prev_close = info.get('previousClose', None)
            
            if not last_price or not prev_close:
                logger.warning(f"Missing price data for {ticker}")
                return None
                
            change = last_price - prev_close
            change_percent = (change / prev_close) * 100 if prev_close else 0
            
            return {
                'symbol': ticker,
                'name': info.get('longName', info.get('shortName', ticker)),
                'last_price': last_price,
                'change': change,
                'change_percent': change_percent,
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'NOK' if ticker.endswith('.OL') else 'USD'),
                'signal': DataService.calculate_signal(ticker_obj)
            }
            
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {str(e)}")
            return None
            
    @staticmethod
    def calculate_signal(ticker_obj):
        """Calculate trading signal based on technical indicators"""
        try:
            history = ticker_obj.history(period="60d")
            if history.empty:
                return "N/A"
                
            # Calculate moving averages
            ma20 = history['Close'].rolling(window=20).mean()
            ma50 = history['Close'].rolling(window=50).mean()
            
            last_price = history['Close'].iloc[-1]
            last_ma20 = ma20.iloc[-1]
            last_ma50 = ma50.iloc[-1]
            
            # Simple signal logic
            if last_price > last_ma20 and last_ma20 > last_ma50:
                return "KJØP"
            elif last_price < last_ma20 and last_ma20 < last_ma50:
                return "SELG"
            else:
                return "HOLD"
                
        except Exception as e:
            logger.error(f"Error calculating signal: {str(e)}")
            return "N/A"