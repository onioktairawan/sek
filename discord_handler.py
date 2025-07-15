import discord
import os
from dotenv import load_dotenv
from bridge import send_to_telegram
from db import save_message, is_mention_or_reply
from telegram_handler import send_to_telegram


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
DISCORD_USER_ID = None

client = discord.Client()

@client.event
async def on_ready():
    global DISCORD_USER_ID
    DISCORD_USER_ID = client.user.id
    print(f"[Discord] Logged in as {client.user}")

@client.event
async def on_message(message):
    print(f"[Discord] Pesan masuk dari {message.author}: {message.content}")
    print(f"[Discord] Channel ID pesan: {message.channel.id}")

    if message.channel.id != DISCORD_CHANNEL_ID:
        print(f"[Discord] ❌ Channel tidak cocok: {message.channel.id}")
        return

    if message.author.id == client.user.id:
        print("[Discord] ❌ Abaikan pesan dari diri sendiri.")
        return

    try:
        is_reply = is_mention_or_reply(DISCORD_USER_ID, message)
        telegram_msg_id = await send_to_telegram(message.author.name, message.content, is_reply, message.id)
        save_message(str(message.id), telegram_msg_id, message.author.name, is_reply=is_reply)
        print("[Discord] ✅ Dikirim ke Telegram.")
    except Exception as e:
        print(f"[Discord] ❌ Gagal kirim ke Telegram: {e}")

async def run_discord_bot():
    print("[Discord] Connecting...")
    await client.start(DISCORD_TOKEN)
