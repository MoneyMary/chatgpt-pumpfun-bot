
import asyncio
import json
import websockets

WS_URL = "wss://pumpportal.fun/api/data"

async def scan_tokens():
    print("Connecting to Pump.fun token feed...")

    async with websockets.connect(
        WS_URL,
        ping_interval=20
    ) as ws:
        await ws.send(json.dumps({
            "method": "subscribeNewToken"
        }))

        print("Scanner connected. Watching new tokens.")

        async for message in ws:
            try:
                token = json.loads(message)

                if not isinstance(token, dict):
                    continue

                mint = token.get("mint")
                name = token.get("name")
                symbol = token.get("symbol")

                if not mint:
                    continue

                print(
                    f"NEW TOKEN: {name} "
                    f"(${symbol}) | Mint: {mint}"
                )

            except (ValueError, TypeError) as error:
                print("Invalid token message:", error)

if __name__ == "__main__":
    asyncio.run(scan_tokens())
