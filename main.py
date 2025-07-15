import asyncio
from discord_handler import run_discord_bot
from telegram_handler import run_telegram_bot, telegram_bot

async def main():
    print("[Main] Memulai bot...")

    # Jalankan Telegram dan tunggu selesai start
    await run_telegram_bot()

    # Setelah telegram_bot siap, baru jalankan Discord
    await run_discord_bot()

if __name__ == "__main__":
    asyncio.run(main())
