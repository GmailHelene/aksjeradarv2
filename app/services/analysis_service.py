import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime, timedelta
import random

class AnalysisService:
    @staticmethod
    def get_technical_analysis(ticker):
        """Get technical analysis for a stock"""
        try:
            from app.services.data_service import DataService
            # Get stock data
            stock_data = DataService.get_stock_data(ticker)
            if stock_data.empty:
                return {'error': f'No data found for {ticker}'}
            
            # Calculate indicators
            indicators = AnalysisService.get_technical_indicators(stock_data)
            
            # Generate signals
            signal, signal_reason = AnalysisService.generate_signal(indicators)
            
            # Calculate support and resistance
            support, resistance = AnalysisService.calculate_support_resistance(stock_data)
            
            # Prepare the response
            result = {
                'ticker': ticker,
                'last_price': stock_data['Close'].iloc[-1] if not stock_data.empty else 'N/A',
                'signal': signal,
                'signal_reason': signal_reason,
                'rsi': indicators.get('rsi', 'N/A'),
                'macd': indicators.get('macd', 'N/A'),
                'macd_signal': indicators.get('macd_signal', 'N/A'),
                'volume': stock_data['Volume'].iloc[-1] if not stock_data.empty else 'N/A',
                'avg_volume': stock_data['Volume'].mean() if not stock_data.empty else 'N/A',
                'support': support,
                'resistance': resistance,
                'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return result
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_technical_indicators(stock_data):
        """Calculate technical indicators for stock data"""
        try:
            # Initialize results
            results = {}
            
            # Ensure we have data
            if stock_data.empty:
                return results
            
            # Calculate RSI (Relative Strength Index)
            delta = stock_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            results['rsi'] = 100 - (100 / (1 + rs)).iloc[-1]
            
            # Calculate MACD (Moving Average Convergence Divergence)
            ema12 = stock_data['Close'].ewm(span=12).mean()
            ema26 = stock_data['Close'].ewm(span=26).mean()
            results['macd'] = (ema12 - ema26).iloc[-1]
            results['macd_signal'] = (ema12 - ema26).ewm(span=9).mean().iloc[-1]
            
            # Calculate Simple Moving Averages
            results['sma20'] = stock_data['Close'].rolling(window=20).mean()
            results['sma50'] = stock_data['Close'].rolling(window=50).mean()
            results['sma200'] = stock_data['Close'].rolling(window=200).mean()
            
            # Calculate Bollinger Bands
            sma20 = stock_data['Close'].rolling(window=20).mean()
            std20 = stock_data['Close'].rolling(window=20).std()
            results['bollinger_upper'] = sma20 + (std20 * 2)
            results['bollinger_lower'] = sma20 - (std20 * 2)
            
            return results
        except Exception as e:
            print(f"Error calculating indicators: {str(e)}")
            return {}
    
    @staticmethod
    def generate_signal(indicators):
        """Generate a buy/sell/hold signal based on indicators"""
        try:
            signal = "HOLD"
            reasons = []
            
            # RSI signals
            rsi = indicators.get('rsi')
            if rsi is not None:
                if rsi < 30:
                    signal = "BUY"
                    reasons.append(f"RSI ({rsi:.2f}) is below 30, indicating oversold conditions")
                elif rsi > 70:
                    signal = "SELL"
                    reasons.append(f"RSI ({rsi:.2f}) is above 70, indicating overbought conditions")
                else:
                    reasons.append(f"RSI ({rsi:.2f}) is in neutral territory")
            
            # MACD signals
            macd = indicators.get('macd')
            macd_signal = indicators.get('macd_signal')
            if macd is not None and macd_signal is not None:
                if macd > macd_signal:
                    if signal != "SELL":  # Don't override a SELL signal from RSI
                        signal = "BUY"
                    reasons.append(f"MACD ({macd:.2f}) is above signal line ({macd_signal:.2f}), suggesting bullish momentum")
                elif macd < macd_signal:
                    if signal != "BUY":  # Don't override a BUY signal from RSI
                        signal = "SELL"
                    reasons.append(f"MACD ({macd:.2f}) is below signal line ({macd_signal:.2f}), suggesting bearish momentum")
                else:
                    reasons.append(f"MACD ({macd:.2f}) is near the signal line ({macd_signal:.2f})")
            
            signal_reason = " • ".join(reasons) if reasons else "No clear signal"
            
            return signal, signal_reason
        except Exception as e:
            print(f"Error generating signal: {str(e)}")
            return "HOLD", f"Error generating signal: {str(e)}"
    
    @staticmethod
    def calculate_support_resistance(stock_data):
        """Calculate support and resistance levels"""
        try:
            if stock_data.empty or len(stock_data) < 5:
                return 0, 0
            
            # Simple implementation: min and max of recent prices
            recent_data = stock_data.tail(30)
            support = recent_data['Low'].min()
            resistance = recent_data['High'].max()
            
            return support, resistance
        except Exception as e:
            print(f"Error calculating support/resistance: {str(e)}")
            return 0, 0
    
    @staticmethod
    def generate_trading_signals(stock_data):
        """Generate trading signals for a stock"""
        try:
            if stock_data.empty:
                return []
            
            signals = []
            indicators = AnalysisService.get_technical_indicators(stock_data)
            
            # Create sample signals for demonstration
            signal_types = ["BUY", "SELL", "HOLD"]
            confidence_levels = ["HIGH", "MEDIUM", "LOW"]
            
            for i in range(5):
                days_ago = random.randint(1, 30)
                signal_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
                
                signals.append({
                    "date": signal_date,
                    "type": random.choice(signal_types),
                    "confidence": random.choice(confidence_levels),
                    "reason": f"Based on technical analysis on {signal_date}"
                })
            
            return signals
        except Exception as e:
            print(f"Error generating trading signals: {str(e)}")
            return []
    
    @staticmethod
    def plot_stock_chart(ticker):
        """Plot a stock chart and return as base64 image"""
        try:
            from app.services.data_service import DataService
            # Get stock data
            stock_data = DataService.get_stock_data(ticker, period='1y')
            if stock_data.empty:
                return None
            
            # Create figure
            plt.figure(figsize=(10, 6))
            plt.plot(stock_data.index, stock_data['Close'])
            plt.title(f"{ticker} Stock Price")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.grid(True)
            
            # Convert plot to base64 image
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            plt.close()
            
            return base64.b64encode(image_png).decode('utf-8')
        except Exception as e:
            print(f"Error plotting chart: {str(e)}")
            return None
    
    @staticmethod
    def get_stock_recommendation(ticker):
        """Get a comprehensive stock recommendation"""
        try:
            # Get technical analysis
            technical = AnalysisService.get_technical_analysis(ticker)
            
            # Generate a mock prediction (in a real app, this would be a ML model)
            prediction = {
                'next_price': technical.get('last_price', 0) * (1 + (random.random() * 0.1 - 0.05)),
                'change_percent': (random.random() * 10 - 5),
                'confidence': random.choice(['HIGH', 'MEDIUM', 'LOW'])
            }
            
            # Combine technical analysis and prediction for recommendation
            if technical.get('signal') == 'BUY' and prediction['change_percent'] > 0:
                recommendation = 'BUY'
                confidence = 'HIGH'
            elif technical.get('signal') == 'SELL' and prediction['change_percent'] < 0:
                recommendation = 'SELL'
                confidence = 'HIGH'
            elif technical.get('signal') == 'BUY' or prediction['change_percent'] > 3:
                recommendation = 'BUY'
                confidence = 'MEDIUM'
            elif technical.get('signal') == 'SELL' or prediction['change_percent'] < -3:
                recommendation = 'SELL'
                confidence = 'MEDIUM'
            else:
                recommendation = 'HOLD'
                confidence = 'MEDIUM'
            
            return {
                'ticker': ticker,
                'recommendation': recommendation,
                'confidence': confidence,
                'technical_analysis': technical,
                'prediction': prediction
            }
        except Exception as e:
            print(f"Error generating recommendation: {str(e)}")
            return {'error': str(e)}