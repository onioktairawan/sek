import asyncio
import logging
from telegram_handler import run_telegram_bot
from discord_handler import run_discord_bot

logging.basicConfig(
    level=logging.INFO,
    filename="bridge.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def main():
    await asyncio.gather(
        run_discord_bot(),
        run_telegram_bot()
    )

if __name__ == "__main__":
    asyncio.run(main())
