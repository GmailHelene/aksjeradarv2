import os
from datetime import datetime
import random

class AIService:
    @staticmethod
    def get_stock_analysis(ticker):
        """
        Generate AI analysis for a stock (demo implementation)
        """
        try:
            # Dictionary with realistic data for specific tickers
            realistic_data = {
                'EQNR.OL': {
                    "ticker": "EQNR.OL",
                    "sentiment": "bullish",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate bullish outlook for Equinor based on strong energy prices and healthy financials.",
                    "technical_factors": [
                        "RSI at 58.2 indicates moderate bullish momentum",
                        "Price trading above both 50-day and 200-day moving averages",
                        "Bullish MACD crossover observed in recent trading sessions"
                    ],
                    "fundamental_factors": [
                        "Strong cash flow from core operations with $12.5B in Q2",
                        "Attractive dividend yield of 4.2% with sustainable payout ratio",
                        "Increasing investments in renewable energy projects with $2.3B committed"
                    ],
                    "prediction": {
                        "direction": "up",
                        "confidence": 0.72,
                        "time_frame": "short to medium term",
                        "target_price": "362 NOK"
                    }
                },
                'DNB.OL': {
                    "ticker": "DNB.OL",
                    "sentiment": "neutral",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate neutral outlook for DNB with stable banking operations but limited growth catalysts.",
                    "technical_factors": [
                        "RSI at 52.3 indicates neutral momentum",
                        "Price oscillating around 50-day moving average",
                        "Volume analysis shows moderate trading activity"
                    ],
                    "fundamental_factors": [
                        "Solid capital position with Tier 1 ratio above regulatory requirements",
                        "Moderate loan growth in retail and corporate sectors at 3.2%",
                        "Dividend yield of 3.8% with potential for increases"
                    ],
                    "prediction": {
                        "direction": "sideways",
                        "confidence": 0.65,
                        "time_frame": "medium term",
                        "target_price": "215-225 NOK range"
                    }
                },
                'AAPL': {
                    "ticker": "AAPL",
                    "sentiment": "bullish",
                    "strength": "strong",
                    "summary": "AI analysis suggests a strong bullish outlook for Apple based on services growth and product innovation.",
                    "technical_factors": [
                        "RSI at 61.5 indicates moderate bullish momentum",
                        "Bullish flag pattern forming on the price chart",
                        "Strong positive volume profile with institutional buying"
                    ],
                    "fundamental_factors": [
                        "Services revenue growing at 18.7% YoY with high margins",
                        "Robust balance sheet with $190B in cash reserves",
                        "Strong brand loyalty and ecosystem lock-in effects"
                    ],
                    "prediction": {
                        "direction": "up",
                        "confidence": 0.82,
                        "time_frame": "medium to long term",
                        "target_price": "$210"
                    }
                },
                'MSFT': {
                    "ticker": "MSFT",
                    "sentiment": "bullish",
                    "strength": "strong",
                    "summary": "AI analysis suggests a strong bullish outlook for Microsoft driven by cloud growth and AI adoption.",
                    "technical_factors": [
                        "RSI at 72.3 indicates overbought conditions, potential short-term pullback",
                        "Price trading well above all key moving averages",
                        "Uptrend intact since March 2023"
                    ],
                    "fundamental_factors": [
                        "Azure cloud service showing accelerating growth of 27.5% YoY",
                        "Strong position in AI with OpenAI integrations",
                        "Diversified revenue streams across multiple product lines"
                    ],
                    "prediction": {
                        "direction": "up",
                        "confidence": 0.85,
                        "time_frame": "long term",
                        "target_price": "$425"
                    }
                },
                'TSLA': {
                    "ticker": "TSLA",
                    "sentiment": "bearish",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate bearish outlook for Tesla due to margin pressures and increasing competition.",
                    "technical_factors": [
                        "RSI at 38.4 approaching oversold territory",
                        "Price below 50-day moving average",
                        "Downward trend channel with repeated failed breakout attempts"
                    ],
                    "fundamental_factors": [
                        "Margin pressure from price competition with 18.2% gross margin",
                        "Challenges meeting delivery targets for new models",
                        "High valuation relative to other automakers at 60x P/E"
                    ],
                    "prediction": {
                        "direction": "down",
                        "confidence": 0.68,
                        "time_frame": "short to medium term",
                        "target_price": "$210"
                    }
                },
                'YAR.OL': {
                    "ticker": "YAR.OL",
                    "sentiment": "bullish",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate bullish outlook for Yara based on improving fertilizer markets and cost control initiatives.",
                    "technical_factors": [
                        "RSI at 63.2 shows growing bullish momentum",
                        "Price recently broke above key resistance level at 340 NOK",
                        "Increasing volume on up days indicates accumulation"
                    ],
                    "fundamental_factors": [
                        "Fertilizer prices stabilizing after period of volatility",
                        "Cost efficiency program targeting 350M USD in annual savings",
                        "Dividend yield of 5.1% appears sustainable"
                    ],
                    "prediction": {
                        "direction": "up",
                        "confidence": 0.71,
                        "time_frame": "medium term",
                        "target_price": "365 NOK"
                    }
                },
                'NHY.OL': {
                    "ticker": "NHY.OL",
                    "sentiment": "neutral",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate neutral outlook for Norsk Hydro with mixed signals from aluminum markets.",
                    "technical_factors": [
                        "RSI at 50.6 indicates neutral momentum",
                        "Price consolidating in range between 62-68 NOK",
                        "Moving averages converging, suggesting potential breakout"
                    ],
                    "fundamental_factors": [
                        "Aluminum prices stabilizing after volatile period",
                        "Cost position improving through operational efficiency",
                        "Green aluminum initiatives gaining traction with premium pricing"
                    ],
                    "prediction": {
                        "direction": "sideways",
                        "confidence": 0.60,
                        "time_frame": "short term",
                        "target_price": "64-68 NOK range"
                    }
                },
                'TEL.OL': {
                    "ticker": "TEL.OL",
                    "sentiment": "bearish",
                    "strength": "weak",
                    "summary": "AI analysis suggests a weak bearish outlook for Telenor due to competitive pressures in core markets.",
                    "technical_factors": [
                        "RSI at 32.1 approaching oversold territory",
                        "Price below both 50-day and 200-day moving averages",
                        "Decreasing volume profile suggests waning seller interest"
                    ],
                    "fundamental_factors": [
                        "Revenue pressure in Nordic markets with 1.5% decline YoY",
                        "Cost cutting initiatives showing limited impact on margins",
                        "Dividend yield of 6.3% may be difficult to maintain"
                    ],
                    "prediction": {
                        "direction": "down",
                        "confidence": 0.58,
                        "time_frame": "short term",
                        "target_price": "118 NOK"
                    }
                },
                'BTC-USD': {
                    "ticker": "BTC-USD",
                    "sentiment": "bullish",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate bullish outlook for Bitcoin following recent halving and institutional adoption.",
                    "technical_factors": [
                        "RSI at 68.3 approaching overbought territory",
                        "Trading above all major moving averages",
                        "Volume profile shows increasing buying interest post-halving"
                    ],
                    "fundamental_factors": [
                        "Reduced issuance rate after halving event",
                        "Increasing institutional adoption through ETFs",
                        "Correlation with traditional financial markets remains high"
                    ],
                    "prediction": {
                        "direction": "up",
                        "confidence": 0.74,
                        "time_frame": "medium to long term",
                        "target_price": "$72,000"
                    }
                },
                'ETH-USD': {
                    "ticker": "ETH-USD",
                    "sentiment": "neutral",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate neutral outlook for Ethereum with technical improvements but scaling challenges.",
                    "technical_factors": [
                        "RSI at 55.2 indicates neutral momentum",
                        "Price consolidating between 3200-3600 USD range",
                        "Volume patterns suggest accumulation phase"
                    ],
                    "fundamental_factors": [
                        "ETH staking yield around 3.8% attracting long-term holders",
                        "Layer 2 scaling solutions gaining traction",
                        "Competition from alternative smart contract platforms"
                    ],
                    "prediction": {
                        "direction": "sideways",
                        "confidence": 0.65,
                        "time_frame": "short term",
                        "target_price": "$3400-3700 range"
                    }
                }
            }
            
            # Return realistic data if available
            if ticker in realistic_data:
                analysis = realistic_data[ticker]
                analysis["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return analysis
            
            # Otherwise generate random but plausible data
            sentiments = ["bullish", "bearish", "neutral"]
            sentiment = random.choice(sentiments)
            
            strength = random.choice(["strong", "moderate", "weak"])
            
            analysis = {
                "ticker": ticker,
                "sentiment": sentiment,
                "strength": strength,
                "summary": f"AI analysis suggests a {strength} {sentiment} outlook for {ticker}.",
                "technical_factors": [
                    f"RSI at {random.randint(30, 70)}.{random.randint(1, 9)} indicates {'potential oversold condition' if sentiment == 'bullish' else 'potential overbought condition' if sentiment == 'bearish' else 'neutral momentum'}",
                    f"Price {'trading above' if sentiment == 'bullish' else 'trading below' if sentiment == 'bearish' else 'oscillating around'} key moving averages",
                    f"Volume patterns suggest {sentiment} momentum building"
                ],
                "fundamental_factors": [
                    f"{'Strong' if sentiment == 'bullish' else 'Weak' if sentiment == 'bearish' else 'Moderate'} financial performance in recent quarters",
                    f"{'Expanding' if sentiment == 'bullish' else 'Contracting' if sentiment == 'bearish' else 'Stable'} margins and profitability metrics",
                    f"{'Favorable' if sentiment == 'bullish' else 'Challenging' if sentiment == 'bearish' else 'Mixed'} industry conditions and market position"
                ],
                "prediction": {
                    "direction": "up" if sentiment == "bullish" else ("down" if sentiment == "bearish" else "sideways"),
                    "confidence": 0.8 if strength == "strong" else (0.6 if strength == "moderate" else 0.4),
                    "time_frame": f"{random.choice(['short', 'medium', 'long'])} term",
                    "target_price": f"${random.randint(5, 500)}" if not ticker.endswith('.OL') else f"{random.randint(50, 500)} NOK"
                },
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return analysis
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def generate_market_summary(sector=None):
        """
        Generate AI market summary (demo implementation)
        """
        try:
            # Realistic market summaries for different sectors
            sector_summaries = {
                "energy": {
                    "summary": "The energy sector is showing positive trends with oil prices stabilizing above $80 per barrel, supporting improved cash flows for major producers.",
                    "details": [
                        "Oil majors reporting strong Q2 earnings with improved cash flows",
                        "Renewable energy investments accelerating across the sector",
                        "Natural gas prices stabilizing after period of high volatility"
                    ],
                    "outlook": "The sector outlook remains positive with balanced supply-demand dynamics and ongoing transition investments.",
                    "key_stocks": ["EQNR.OL", "XOM", "CVX", "BP"]
                },
                "finance": {
                    "summary": "The financial sector is showing mixed signals with banks benefiting from higher interest rates but facing increased loan loss provisions.",
                    "details": [
                        "Net interest margins improving for most banks in the current rate environment",
                        "Investment banking activity showing signs of recovery after weak 2023",
                        "Fintech competition continues to pressure traditional business models"
                    ],
                    "outlook": "The sector faces both opportunities from high rates and challenges from potential credit quality deterioration.",
                    "key_stocks": ["DNB.OL", "JPM", "BAC", "GS"]
                },
                "technology": {
                    "summary": "The technology sector continues to outperform, driven by AI adoption, cloud growth, and improving semiconductor demand.",
                    "details": [
                        "AI investments accelerating across enterprise software and hardware",
                        "Cloud providers reporting strong growth with improving margins",
                        "Semiconductor companies seeing improved demand after inventory correction"
                    ],
                    "outlook": "The technology sector remains well-positioned for growth with AI as a major catalyst.",
                    "key_stocks": ["MSFT", "AAPL", "NVDA", "ASML"]
                },
                "healthcare": {
                    "summary": "The healthcare sector is showing resilience with pharmaceuticals and medical technology companies reporting solid results.",
                    "details": [
                        "Pharmaceutical companies benefiting from strong pipelines and new drug approvals",
                        "Healthcare services seeing stable demand patterns",
                        "Medical technology innovation accelerating in diagnostics and monitoring"
                    ],
                    "outlook": "The healthcare sector offers defensive characteristics with growth opportunities in specific segments.",
                    "key_stocks": ["JNJ", "PFE", "ISRG", "UNH"]
                }
            }
            
            # Default market summary
            default_summary = {
                "summary": "Overall market sentiment is cautiously optimistic with mixed signals across sectors. Technology and energy showing strength while consumer discretionary faces headwinds.",
                "details": [
                    "Major indices trading near all-time highs with improving breadth",
                    "Interest rate expectations stabilizing with inflation trending lower",
                    "Earnings reports generally in line with or exceeding analyst expectations"
                ],
                "outlook": "Markets appear fairly valued with potential volatility around economic data and monetary policy decisions.",
                "key_stocks": ["AAPL", "MSFT", "EQNR.OL", "DNB.OL"]
            }
            
            # Return sector-specific summary if requested and available
            if sector and sector.lower() in sector_summaries:
                summary = sector_summaries[sector.lower()]
            else:
                # Return general market summary
                summary = default_summary
            
            # Add generation timestamp
            summary["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return summary
            
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_ai_portfolio_recommendation(tickers):
        """
        Get AI recommendation for a portfolio (demo implementation)
        """
        if not tickers:
            return None
        
        # Dictionary with realistic recommendations for specific tickers
        ticker_recommendations = {
            'EQNR.OL': {"action": "buy", "confidence": "high", "reason": "Strong cash flow generation and attractive valuation"},
            'DNB.OL': {"action": "hold", "confidence": "medium", "reason": "Stable performance with limited near-term catalysts"},
            'YAR.OL': {"action": "buy", "confidence": "medium", "reason": "Improving fertilizer market conditions and cost efficiency"},
            'NHY.OL': {"action": "hold", "confidence": "medium", "reason": "Balanced risk-reward with aluminum market uncertainty"},
            'TEL.OL': {"action": "reduce", "confidence": "medium", "reason": "Competitive pressures in key markets affecting growth"},
            'AAPL': {"action": "buy", "confidence": "high", "reason": "Services growth and ecosystem strength continue to drive results"},
            'MSFT': {"action": "buy", "confidence": "high", "reason": "Cloud leadership and AI integration creating multiple growth vectors"},
            'AMZN': {"action": "buy", "confidence": "medium", "reason": "Improving margins in retail and continued AWS strength"},
            'GOOGL': {"action": "buy", "confidence": "medium", "reason": "Digital advertising recovery and AI integration across services"},
            'TSLA': {"action": "sell", "confidence": "medium", "reason": "Margin pressure and increasing competition in EV space"},
            'BTC-USD': {"action": "buy", "confidence": "medium", "reason": "Post-halving dynamics and institutional adoption through ETFs"},
            'ETH-USD': {"action": "hold", "confidence": "medium", "reason": "Ongoing technical improvements but scaling challenges remain"}
        }
        
        # Generate recommendations
        recommendations = []
        for ticker in tickers:
            if ticker in ticker_recommendations:
                rec = ticker_recommendations[ticker]
                recommendations.append({
                    "ticker": ticker,
                    "action": rec["action"],
                    "confidence": rec["confidence"],
                    "reason": rec["reason"]
                })
            else:
                # Random but plausible recommendation for unknown tickers
                action = random.choice(["hold", "buy", "sell", "increase", "decrease"])
                confidence = random.choice(["high", "medium", "low"])
                reason = f"Based on {random.choice(['technical indicators', 'fundamental analysis', 'market trends', 'sector performance'])}"
                recommendations.append({
                    "ticker": ticker,
                    "action": action,
                    "confidence": confidence,
                    "reason": reason
                })
        
        # Portfolio health assessment based on the recommendations
        buy_count = sum(1 for r in recommendations if r["action"] in ["buy", "increase"])
        sell_count = sum(1 for r in recommendations if r["action"] in ["sell", "decrease"])
        
        if buy_count > sell_count * 2:
            portfolio_health = "strong"
        elif buy_count > sell_count:
            portfolio_health = "moderate"
        else:
            portfolio_health = "needs attention"
            
        # Portfolio diversification based on tickers
        sectors_count = len(set([t.split('.')[0][-2:] if '.' in t else t[:4] for t in tickers]))
        if sectors_count >= 5 or len(tickers) >= 8:
            diversification = "well diversified"
        elif sectors_count >= 3 or len(tickers) >= 5:
            diversification = "moderately diversified"
        else:
            diversification = "poorly diversified"
            
        return {
            "portfolio_health": portfolio_health,
            "diversification": diversification,
            "risk_level": random.choice(["low", "moderate", "high"]),
            "recommendations": recommendations,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }