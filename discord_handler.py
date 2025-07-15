import discord
from discord.ext import tasks
from dotenv import load_dotenv
import os
from telegram_handler import send_to_telegram
from db import save_message, is_mention_or_reply

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
    if message.channel.id != DISCORD_CHANNEL_ID or message.author.id == client.user.id:
        return

    is_reply = is_mention_or_reply(DISCORD_USER_ID, message)
    telegram_msg_id = await send_to_telegram(message.author.name, message.content, is_reply, message.id)
    save_message(str(message.id), telegram_msg_id, message.author.name, is_reply=is_reply)

def run_discord_bot():
    return client.start(DISCORD_TOKEN)

