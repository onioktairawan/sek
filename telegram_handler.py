from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CallbackQueryHandler, MessageHandler, filters, CommandHandler
from dotenv import load_dotenv
import os
from db import get_discord_id_by_telegram_id
from utils import format_discord_message, format_telegram_reply
import discord_handler

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_ID = int(os.getenv("TELEGRAM_GROUP_ID"))

app = None
reply_map = {}

async def send_to_telegram(author, content, is_reply, discord_msg_id):
    global app
    keyboard = [[InlineKeyboardButton("\ud83d\udcac Balas", callback_data=f"reply|{discord_msg_id}")]]
    sent = await app.bot.send_message(
        chat_id=TELEGRAM_GROUP_ID,
        text=format_discord_message(author, content, is_reply),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return sent.message_id

async def handle_reply_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("reply|"):
        discord_msg_id = data.split("|")[1]
        reply_map[query.from_user.id] = discord_msg_id
        await query.message.reply_text("Silakan ketik balasan Anda:")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in reply_map:
        reply_to = reply_map.pop(user_id)
        text = update.message.text
        name = update.message.from_user.full_name
        discord_channel = discord_handler.client.get_channel(int(os.getenv("DISCORD_CHANNEL_ID")))
        if discord_channel:
            try:
                reply_msg = await discord_channel.fetch_message(reply_to)
                await reply_msg.reply(format_telegram_reply(name, text))
            except:
                await discord_channel.send(format_telegram_reply(name, text))

async def run_telegram_bot():
    global app
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CallbackQueryHandler(handle_reply_button))
    app.add_handler(MessageHandler(filters.TEXT & filters.Chat(TELEGRAM_GROUP_ID), handle_text))
    await app.start()
    print("[Telegram] Bot started")
    await app.updater.start_polling()
