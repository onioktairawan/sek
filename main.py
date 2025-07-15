import asyncio
from discord_handler import run_discord_client
from telegram_handler import run_telegram_bot

async def main():
    print("[Main] Memulai bot...")

    # Jalankan Telegram bot dulu supaya telegram_bot siap
    tg_task = asyncio.create_task(run_telegram_bot())

    # Delay kecil untuk memastikan telegram_bot sudah ter-set
    await asyncio.sleep(2)

    # Jalankan Discord client setelahnya
    dc_task = asyncio.create_task(run_discord_client())

    await asyncio.gather(tg_task, dc_task)

if __name__ == "__main__":
    asyncio.run(main())
