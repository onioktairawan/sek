import os
import discord
from dotenv import load_dotenv
from telegram_handler import send_to_telegram

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
OWNER_ID = int(os.getenv("DISCORD_USER_ID"))

client = discord.Client()

@client.event
async def on_ready():
    print(f"[Discord] Logged in as {client.user}")

@client.event
async def on_ready():
    print(f"[Discord] Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.channel.id != DISCORD_CHANNEL_ID:
        print(f"[Discord] ❌ Channel tidak cocok: {message.channel.id}")
        return

    if message.author.id == OWNER_ID:
        print("[Discord] ❌ Abaikan pesan dari diri sendiri.")
        return

    author = f"{message.author.name}#{message.author.discriminator}"
    content = message.content or "[Pesan kosong]"
    is_reply = (
        message.reference is not None
        and message.reference.resolved is not None
        and getattr(message.reference.resolved, "author", None) is not None
        and message.reference.resolved.author.id == OWNER_ID
    ) or (f"<@{OWNER_ID}>" in content or f"<@!{OWNER_ID}>" in content)

    print(f"[Discord] Pesan masuk dari {author}: {content}")
    print(f"[Discord] Channel ID pesan: {message.channel.id}")

    try:
        result = await send_to_telegram(author, content, is_reply, str(message.id))
        if result:
            print("[Discord] ✅ Dikirim ke Telegram.")
        else:
            print("[Discord] ⚠️ Tidak berhasil kirim (tidak ada result).")
    except Exception as e:
        print(f"[Discord] ❌ Gagal kirim ke Telegram: {e}")

async def run_discord_bot():
    print("[Discord] Connecting...")
    await client.start(DISCORD_TOKEN)
