from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
from dotenv import load_dotenv
import os
from utils import format_telegram_reply

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_ID = int(os.getenv("TELEGRAM_GROUP_ID"))

reply_map = {}
telegram_bot = None  # Akan diisi oleh wrapper

# === Wrapper untuk dipanggil dari Discord ===
class TelegramBotWrapper:
    def __init__(self, application, group_chat_id):
        self.app = application
        self.group_chat_id = group_chat_id

    async def send_message(self, text, reply_to_message_id=None, reply_markup=None):
        return await self.app.bot.send_message(
            chat_id=self.group_chat_id,
            text=text,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

def build_keyboard(discord_message_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Balas", callback_data=f"reply|{discord_message_id}")]
    ])

async def send_to_telegram(author, content, is_reply, discord_message_id):
    global telegram_bot
    if telegram_bot is None:
        print("[Bridge] ❌ Gagal kirim ke Telegram: telegram_bot belum siap")
        return None

    try:
        text = f"<b>{author}</b>\n{content}"
        keyboard = build_keyboard(discord_message_id)

        msg = await telegram_bot.send_message(text=text, reply_markup=keyboard)
        return msg.message_id
    except Exception as e:
        print(f"[Bridge] ❌ Gagal kirim ke Telegram: {e}")
        return None

# === Handler reply balasan dari Telegram ke Discord ===
async def handle_reply_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("reply|"):
        discord_msg_id = data.split("|")[1]
        reply_map[query.from_user.id] = {
            "discord_msg_id": discord_msg_id,
            "telegram_msg_id": query.message.message_id
        }
        await query.message.reply_text("Silakan ketik balasan Anda:")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in reply_map:
        data = reply_map.pop(user_id)
        reply_to = data["discord_msg_id"]
        text = update.message.text

        from discord_handler import client
        discord_channel = client.get_channel(int(os.getenv("DISCORD_CHANNEL_ID")))
        if discord_channel:
            try:
                reply_msg = await discord_channel.fetch_message(reply_to)
                await reply_msg.reply(text)
            except:
                await discord_channel.send(text)

async def run_telegram_bot():
    global telegram_bot
    print("[Telegram] Bot starting...")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CallbackQueryHandler(handle_reply_button))
    app.add_handler(MessageHandler(filters.TEXT & filters.Chat(TELEGRAM_GROUP_ID), handle_text))

    telegram_bot = TelegramBotWrapper(app, TELEGRAM_GROUP_ID)

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
