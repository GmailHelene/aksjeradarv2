import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Define some constants for demo data
OSLO_BORS_TICKERS = [
    "EQNR.OL", "DNB.OL", "TEL.OL", "YAR.OL", "NHY.OL", "AKSO.OL", 
    "MOWI.OL", "ORK.OL", "SALM.OL", "AKERBP.OL", "AUSS.OL", "AZT.OL",
    "BAKKA.OL", "BWLPG.OL", "CRAYN.OL", "ENTRA.OL", "FLNG.OL", "GOGL.OL",
    "GJF.OL", "HEX.OL", "KOG.OL", "MEDI.OL", "ODF.OL", "PGS.OL",
    "SCHA.OL", "SCATC.OL", "SCHB.OL", "SRBANK.OL", "STB.OL", "SUBC.OL",
    "TGS.OL", "TOM.OL", "VEI.OL", "VIZ.OL", "AKVA.OL", "AKER.OL",
    "ASTK.OL", "ADE.OL", "BWE.OL", "BMA.OL", "BGBIO.OL", "COV.OL",
    "DAT.OL", "ELABS.OL", "IDEX.OL", "KID.OL", "KOA.OL", "NAVA.OL",
    "NORD.OL", "NSKOG.OL", "OTS.OL", "PEN.OL", "RECSI.OL", "SADG.OL",
    "SOFF.OL", "ULTI.OL", "XXL.OL", "ZAL.OL", "EMGS.OL", "MULTI.OL",
    "AQUA.OL", "BIOTEC.OL", "NEXT.OL", "PLCS.OL", "REACH.OL", "FRO.OL",
    "ACR.OL", "BDCO.OL", "BOR.OL", "BOREA.OL", "BELCO.OL", "CAMBI.OL",
    "CNTXT.OL", "CIRCA.OL", "CSAM.OL", "DLTX.OL", "EIOF.OL", "ENDUR.OL",
    "FKRAFT.OL", "FROY.OL", "HAFNI.OL", "HUNT.OL", "ISLAX.OL", "JAEREN.OL",
    "KIT.OL", "KOMPL.OL", "LSG.OL", "MSEIS.OL", "NORBT.OL", "NORECO.OL",
    "NRC.OL", "NTSG.OL", "OTOVO.OL", "PARR.OL", "POL.OL", "PROT.OL",
    "QFR.OL", "RING.OL", "SBX.OL", "SAGA.OL", "SALMON.OL", "SATS.OL",
    "SMCRT.OL", "SHLF.OL", "SKUE.OL", "SOGN.OL", "SMDR.OL", "SPOG.OL", 
    "SSG.OL", "SVEG.OL", "TEL.OL", "TGS.OL", "TRVX.OL", "VISTN.OL",
    "VOW.OL", "WAWI.OL", "MORG.OL", "FUELC.OL", "AKER.OL", "ABG.OL",
    "KAHOT.OL", "LINK.OL", "NEL.OL", "NPRO.OL", "NORAM.OL", "MGN.OL",
    "PEXIP.OL", "SANDS.OL", "SCHB.OL", "SUBC.OL", "TIETOO.OL", "VOLUE.OL"
]

GLOBAL_TICKERS = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA", 
    "JPM", "BAC", "JNJ", "PG", "V", "MA", "UNH", "HD", "DIS",
    "NFLX", "PYPL", "ADBE", "CRM", "INTC", "CSCO", "CMCSA", "PEP",
    "KO", "T", "VZ", "ABT", "MRK", "PFE", "TMO", "ABBV", "AVGO",
    "ACN", "TXN", "QCOM", "COST", "WMT", "NKE", "MCD", "SBUX",
    "AMD", "IBM", "GS", "MS", "C", "CVX", "XOM", "BA", "CAT",
    "MMM", "GE", "HON", "LMT", "RTX", "BLK", "SCHW"
]

# Add cryptocurrency data
CRYPTO_DATA = [
    {"symbol": "BTC", "name": "Bitcoin", "image": "https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png"},
    {"symbol": "ETH", "name": "Ethereum", "image": "https://assets.coingecko.com/coins/images/279/thumb/ethereum.png"},
    {"symbol": "USDT", "name": "Tether", "image": "https://assets.coingecko.com/coins/images/325/thumb/Tether.png"},
    {"symbol": "BNB", "name": "Binance Coin", "image": "https://assets.coingecko.com/coins/images/825/thumb/bnb-icon2_2x.png"},
    {"symbol": "USDC", "name": "USD Coin", "image": "https://assets.coingecko.com/coins/images/6319/thumb/USD_Coin_icon.png"},
    {"symbol": "XRP", "name": "XRP", "image": "https://assets.coingecko.com/coins/images/44/thumb/xrp-symbol-white-128.png"},
    {"symbol": "SOL", "name": "Solana", "image": "https://assets.coingecko.com/coins/images/4128/thumb/solana.png"},
    {"symbol": "ADA", "name": "Cardano", "image": "https://assets.coingecko.com/coins/images/975/thumb/cardano.png"},
    {"symbol": "DOGE", "name": "Dogecoin", "image": "https://assets.coingecko.com/coins/images/5/thumb/dogecoin.png"},
    {"symbol": "TRX", "name": "TRON", "image": "https://assets.coingecko.com/coins/images/1094/thumb/tron-logo.png"},
    # Add 40 more cryptocurrencies
    {"symbol": "DOT", "name": "Polkadot", "image": "https://assets.coingecko.com/coins/images/12171/thumb/polkadot.png"},
    {"symbol": "MATIC", "name": "Polygon", "image": "https://assets.coingecko.com/coins/images/4713/thumb/matic-token-icon.png"},
    {"symbol": "LTC", "name": "Litecoin", "image": "https://assets.coingecko.com/coins/images/2/thumb/litecoin.png"},
    {"symbol": "SHIB", "name": "Shiba Inu", "image": "https://assets.coingecko.com/coins/images/11939/thumb/shiba.png"},
    # ... Add more cryptocurrencies here
]

# Add currency data
CURRENCY_DATA = [
    {"code": "USD", "name": "US Dollar", "flag_url": "/static/images/flags/us.png"},
    {"code": "EUR", "name": "Euro", "flag_url": "/static/images/flags/eu.png"},
    {"code": "GBP", "name": "British Pound", "flag_url": "/static/images/flags/gb.png"},
    {"code": "JPY", "name": "Japanese Yen", "flag_url": "/static/images/flags/jp.png"},
    {"code": "CHF", "name": "Swiss Franc", "flag_url": "/static/images/flags/ch.png"},
    {"code": "AUD", "name": "Australian Dollar", "flag_url": "/static/images/flags/au.png"},
    {"code": "CAD", "name": "Canadian Dollar", "flag_url": "/static/images/flags/ca.png"},
    {"code": "SEK", "name": "Swedish Krona", "flag_url": "/static/images/flags/se.png"},
    {"code": "DKK", "name": "Danish Krone", "flag_url": "/static/images/flags/dk.png"},
    {"code": "NOK", "name": "Norwegian Krone", "flag_url": "/static/images/flags/no.png"},
    # Add more currencies as needed
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
    def get_crypto_list(page=1, per_page=50):
        """Get a paginated list of cryptocurrencies"""
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        cryptos = []
        for idx, crypto in enumerate(CRYPTO_DATA[start_idx:end_idx], start=start_idx+1):
            price = random.uniform(100, 100000) if crypto["symbol"] == "BTC" else random.uniform(0.1, 5000)
            change = random.uniform(-10, 10)
            market_cap = price * random.uniform(1000000, 1000000000)
            volume = market_cap * random.uniform(0.1, 0.3)
            supply = market_cap / price
            
            cryptos.append({
                "rank": idx,
                "name": crypto["name"],
                "symbol": crypto["symbol"],
                "image": crypto["image"],
                "current_price": price,
                "price_change_percentage_24h": change,
                "market_cap": market_cap,
                "total_volume": volume,
                "circulating_supply": supply
            })
                "rank": idx,
                "name": crypto["name"],
                "symbol": crypto["symbol"],
                "image": crypto["image"],
                "current_price": price,
                "price_change_percentage_24h": change,
                "market_cap": market_cap,
                "total_volume": volume,
                "circulating_supply": supply
            })
        
        return cryptos

    @staticmethod
    def get_crypto_count():
        """Get total number of cryptocurrencies"""
        return len(CRYPTO_DATA)

    @staticmethod
    def get_currency_list(base="NOK", page=1, per_page=50):
        """Get a paginated list of currency exchange rates"""
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        currencies = []
        for currency in CURRENCY_DATA[start_idx:end_idx]:
            if currency["code"] == base:
                continue
                
            rate = random.uniform(0.5, 2.0)
            change_24h = random.uniform(-5, 5)
            change_1w = random.uniform(-8, 8)
            change_1m = random.uniform(-12, 12)
            
            currencies.append({
                "code": currency["code"],
                "name": currency["name"],
                "flag_url": currency["flag_url"],
                "rate": f"{rate:.4f}",
                "change_24h": f"{change_24h:.2f}",
                "change_1w": f"{change_1w:.2f}",
                "change_1m": f"{change_1m:.2f}",
                "updated_at": datetime.now().strftime("%H:%M:%S")
            })
        
        return currencies

    @staticmethod
    def get_currency_count():
        """Get total number of currencies"""
        return len(CURRENCY_DATA)

    @staticmethod
    def get_crypto_overview(limit=10):
        """Get overview of top cryptocurrencies"""
        return DataService.get_crypto_list(page=1, per_page=limit)

    @staticmethod
    def get_currency_overview(limit=10):
        """Get overview of main currencies"""
        return DataService.get_currency_list(page=1, per_page=limit)

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