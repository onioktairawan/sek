import asyncio
from telegram_handler import run_telegram_bot
from discord_handler import run_discord_bot

async def main():
    print("[Main] Memulai bot...")
    await asyncio.gather(
        run_discord_bot(),
        run_telegram_bot()
    )

if __name__ == "__main__":
    asyncio.run(main())
