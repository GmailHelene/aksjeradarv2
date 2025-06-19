import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Define some constants for demo data
OSLO_BORS_TICKERS = [
    "EQNR.OL", "DNB.OL", "TEL.OL", "YAR.OL", "NHY.OL", "AKSO.OL", 
    "MOWI.OL", "ORK.OL", "SALM.OL", "AKERBP.OL"
]

GLOBAL_TICKERS = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA", 
    "JPM", "BAC", "JNJ"
]

class DataService:
    @staticmethod
    def get_stock_data(ticker, period='1mo'):
        """Get historical stock data for a ticker"""
        try:
            # For demo, generate some random data
            end_date = datetime.now()
            
            if period == '1d':
                start_date = end_date - timedelta(days=1)
                periods = 24
            elif period == '5d':
                start_date = end_date - timedelta(days=5)
                periods = 5 * 8
            elif period == '1mo':
                start_date = end_date - timedelta(days=30)
                periods = 30
            elif period == '1y':
                start_date = end_date - timedelta(days=365)
                periods = 365
            else:
                start_date = end_date - timedelta(days=30)
                periods = 30
            
            # Create date range
            date_range = pd.date_range(start=start_date, end=end_date, periods=periods)
            
            # Generate random price data
            base_price = 100 + random.random() * 900  # Random starting price between 100 and 1000
            
            # Add some randomness but maintain a trend
            prices = np.random.normal(0, 1, len(date_range))
            prices = np.cumsum(prices)  # Cumulative sum to create a random walk
            # Scale prices and add to base price
            prices = (prices - min(prices)) / (max(prices) - min(prices)) * base_price * 0.2 + base_price
            
            # Generate volume data
            volumes = np.random.randint(100000, 10000000, len(date_range))
            
            # Create DataFrame
            df = pd.DataFrame({
                'Open': prices * 0.99,
                'High': prices * 1.02,
                'Low': prices * 0.98,
                'Close': prices,
                'Volume': volumes
            }, index=date_range)
            
            return df
        except Exception as e:
            print(f"Error fetching data for {ticker}: {str(e)}")
            return pd.DataFrame()
    
    @staticmethod
    def get_stock_info(ticker):
        """Get basic info for a stock"""
        try:
            # For demo, return mock data
            company_names = {
                "EQNR.OL": "Equinor",
                "DNB.OL": "DNB Bank",
                "TEL.OL": "Telenor",
                "YAR.OL": "Yara International",
                "NHY.OL": "Norsk Hydro",
                "AKSO.OL": "Aker Solutions",
                "MOWI.OL": "Mowi",
                "ORK.OL": "Orkla",
                "SALM.OL": "SalMar",
                "AKERBP.OL": "Aker BP",
                "AAPL": "Apple Inc",
                "MSFT": "Microsoft Corporation",
                "AMZN": "Amazon.com Inc",
                "GOOGL": "Alphabet Inc",
                "META": "Meta Platforms Inc",
                "TSLA": "Tesla Inc",
                "NVDA": "NVIDIA Corporation",
                "JPM": "JPMorgan Chase & Co",
                "BAC": "Bank of America Corp",
                "JNJ": "Johnson & Johnson"
            }
            
            sectors = ["Technology", "Energy", "Finance", "Healthcare", "Consumer", "Industrials"]
            
            info = {
                'ticker': ticker,
                'shortName': company_names.get(ticker, f"Company {ticker}"),
                'longName': company_names.get(ticker, f"Company {ticker}") + " Corporation",
                'sector': random.choice(sectors),
                'regularMarketPrice': 100 + random.random() * 900,
                'marketCap': random.randint(1000000, 2000000000000),
                'dividendYield': random.random() * 0.05,
                'country': "Norway" if ".OL" in ticker else "USA"
            }
            
            return info
        except Exception as e:
            print(f"Error fetching info for {ticker}: {str(e)}")
            return {}
    
    @staticmethod
    def get_oslo_bors_overview():
        """Get overview of Oslo Børs stocks"""
        overview = {}
        for ticker in OSLO_BORS_TICKERS:
            try:
                data = DataService.get_stock_data(ticker, period='5d')
                info = DataService.get_stock_info(ticker)
                
                if not data.empty:
                    last_price = data['Close'].iloc[-1]
                    prev_price = data['Close'].iloc[-2] if len(data) > 1 else data['Open'].iloc[-1]
                    change = last_price - prev_price
                    change_percent = (change / prev_price) * 100 if prev_price > 0 else 0
                    
                    signals = ["BUY", "SELL", "HOLD"]
                    signal_weights = [0.3, 0.2, 0.5]  # More likely to be HOLD
                    
                    overview[ticker] = {
                        'ticker': ticker,
                        'name': info.get('shortName', ticker),
                        'last_price': round(last_price, 2),
                        'change': round(change, 2),
                        'change_percent': round(change_percent, 2),
                        'volume': data['Volume'].iloc[-1],
                        'signal': random.choices(signals, weights=signal_weights, k=1)[0]
                    }
            except Exception as e:
                print(f"Error getting overview for {ticker}: {str(e)}")
        
        return overview
    
    @staticmethod
    def get_global_stocks_overview():
        """Get overview of global stocks"""
        overview = {}
        for ticker in GLOBAL_TICKERS:
            try:
                data = DataService.get_stock_data(ticker, period='5d')
                info = DataService.get_stock_info(ticker)
                
                if not data.empty:
                    last_price = data['Close'].iloc[-1]
                    prev_price = data['Close'].iloc[-2] if len(data) > 1 else data['Open'].iloc[-1]
                    change = last_price - prev_price
                    change_percent = (change / prev_price) * 100 if prev_price > 0 else 0
                    
                    signals = ["BUY", "SELL", "HOLD"]
                    signal_weights = [0.3, 0.2, 0.5]  # More likely to be HOLD
                    
                    overview[ticker] = {
                        'ticker': ticker,
                        'name': info.get('shortName', ticker),
                        'last_price': round(last_price, 2),
                        'change': round(change, 2),
                        'change_percent': round(change_percent, 2),
                        'volume': data['Volume'].iloc[-1],
                        'signal': random.choices(signals, weights=signal_weights, k=1)[0]
                    }
            except Exception as e:
                print(f"Error getting overview for {ticker}: {str(e)}")
        
        return overview
    
    @staticmethod
    def get_single_stock_data(ticker):
        """Get data for a single stock"""
        try:
            # Hent gjeldende data
            stock_data = DataService.get_stock_data(ticker, period='1d')
            if stock_data.empty:
                return None
                
            # Get last price
            last_price = stock_data['Close'].iloc[-1]
            change = 0
            change_percent = 0
            
            if len(stock_data) > 1:
                prev_price = stock_data['Close'].iloc[-2]
                change = last_price - prev_price
                change_percent = (change / prev_price) * 100 if prev_price > 0 else 0
            
            # Mock data for signal, RSI, etc.
            signals = ["BUY", "SELL", "HOLD"]
            signal_weights = [0.3, 0.2, 0.5]  # More likely to be HOLD
            
            return {
                'ticker': ticker,
                'last_price': round(last_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'signal': random.choices(signals, weights=signal_weights, k=1)[0],
                'rsi': round(20 + random.random() * 60, 2),  # Random RSI between 20 and 80
                'volume': int(stock_data['Volume'].iloc[-1])
            }
        except Exception as e:
            print(f"Error getting data for {ticker}: {str(e)}")
            return None
    
    @staticmethod
    def get_crypto_overview():
        """Get overview of cryptocurrencies"""
        crypto_tickers = ["BTC-USD", "ETH-USD", "XRP-USD", "LTC-USD", "ADA-USD"]
        overview = {}
        
        for ticker in crypto_tickers:
            try:
                data = DataService.get_stock_data(ticker, period='5d')
                
                if not data.empty:
                    last_price = data['Close'].iloc[-1]
                    prev_price = data['Close'].iloc[-2] if len(data) > 1 else data['Open'].iloc[-1]
                    change = last_price - prev_price
                    change_percent = (change / prev_price) * 100 if prev_price > 0 else 0
                    
                    signals = ["BUY", "SELL", "HOLD"]
                    signal_weights = [0.3, 0.2, 0.5]  # More likely to be HOLD
                    
                    crypto_names = {
                        "BTC-USD": "Bitcoin",
                        "ETH-USD": "Ethereum",
                        "XRP-USD": "Ripple",
                        "LTC-USD": "Litecoin",
                        "ADA-USD": "Cardano"
                    }
                    
                    overview[ticker] = {
                        'ticker': ticker,
                        'name': crypto_names.get(ticker, ticker),
                        'last_price': round(last_price, 2),
                        'change': round(change, 2),
                        'change_percent': round(change_percent, 2),
                        'volume': data['Volume'].iloc[-1],                        'signal': random.choices(signals, weights=signal_weights, k=1)[0]
                    }
            except Exception as e:
                print(f"Error getting overview for {ticker}: {str(e)}")
        
        return overview
        
    @staticmethod
    def get_currency_overview():
        """Get overview of currencies"""
        currency_pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCNY=X", "NOKUSD=X"]
        overview = {}
        
        for pair in currency_pairs:
            try:
                data = DataService.get_stock_data(pair, period='5d')
                
                if not data.empty:
                    last_price = data['Close'].iloc[-1]
                    prev_price = data['Close'].iloc[-2] if len(data) > 1 else data['Open'].iloc[-1]
                    change = last_price - prev_price
                    change_percent = (change / prev_price) * 100 if prev_price > 0 else 0
                    
                    pair_names = {
                        "EURUSD=X": "EUR/USD",
                        "GBPUSD=X": "GBP/USD",
                        "USDJPY=X": "USD/JPY",
                        "USDCNY=X": "USD/CNY",
                        "NOKUSD=X": "NOK/USD"
                    }
                      # Dynamic signal generation based on price movements
                    signals = ["BUY", "SELL", "HOLD"]
                    signal_weights = [0.3, 0.2, 0.5]  # Base weights
                    
                    # Adjust weights based on price movement trends
                    if change_percent > 0.5:
                        signal_weights = [0.6, 0.1, 0.3]  # More likely to be BUY
                    elif change_percent < -0.5:
                        signal_weights = [0.1, 0.6, 0.3]  # More likely to be SELL
                    
                    # For demo consistency, we can assign specific signals to certain pairs
                    # but still maintain some variability based on price movement
                    pair_tendency = {
                        "EURUSD=X": 0.7 if change_percent > 0 else 0.3,  # Tends toward BUY
                        "GBPUSD=X": 0.6 if change_percent > 0 else 0.4,  # Tends toward BUY
                        "USDJPY=X": 0.3 if change_percent > 0 else 0.7,  # Tends toward SELL
                        "NOKUSD=X": 0.5,  # Neutral tendency
                    }
                    
                    # Apply pair-specific tendency if available
                    if pair in pair_tendency:
                        tendency = pair_tendency[pair]
                        if random.random() < tendency:
                            signal = "BUY" if change_percent > 0 else "SELL"
                        else:
                            signal = random.choices(signals, weights=signal_weights, k=1)[0]
                    else:
                        signal = random.choices(signals, weights=signal_weights, k=1)[0]
                    
                    overview[pair] = {
                        'ticker': pair,
                        'name': pair_names.get(pair, pair),
                        'last_price': round(last_price, 4),
                        'change': round(change, 4),
                        'change_percent': round(change_percent, 2),
                        'volume': "N/A",  # Forex typically doesn't have volume data in the same way
                        'signal': signal
                    }
            except Exception as e:
                print(f"Error getting overview for {pair}: {str(e)}")
        
        return overview
    
    @staticmethod
    def get_market_overview():
        """Get complete market overview"""
        return {
            'oslo_stocks': DataService.get_oslo_bors_overview(),
            'global_stocks': DataService.get_global_stocks_overview(),
            'crypto': DataService.get_crypto_overview(),
            'currency': DataService.get_currency_overview()
        }
    
    @staticmethod
    def search_ticker(query):
        """Search for tickers by query string"""
        # Mock implementation
        results = []
        
        # Search Oslo Børs tickers
        for ticker in OSLO_BORS_TICKERS:
            if query.lower() in ticker.lower():
                info = DataService.get_stock_info(ticker)
                results.append({
                    'ticker': ticker,
                    'name': info.get('shortName', ticker),
                    'market': 'Oslo Børs'
                })
        
        # Search global tickers
        for ticker in GLOBAL_TICKERS:
            if query.lower() in ticker.lower():
                info = DataService.get_stock_info(ticker)
                results.append({
                    'ticker': ticker,
                    'name': info.get('shortName', ticker),
                    'market': 'Global'
                })
        
        return results
    
    @staticmethod
    def get_crypto_data():
        """Get cryptocurrency data"""
        return DataService.get_crypto_overview()
    
    @staticmethod
    def get_currency_data():
        """Get currency data"""
        return DataService.get_currency_overview()
    
    @staticmethod
    def get_market_news():
        """Get market news"""
        # Mock implementation
        news = []
        
        news_titles = [
            "Markets rise on positive economic data",
            "Tech stocks lead market rally",
            "Oil prices drop on supply concerns",
            "Central bank holds interest rates steady",
            "Earnings season starts with mixed results",
            "Inflation data shows slight decrease",
            "Global markets react to economic indicators",
            "Cryptocurrency market sees volatility"
        ]
        
        for i in range(5):
            days_ago = random.randint(0, 3)
            news_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            
            news.append({
                'title': random.choice(news_titles),
                'date': news_date,
                'source': random.choice(['Bloomberg', 'Reuters', 'CNBC', 'Financial Times', 'Wall Street Journal']),
                'url': f"https://example.com/news/{i}"
            })
        
        return news