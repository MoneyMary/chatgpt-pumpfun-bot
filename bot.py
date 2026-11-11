# chatgpt-pumpfun-bot
AI-powered Pump.fun trading bot

import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

MAX_TRADE_USD = 1.00
MAX_POSITIONS = 2
LIVE_TRADING = False

def analyze_token(token):
    prompt = {
        "token": token,
        "max_trade_usd": MAX_TRADE_USD,
        "instructions": "Evaluate risk. Skip if data is missing."
    }

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "You are a cautious token risk analyzer. "
            "Return JSON only, with keys action, reason. "
            "action must be BUY, SELL, or SKIP. "
            "Never assume missing market data is safe. "
            "This is an analysis signal, not a trade."
        ),
        input=json.dumps(prompt),
    )

    try:
        result = json.loads(response.output_text)
        action = result.get("action", "SKIP")
        if action not in ("BUY", "SELL", "SKIP"):
            action = "SKIP"
        return {
            "action": action,
            "reason": str(result.get("reason", ""))[:300]
        }
    except (ValueError, TypeError):
        return {
            "action": "SKIP",
            "reason": "Invalid AI response"
        }

if __name__ == "__main__":
    print("Pump.fun AI bot initialized")
    print("Live trading:", LIVE_TRADING)
    print("Maximum trade: $", MAX_TRADE_USD)
