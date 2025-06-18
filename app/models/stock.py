from datetime import datetime

# Endre denne importlinjen
from ..extensions import db  # Bruk relative imports

class Watchlist(db.Model):
    __tablename__ = 'watchlist'  # Legg til eksplisitt tabellnavn
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    stocks = db.relationship('WatchlistStock', backref='watchlist', lazy='dynamic')
    
    def __repr__(self):
        return f'<Watchlist {self.name}>'

class WatchlistStock(db.Model):
    __tablename__ = 'watchlist_stock'  # Legg til eksplisitt tabellnavn
    id = db.Column(db.Integer, primary_key=True)
    watchlist_id = db.Column(db.Integer, db.ForeignKey('watchlist.id'))
    ticker = db.Column(db.String(20))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<WatchlistStock {self.ticker}>'