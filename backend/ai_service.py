import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from utils.indicators import simple_moving_average, rsi, macd, bollinger_bands, adx

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("DEBUG: Gemini API Key NOT found in environment variables.")
else:
    print(f"DEBUG: Gemini API Key found: {api_key[:5]}...{api_key[-4:]}")
    genai.configure(api_key=api_key)

# Use a model that supports JSON mode or structured output if possible, 
# otherwise we'll use prompt engineering.
model = genai.GenerativeModel('gemini-2.0-flash')

async def getAIRecommendation(stock_data, fundamentals, news):
    """
    Analyzes stock data using Google Gemini to provide a recommendation.
    """
    # Calculate Technical Indicators
    tech_ind = {
        "SMA_20": simple_moving_average(stock_data, 20),
        "SMA_50": simple_moving_average(stock_data, 50),
        "SMA_200": simple_moving_average(stock_data, 200),
        "RSI": rsi(stock_data),
        "MACD": macd(stock_data),
        "Bollinger": bollinger_bands(stock_data),
        "ADX": adx(stock_data),
        "Volume_Trend": "Neutral" # Placeholder, could be improved
    }
    
    # Infer Volume Trend
    if len(stock_data) >= 20:
        avg_vol = sum(d.get('volume', 0) for d in stock_data[:20]) / 20
        curr_vol = stock_data[0].get('volume', 0)
        if curr_vol > avg_vol * 1.2:
            tech_ind["Volume_Trend"] = "High"
        elif curr_vol < avg_vol * 0.8:
            tech_ind["Volume_Trend"] = "Low"

    # Map Fundamentals
    fund_input = {
        "PE": fundamentals.get("pe_ratio"),
        "PB": fundamentals.get("price_to_book"),
        "ROE": fundamentals.get("return_on_equity"),
        "ROA": fundamentals.get("return_on_assets"),
        "EPS_Growth": fundamentals.get("quarterly_earnings_growth_yoy"),
        "Debt_to_Equity": fundamentals.get("debt_to_equity"),
        "Revenue_Growth": fundamentals.get("quarterly_revenue_growth_yoy"),
        "Profit_Margins": fundamentals.get("profit_margin")
    }

    # Format News
    news_input = [{"headline": n.get("title"), "sentiment": n.get("sentiment")} for n in news[:5]]

    # Infer Market Regime (Simple Heuristic)
    market_regime = "Sideways"
    if tech_ind["SMA_50"] and tech_ind["SMA_200"]:
        if tech_ind["SMA_50"] > tech_ind["SMA_200"]:
            market_regime = "Bull"
        else:
            market_regime = "Bear"

    prompt = f"""
    **EDUCATIONAL PURPOSE ONLY**: This analysis is a simulation for educational purposes.

    You are a **Decisive Financial Analysis Engine**. 
    Your goal is to provide a clear **Buy, Sell, or Hold** recommendation based on the weight of evidence.

    **INPUT DATA**:
    - **Price History**: {json.dumps(stock_data[:30])}
    - **Technical Indicators**: {json.dumps(tech_ind)}
    - **Fundamentals**: {json.dumps(fund_input)}
    - **News & Sentiment**: {json.dumps(news_input)}
    - **Context**: Sector Trend="Neutral", Market Regime="{market_regime}"

    **DECISION LOGIC (WEIGHTED RESOLUTION)**:
    1.  **Do NOT default to "Hold"** just because signals conflict. You MUST resolve the conflict.
    2.  **Trend Priority**: If the Medium-Term Trend (SMA50, MACD) is strong, follow the trend for the Recommendation (Buy/Sell).
    3.  **Fundamental Impact**: Use Fundamentals to adjust the **Confidence Score**, not to block the trade. 
        - *Example*: Strong Uptrend + Weak Fundamentals = **"Buy"** (with Low Confidence/Speculative warning).
        - *Example*: Strong Downtrend + Strong Fundamentals = **"Sell"** (Price action leads).
    4.  **"Hold" Criteria**: ONLY recommend "Hold" if the market is truly ranging/sideways (e.g., ADX < 20, Flat SMAs) with no clear directional bias.

    **SCORING GUIDE**:
    - **Strong Buy**: Bullish Trend + Bullish Fundamentals + Positive News.
    - **Buy**: Bullish Trend (even if Fundamentals are mixed).
    - **Sell**: Bearish Trend (even if Fundamentals are mixed).
    - **Strong Sell**: Bearish Trend + Bearish Fundamentals + Negative News.
    - **Hold**: Neutral Trend / Sideways Market.

    **OUTPUT FORMAT (STRICT JSON)**:
    {{
      "recommendation": "Strong Buy" | "Buy" | "Hold" | "Sell" | "Strong Sell",
      "confidence": 0.0 to 1.0,
      "reasoning": "Explain the decision. If signals conflict, explain why the Trend won out (e.g., 'Despite weak fundamentals, the strong technical breakout dictates a speculative Buy')."
    }}

    Return ONLY the JSON.
    """

    try:
        # Gemini generation
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        content = response.text
        print(f"DEBUG: Raw Gemini content: {content!r}")
        
        # Clean up markdown code blocks if present (though response_mime_type should handle it)
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)

    except Exception as e:
        print(f"AI recommendation error: {e}")
        # Return a default or error response
        return {
            "recommendation": "Hold",
            "confidence": 0.5,
            "reasoning": f"AI analysis failed due to an error: {str(e)}. Defaulting to 'Hold'."
        }