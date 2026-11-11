
import asyncio
import json
import os
import websockets

from bot import analyze_token

WS_URL = "wss://pumpportal.fun/api/data"

# Limit AI calls to control API costs.
MAX_AI_CHECKS = 5
ai_checks = 0

async def scan_tokens():
    global ai_checks

    print("Connecting to Pump.fun...")

    async with websockets.connect(WS_URL) as ws:
        await ws.send(json.dumps({
            "method": "subscribeNewToken"
        }))

        print("ChatGPT token scanner connected!")

        async for message in ws:
            try:
                token = json.loads(message)
                if not isinstance(token, dict):
                    continue

                mint = token.get("mint")
                if not mint:
                    continue

                print("Found token:", mint)

                # No verified market-risk data yet.
                # Therefore, do not execute any buys.
                if ai_checks >= MAX_AI_CHECKS:
                    print("AI check limit reached.")
                    break

                ai_checks += 1

                try:
                    result = await asyncio.to_thread(
                        analyze_token, token
                    )
                    print("AI analysis:", result)

                except Exception as error:
                    print("AI unavailable; skipping.")
                    continue

                print("TRADE DISABLED: analysis only")

            except (ValueError, TypeError):
                continue

if __name__ == "__main__":
    asyncio.run(scan_tokens())
