import asyncio
from discord_handler import run_discord_bot  # gunakan nama fungsi yang benar
from telegram_handler import run_telegram_bot

async def main():
    print("[Main] Memulai bot...")

    # Jalankan Telegram bot dulu supaya telegram_bot siap
    tg_task = asyncio.create_task(run_telegram_bot())

    # Delay kecil untuk memastikan telegram_bot sudah ter-set
    await asyncio.sleep(2)

    # Jalankan Discord bot setelah itu
    dc_task = asyncio.create_task(run_discord_bot())

    await asyncio.gather(tg_task, dc_task)

if __name__ == "__main__":
    asyncio.run(main())
