import asyncio
from telegram_handler import run_telegram_bot
from discord_handler import run_discord_bot

async def main():
    print("[Main] Memulai bot...")

    discord_task = asyncio.create_task(run_discord_bot())
    telegram_task = asyncio.create_task(run_telegram_bot())

    done, pending = await asyncio.wait(
        [discord_task, telegram_task],
        return_when=asyncio.FIRST_EXCEPTION
    )

    for task in done:
        if task.exception():
            print(f"[ERROR] Task gagal: {task.exception()}")
            for p in pending:
                p.cancel()
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Dihentikan oleh pengguna.")
