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
            realistic_data = {                'EQNR.OL': {
                    "ticker": "EQNR.OL",
                    "sentiment": "bullish",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate bullish outlook for Equinor based on strong energy prices, healthy financials, and strategic renewable energy investments. The company continues to benefit from high oil and gas prices while simultaneously investing in green energy projects.",
                    "technical_factors": [
                        "RSI at 58.2 indicates moderate bullish momentum without being overbought",
                        "Price trading above both 50-day and 200-day moving averages, confirming uptrend",
                        "Bullish MACD crossover observed in recent trading sessions with increasing histogram",
                        "Volume profile shows accumulation on up days, suggesting institutional buying",
                        "Recent consolidation pattern with higher lows indicates possible continuation"
                    ],
                    "fundamental_factors": [
                        "Strong cash flow from core operations with $12.5B in Q2, 15% higher than previous quarter",
                        "Attractive dividend yield of 4.2% with sustainable 40% payout ratio",
                        "Increasing investments in renewable energy projects with $2.3B committed to offshore wind",
                        "Net debt to capital ratio of 15.3%, well below industry average of 28%",
                        "Forward P/E of 7.5 represents a 30% discount to 5-year average"
                    ],
                    "prediction": {
                        "direction": "up",
                        "confidence": 0.72,
                        "time_frame": "short to medium term (3-6 months)",
                        "target_price": "362 NOK"
                    },
                    "economic_indicators": {
                        "oil_price_trend": "stable with upward bias",
                        "sector_performance": "energy sector outperforming market by 8%",
                        "interest_rate_impact": "minimal exposure to rate increases",
                        "currency_exposure": "USD strength favorable for oil revenues"
                    }
                },
                'DNB.OL': {
                    "ticker": "DNB.OL",
                    "sentiment": "neutral",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate neutral outlook for DNB with stable banking operations but limited growth catalysts. While the bank maintains strong capital levels and benefits from higher interest rates, slow economic growth in Norway limits loan expansion opportunities.",
                    "technical_factors": [
                        "RSI at 52.3 indicates neutral momentum with no clear overbought/oversold signals",
                        "Price oscillating around 50-day moving average with decreased volatility",
                        "Volume analysis shows moderate trading activity with no clear accumulation/distribution",
                        "Price consolidating in range between 210-225 NOK for past 6 weeks",
                        "200-day moving average showing flattening trend, indicating neutral long-term outlook"
                    ],
                    "fundamental_factors": [
                        "Solid capital position with Tier 1 ratio of 18.2%, well above regulatory requirements",
                        "Moderate loan growth in retail and corporate sectors at 3.2% year-over-year",
                        "Dividend yield of 3.8% with potential for increases given 50% payout ratio target",
                        "Net interest margin improved to 1.7% from 1.5% due to higher interest rates",
                        "Cost-to-income ratio stable at 43.5%, among best-in-class for European banks"
                    ],
                    "prediction": {
                        "direction": "sideways",
                        "confidence": 0.65,
                        "time_frame": "medium term (6-12 months)",
                        "target_price": "215-225 NOK range"
                    },
                    "economic_indicators": {
                        "interest_rate_trend": "stable high rates favorable for margins",
                        "norwegian_economy": "modest GDP growth of 1.5-2%",
                        "housing_market": "cooling but stable, limiting mortgage growth",
                        "consumer_confidence": "moderately cautious, affecting loan demand"
                    }
                },
                'AAPL': {
                    "ticker": "AAPL",
                    "sentiment": "bullish",
                    "strength": "strong",
                    "summary": "AI analysis suggests a strong bullish outlook for Apple based on services growth, strong product ecosystem, and upcoming AI innovations. The company continues to demonstrate pricing power and customer loyalty while expanding its high-margin services business at double-digit rates.",
                    "technical_factors": [
                        "RSI at 61.5 indicates moderate bullish momentum without reaching overbought levels",
                        "Bullish flag pattern forming on the price chart after recent 15% rally",
                        "Strong positive volume profile with institutional buying on pullbacks",
                        "Golden cross formed with 50-day SMA crossing above 200-day SMA",
                        "Price consolidating above previous resistance level, now acting as support"
                    ],
                    "fundamental_factors": [
                        "Services revenue growing at 18.7% YoY with high margins exceeding 70%",
                        "Robust balance sheet with $190B in cash reserves and minimal debt",
                        "Strong brand loyalty and ecosystem lock-in effects with 98% retention rate",
                        "Share repurchase program continuing with $90B authorized, reducing share count",
                        "Forward P/E of 28x justified by services growth and upcoming AI initiatives"
                    ],
                    "prediction": {
                        "direction": "up",
                        "confidence": 0.82,
                        "time_frame": "medium to long term (6-18 months)",
                        "target_price": "$210-215"
                    },
                    "economic_indicators": {
                        "consumer_spending": "resilient in premium segment",
                        "tech_sector_trend": "outperforming broader market by 12%",
                        "ai_investment_cycle": "early stages with significant growth potential",
                        "supply_chain": "improved with diversification away from China"
                    }
                },
                'MSFT': {
                    "ticker": "MSFT",
                    "sentiment": "bullish",
                    "strength": "strong",
                    "summary": "AI analysis suggests a strong bullish outlook for Microsoft driven by cloud growth, AI adoption, and recurring revenue model strength. The company is well-positioned as a leader in enterprise AI implementation with Azure and Copilot services.",
                    "technical_factors": [
                        "RSI at 72.3 indicates overbought conditions, potential short-term pullback opportunity",
                        "Price trading well above all key moving averages with strong momentum",
                        "Uptrend intact since March 2023 with series of higher highs and higher lows",
                        "Volume increasing on breakouts, confirming bullish sentiment",
                        "Minimal price resistance overhead based on historical trading patterns"
                    ],
                    "fundamental_factors": [
                        "Azure cloud service showing accelerating growth of 27.5% YoY, exceeding expectations",
                        "Strong position in AI with OpenAI integrations and Copilot monetization",
                        "Diversified revenue streams across multiple product lines with 85% recurring revenue",
                        "Operating margins expanded to 43.2% from 41.8% year-over-year",
                        "Forward EV/EBITDA of 22x justified by cloud growth and AI premium"
                    ],
                    "prediction": {
                        "direction": "up",
                        "confidence": 0.85,
                        "time_frame": "long term (12-24 months)",
                        "target_price": "$425-435"
                    },
                    "economic_indicators": {
                        "enterprise_tech_spending": "resilient despite economic uncertainty",
                        "cloud_market_growth": "22% CAGR expected over next 3 years",
                        "ai_adoption_rate": "accelerating in enterprise segment",
                        "interest_rate_impact": "minimal with strong cash flow generation"
                    }
                },
                'TSLA': {
                    "ticker": "TSLA",
                    "sentiment": "bearish",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate bearish outlook for Tesla due to margin pressures, increasing competition in the EV market, and high valuation relative to other automakers. The company faces challenges meeting delivery targets while managing price reductions.",
                    "technical_factors": [
                        "RSI at 38.4 approaching oversold territory but without positive divergence yet",
                        "Price below 50-day and 200-day moving averages, confirming downtrend",
                        "Downward trend channel with repeated failed breakout attempts since January",
                        "Volume increasing on down days, suggesting distribution pattern",
                        "Head and shoulders pattern formed with neckline broken, targeting $210 area"
                    ],
                    "fundamental_factors": [
                        "Margin pressure from price competition with 18.2% gross margin, down from 25.1% last year",
                        "Challenges meeting delivery targets for new models with 5% miss in Q2",
                        "High valuation relative to other automakers at 60x P/E vs. industry average of 12x",
                        "Increasing competition in core EV market with 27 new models launching this year",
                        "R&D spending declining as percentage of revenue, potentially limiting future innovation"
                    ],
                    "prediction": {
                        "direction": "down",
                        "confidence": 0.68,
                        "time_frame": "short to medium term (3-6 months)",
                        "target_price": "$210-195 range"
                    },
                    "economic_indicators": {
                        "ev_market_growth": "slowing to 25% from 40% previous year",
                        "battery_material_costs": "stabilizing after significant declines",
                        "interest_rate_impact": "negative on vehicle financing and valuation",
                        "china_market_dynamics": "increasing competition and price pressure"
                    }
                },
                'YAR.OL': {
                    "ticker": "YAR.OL",
                    "sentiment": "bullish",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate bullish outlook for Yara based on improving fertilizer markets, cost control initiatives, and strategic positioning in green ammonia. The company is successfully navigating volatile commodity prices while maintaining operational efficiency.",
                    "technical_factors": [
                        "RSI at 63.2 shows growing bullish momentum without reaching overbought levels",
                        "Price recently broke above key resistance level at 340 NOK on high volume",
                        "Increasing volume on up days indicates accumulation phase",
                        "50-day moving average crossed above 200-day moving average (golden cross)",
                        "Price consolidation after breakout suggesting continuation pattern"
                    ],
                    "fundamental_factors": [
                        "Fertilizer prices stabilizing after period of volatility, improving margin visibility",
                        "Cost efficiency program targeting 350M USD in annual savings, 65% achieved",
                        "Dividend yield of 5.1% appears sustainable with 50-60% payout ratio policy",
                        "Strategic investments in green ammonia position company for future growth",
                        "Valuation at 8.2x forward EV/EBITDA represents 15% discount to 5-year average"
                    ],
                    "prediction": {
                        "direction": "up",
                        "confidence": 0.71,
                        "time_frame": "medium term (6-12 months)",
                        "target_price": "365-380 NOK"
                    },
                    "economic_indicators": {
                        "agricultural_commodity_prices": "stabilizing at profitable levels for farmers",
                        "natural_gas_prices": "moderating, positive for production costs",
                        "global_food_demand": "increasing with population growth",
                        "green_transition": "favorable policy environment for low-carbon ammonia"
                    }
                },
                'NHY.OL': {
                    "ticker": "NHY.OL",
                    "sentiment": "neutral",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate neutral outlook for Norsk Hydro with mixed signals from aluminum markets, energy costs, and operational improvements. The company benefits from green aluminum premiums but faces uncertainty in global industrial demand.",
                    "technical_factors": [
                        "RSI at 50.6 indicates neutral momentum in balanced territory",
                        "Price consolidating in range between 62-68 NOK for past 8 weeks",
                        "Moving averages converging, suggesting potential breakout or breakdown",
                        "Volume pattern shows no clear accumulation or distribution",
                        "Price sitting at 200-day moving average, key technical level"
                    ],
                    "fundamental_factors": [
                        "Aluminum prices stabilizing around $2,400/ton after volatile period",
                        "Cost position improving through operational efficiency program",
                        "Green aluminum initiatives gaining traction with premium pricing of 15-20%",
                        "European energy costs moderating, positive for smelting operations",
                        "Capital allocation balanced between dividends (3.5% yield) and growth investments"
                    ],
                    "prediction": {
                        "direction": "sideways",
                        "confidence": 0.60,
                        "time_frame": "short to medium term (3-6 months)",
                        "target_price": "64-68 NOK range"
                    },
                    "economic_indicators": {
                        "industrial_production": "slowing in Europe and China",
                        "energy_prices": "stabilizing at lower levels than 2022 peak",
                        "construction_activity": "weakening in key markets",
                        "green_transition": "supportive policies for low-carbon aluminum"
                    }
                },
                'TEL.OL': {
                    "ticker": "TEL.OL",
                    "sentiment": "bearish",
                    "strength": "weak",
                    "summary": "AI analysis suggests a weak bearish outlook for Telenor due to competitive pressures in core markets, revenue challenges, and limited growth catalysts. The company faces margin pressure despite cost-cutting initiatives.",
                    "technical_factors": [
                        "RSI at 32.1 approaching oversold territory, potential for technical bounce",
                        "Price below both 50-day and 200-day moving averages, confirming downtrend",
                        "Decreasing volume profile suggests waning seller interest, potential bottoming",
                        "Series of lower highs and lower lows established since September",
                        "Price approaching support level at 120 NOK from previous consolidation"
                    ],
                    "fundamental_factors": [
                        "Revenue pressure in Nordic markets with 1.5% decline YoY in mature segments",
                        "Cost cutting initiatives showing limited impact on overall margins",
                        "Dividend yield of 6.3% may be difficult to maintain given 85% payout ratio",
                        "Market saturation in core Nordic mobile and broadband segments",
                        "Asian operations facing regulatory and competitive challenges"
                    ],
                    "prediction": {
                        "direction": "down",
                        "confidence": 0.58,
                        "time_frame": "short term (3 months)",
                        "target_price": "118-122 NOK"
                    },
                    "economic_indicators": {
                        "telecom_sector_performance": "underperforming broader market by 6%",
                        "nordic_economies": "slowing consumer spending affecting upgrades",
                        "asian_markets": "competitive intensity increasing",
                        "interest_rate_impact": "negative with high dividend payout expectations"
                    }
                },
                'BTC-USD': {
                    "ticker": "BTC-USD",
                    "sentiment": "bullish",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate bullish outlook for Bitcoin following recent halving and increasing institutional adoption through ETFs. While near-term volatility is expected, the longer-term supply-demand dynamics appear favorable.",
                    "technical_factors": [
                        "RSI at 68.3 approaching overbought territory, suggesting potential consolidation",
                        "Trading above all major moving averages (50, 100, and 200-day)",
                        "Volume profile shows increasing buying interest post-halving event",
                        "Higher lows established on weekly timeframe since October 2023",
                        "Key resistance at $70,000 based on previous all-time high"
                    ],
                    "fundamental_factors": [
                        "Reduced issuance rate after halving event, cutting new supply by 50%",
                        "Increasing institutional adoption through spot ETFs with $12B in inflows",
                        "Correlation with traditional financial markets remains high at 0.65",
                        "On-chain metrics show accumulation by long-term holders",
                        "Mining difficulty at all-time high, indicating network security"
                    ],
                    "prediction": {
                        "direction": "up",
                        "confidence": 0.74,
                        "time_frame": "medium to long term (6-18 months)",
                        "target_price": "$72,000-80,000"
                    },
                    "economic_indicators": {
                        "inflation_expectations": "moderating but still supportive for hard assets",
                        "institutional_interest": "growing with regulatory clarity",
                        "retail_sentiment": "improving from bear market lows",
                        "global_liquidity": "expanding with central bank policies"
                    }
                },
                'ETH-USD': {
                    "ticker": "ETH-USD",
                    "sentiment": "neutral",
                    "strength": "moderate",
                    "summary": "AI analysis suggests a moderate neutral outlook for Ethereum with technical improvements but scaling challenges and competition from alternative Layer 1 blockchains. The network benefits from developer activity but faces uncertainty around regulatory classification.",
                    "technical_factors": [
                        "RSI at 55.2 indicates neutral momentum in balanced territory",
                        "Price consolidating between 3200-3600 USD range for past 6 weeks",
                        "Volume patterns suggest accumulation phase but without breakout confirmation",
                        "200-day moving average providing support at $3,150 level",
                        "Narrowing Bollinger Bands indicate potential volatility expansion ahead"
                    ],
                    "fundamental_factors": [
                        "ETH staking yield around 3.8% attracting long-term holders with 25% supply staked",
                        "Layer 2 scaling solutions gaining traction with 42% increase in TVL",
                        "Competition from alternative smart contract platforms pressuring market share",
                        "Deflationary tokenomics with net supply reduction since EIP-1559",
                        "Developer activity remains strong with 28% growth in active repositories"
                    ],
                    "prediction": {
                        "direction": "sideways",
                        "confidence": 0.65,
                        "time_frame": "short term (1-3 months)",
                        "target_price": "$3400-3700 range"
                    },
                    "economic_indicators": {
                        "defi_ecosystem": "stabilizing after period of contraction",
                        "regulatory_environment": "uncertain classification as security or commodity",
                        "institutional_adoption": "growing but at slower pace than Bitcoin",
                        "correlation_with_bitcoin": "high at 0.82 coefficient"
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
            
            # More realistic random generation based on ticker characteristics
            ticker_type = "crypto" if "-USD" in ticker else ("norwegian" if ".OL" in ticker else "global")
            
            # Generate more plausible summary based on ticker type and sentiment
            summary_templates = {
                "bullish": {
                    "norwegian": f"AI analysis suggests a {strength} bullish outlook for {ticker} based on favorable Nordic economic conditions, strong financial position, and positive technical signals.",
                    "global": f"AI analysis suggests a {strength} bullish outlook for {ticker} based on robust earnings growth, market position strength, and positive technical momentum.",
                    "crypto": f"AI analysis suggests a {strength} bullish outlook for {ticker} based on increasing adoption, favorable on-chain metrics, and improving market sentiment."
                },
                "bearish": {
                    "norwegian": f"AI analysis suggests a {strength} bearish outlook for {ticker} due to Nordic economic headwinds, competitive pressures, and negative technical indicators.",
                    "global": f"AI analysis suggests a {strength} bearish outlook for {ticker} due to earnings concerns, valuation pressures, and deteriorating technical signals.",
                    "crypto": f"AI analysis suggests a {strength} bearish outlook for {ticker} due to regulatory uncertainties, weakening on-chain metrics, and negative market sentiment."
                },
                "neutral": {
                    "norwegian": f"AI analysis suggests a {strength} neutral outlook for {ticker} with balanced risk-reward, mixed technical signals, and stable Nordic market conditions.",
                    "global": f"AI analysis suggests a {strength} neutral outlook for {ticker} with balanced growth prospects, fair valuation, and mixed technical indicators.",
                    "crypto": f"AI analysis suggests a {strength} neutral outlook for {ticker} with balanced on-chain metrics, evolving regulatory environment, and consolidating price action."
                }
            }
            
            # Generate technical factors based on sentiment and ticker type
            technical_factors_templates = {
                "bullish": [
                    f"RSI at {random.randint(55, 69)}.{random.randint(1, 9)} shows building momentum without reaching overbought levels",
                    f"Price trading above both 50-day and 200-day moving averages, confirming uptrend",
                    f"Increasing volume on up days suggests institutional accumulation",
                    f"Recent breakout from {random.randint(2, 6)}-month consolidation pattern",
                    f"Higher lows pattern forming, indicating strengthening buyer interest"
                ],
                "bearish": [
                    f"RSI at {random.randint(30, 45)}.{random.randint(1, 9)} approaching oversold territory",
                    f"Price trading below key moving averages, confirming downtrend",
                    f"Decreasing volume on rallies suggests lack of conviction",
                    f"Lower highs and lower lows pattern established since {random.choice(['January', 'February', 'March', 'April', 'May', 'June'])}",
                    f"Death cross formed with 50-day moving average crossing below 200-day"
                ],
                "neutral": [
                    f"RSI at {random.randint(45, 55)}.{random.randint(1, 9)} indicates balanced momentum",
                    f"Price oscillating around key moving averages without clear direction",
                    f"Volume profile shows no clear accumulation or distribution patterns",
                    f"Price consolidating in range between support and resistance levels",
                    f"Bollinger Bands narrowing, suggesting potential volatility expansion ahead"
                ]
            }
            
            # Generate fundamental factors based on sentiment and ticker type
            fundamental_factors_templates = {
                "bullish": {
                    "norwegian": [
                        f"Strong financial position with healthy balance sheet metrics",
                        f"Dividend yield of {random.randint(3, 6)}.{random.randint(1, 9)}% with sustainable payout ratio",
                        f"Cost efficiency initiatives improving margins by {random.randint(1, 3)}.{random.randint(1, 9)} percentage points",
                        f"Revenue growth outpacing Nordic sector average by {random.randint(2, 8)}%",
                        f"Attractive valuation at {random.randint(8, 15)}x forward earnings"
                    ],
                    "global": [
                        f"Earnings growth of {random.randint(10, 25)}% year-over-year exceeding analyst expectations",
                        f"Strong market position in core segments with {random.randint(20, 40)}% share",
                        f"Operating margins expanding to {random.randint(25, 45)}% from investment in automation",
                        f"R&D pipeline showing promising results for future growth",
                        f"Balance sheet strength with {random.randint(10, 30)}B in cash reserves"
                    ],
                    "crypto": [
                        f"Growing adoption metrics with {random.randint(15, 40)}% increase in active addresses",
                        f"Improving tokenomics with supply reduction mechanisms",
                        f"Development activity increasing with new protocol upgrades",
                        f"Institutional interest growing through regulated investment vehicles",
                        f"Network security metrics at all-time highs"
                    ]
                },
                "bearish": {
                    "norwegian": [
                        f"Margin pressure from increased competition in Nordic markets",
                        f"Revenue declining by {random.randint(1, 5)}% year-over-year",
                        f"High dividend payout ratio of {random.randint(70, 90)}% may be unsustainable",
                        f"Rising operational costs offsetting efficiency initiatives",
                        f"Losing market share to more agile competitors"
                    ],
                    "global": [
                        f"Earnings missing consensus estimates by {random.randint(5, 15)}%",
                        f"Margin compression due to input cost inflation",
                        f"Market share erosion in key segments",
                        f"High valuation at {random.randint(25, 40)}x forward earnings",
                        f"Balance sheet concerns with {random.randint(10, 30)}B in debt maturing within 2 years"
                    ],
                    "crypto": [
                        f"Declining network activity with {random.randint(10, 30)}% reduction in transactions",
                        f"Regulatory headwinds increasing uncertainty",
                        f"Technical challenges delaying important protocol upgrades",
                        f"Increasing competition from alternative protocols",
                        f"Concentration risks with {random.randint(20, 40)}% held by top 10 addresses"
                    ]
                },
                "neutral": {
                    "norwegian": [
                        f"Stable revenue with {random.randint(0, 3)}% growth year-over-year",
                        f"Margins holding steady at {random.randint(20, 30)}%",
                        f"Dividend yield of {random.randint(3, 5)}% in line with sector average",
                        f"Market share stable in core Nordic markets",
                        f"Valuation in line with historical averages"
                    ],
                    "global": [
                        f"Earnings in line with analyst expectations",
                        f"Stable market position with no significant share changes",
                        f"Cost management offsetting moderate input price inflation",
                        f"R&D spending maintained at {random.randint(8, 15)}% of revenue",
                        f"Balance sheet metrics stable year-over-year"
                    ],
                    "crypto": [
                        f"Network metrics stable with balanced supply-demand dynamics",
                        f"Development continuing at steady pace",
                        f"Regulatory situation evolving but without immediate impact",
                        f"Correlation with broader crypto market at average levels",
                        f"Adoption metrics growing in line with market average"
                    ]
                }
            }
            
            # Generate economic indicators based on ticker type
            economic_indicators_templates = {
                "norwegian": {
                    "norwegian_economy": random.choice(["showing resilience with 2.1% GDP growth", "slowing with 1.3% GDP growth", "stable with 1.8% GDP forecast"]),
                    "interest_rate_environment": random.choice(["stable with Norges Bank holding rates", "challenging with potential rate increases", "favorable with potential rate cuts"]),
                    "sector_performance": f"{random.choice(['outperforming', 'underperforming', 'in line with'])} broader Oslo Børs index",
                    "currency_impact": f"NOK {random.choice(['strengthening', 'weakening', 'stable'])} against major trading partners"
                },
                "global": {
                    "global_economy": random.choice(["showing moderate growth at 3.2%", "facing headwinds with 2.5% growth", "resilient with 3.0% expansion"]),
                    "interest_rate_trend": random.choice(["declining with central banks easing", "rising with inflation concerns", "stabilizing after hiking cycle"]),
                    "sector_rotation": f"investors {random.choice(['favoring', 'rotating out of', 'neutral on'])} this sector",
                    "geopolitical_factors": random.choice(["presenting moderate risks", "generally supportive", "creating uncertainty"])
                },
                "crypto": {
                    "bitcoin_dominance": f"{random.randint(40, 60)}% and {random.choice(['increasing', 'decreasing', 'stable'])}",
                    "market_liquidity": random.choice(["improving with institutional participation", "declining with exchange outflows", "stable with balanced flows"]),
                    "regulatory_landscape": random.choice(["gradually clarifying", "presenting challenges", "mixed with regional differences"]),
                    "correlation_with_equities": random.choice(["high at 0.7 coefficient", "moderate at 0.5 coefficient", "declining to 0.3 coefficient"])
                }
            }
            
            # Build the analysis object with more realistic random data
            analysis = {
                "ticker": ticker,
                "sentiment": sentiment,
                "strength": strength,
                "summary": summary_templates[sentiment][ticker_type],
                "technical_factors": technical_factors_templates[sentiment],
                "fundamental_factors": fundamental_factors_templates[sentiment][ticker_type],
                "prediction": {
                    "direction": "up" if sentiment == "bullish" else ("down" if sentiment == "bearish" else "sideways"),
                    "confidence": 0.8 if strength == "strong" else (0.65 if strength == "moderate" else 0.4),
                    "time_frame": f"{random.choice(['short', 'medium', 'long'])} term ({random.choice(['1-3', '3-6', '6-12', '12-24'])} months)",
                    "target_price": f"${random.randint(5, 500)}" if not ticker.endswith('.OL') else f"{random.randint(50, 500)} NOK"
                },
                "economic_indicators": economic_indicators_templates[ticker_type],
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
        