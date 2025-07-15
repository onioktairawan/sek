import asyncio
from discord_handler import run_discord_bot
from telegram_handler import run_telegram_bot

async def main():
    print("[Main] Memulai bot...")

    tg_task = asyncio.create_task(run_telegram_bot())

    await asyncio.sleep(2)  # Pastikan telegram_bot siap

    dc_task = asyncio.create_task(run_discord_bot())

    await asyncio.gather(tg_task, dc_task)

if __name__ == "__main__":
    asyncio.run(main())
