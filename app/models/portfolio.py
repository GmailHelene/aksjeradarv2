from datetime import datetime

# Endre denne importlinjen
from ..extensions import db  # Bruk relative imports
from ..services.data_service import DataService

class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Endre fra users_id til user_id
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    stocks = db.relationship('PortfolioStock', backref='portfolio', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Portfolio {self.name}>'
    
    def get_total_value(self):
        """Calculate the total value of the portfolio"""
        total = 0
        for stock in self.stocks:
            try:
                # Prøv å hente gjeldende pris fra en tjeneste
                stock_data = DataService.get_stock_data(stock.ticker, period='1d')
                if not stock_data.empty:
                    current_price = stock_data['Close'].iloc[-1]
                    total += current_price * stock.quantity
            except Exception as e:
                # Fallback til kjøpspris hvis vi ikke kan hente gjeldende pris
                total += stock.purchase_price * stock.quantity
        return total
    
    def get_performance(self):
        """Calculate the performance of the portfolio"""
        total_current = 0
        total_purchase = 0
        
        for stock in self.stocks:
            try:
                # Prøv å hente gjeldende pris fra en tjeneste
                stock_data = DataService.get_stock_data(stock.ticker, period='1d')
                if not stock_data.empty:
                    current_price = stock_data['Close'].iloc[-1]
                    total_current += current_price * stock.quantity
                else:
                    total_current += stock.purchase_price * stock.quantity
            except Exception:
                # Fallback til kjøpspris hvis vi ikke kan hente gjeldende pris
                total_current += stock.purchase_price * stock.quantity
            
            total_purchase += stock.purchase_price * stock.quantity
        
        # Unngå divisjon med null
        if total_purchase == 0:
            return 0
        
        return ((total_current / total_purchase) - 1) * 100  # Return as percentage

class PortfolioStock(db.Model):
    __tablename__ = 'portfolio_stock'
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    ticker = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0)
    purchase_price = db.Column(db.Float, nullable=False, default=0)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<PortfolioStock {self.ticker}>'
    
    def get_current_value(self):
        """Get the current value of this stock position"""
        try:
            stock_data = DataService.get_stock_data(self.ticker, period='1d')
            if not stock_data.empty:
                current_price = stock_data['Close'].iloc[-1]
                return current_price * self.quantity
        except Exception:
            pass
        
        # Fallback til kjøpspris
        return self.purchase_price * self.quantity
    
    def get_profit_loss(self):
        """Get the profit/loss for this stock position"""
        current_value = self.get_current_value()
        purchase_value = self.purchase_price * self.quantity
        return current_value - purchase_value
    
    def get_profit_loss_percent(self):
        """Get the profit/loss percentage for this stock position"""
        purchase_value = self.purchase_price * self.quantity
        if purchase_value == 0:
            return 0
        
        profit_loss = self.get_profit_loss()
        return (profit_loss / purchase_value) * 100

class StockTip(db.Model):
    __tablename__ = 'stock_tips'
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), nullable=False)
    tip_type = db.Column(db.String(10), nullable=False)  # BUY, SELL, HOLD
    confidence = db.Column(db.String(10), nullable=False)  # HIGH, MEDIUM, LOW
    analysis = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<StockTip {self.ticker} - {self.tip_type}>'
    
    @classmethod
    def get_latest_tips(cls, limit=10):
        """Get the latest stock tips"""
        return cls.query.order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def get_tips_by_ticker(cls, ticker):
        """Get all tips for a specific ticker"""
        return cls.query.filter_by(ticker=ticker).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_tips_by_type(cls, tip_type):
        """Get all tips of a specific type (BUY, SELL, HOLD)"""
        return cls.query.filter_by(tip_type=tip_type).order_by(cls.created_at.desc()).all()