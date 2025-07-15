import asyncio
import logging
from telegram_handler import run_telegram_bot
from discord_handler import run_discord_bot

logging.basicConfig(level=logging.INFO, filename="bridge.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(run_discord_bot())
    loop.create_task(run_telegram_bot())
    loop.run_forever()
