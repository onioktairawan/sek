from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils import format_discord_message
import telegram_handler

async def send_to_telegram(author, content, is_reply, discord_msg_id):
    keyboard = [[InlineKeyboardButton("💬 Balas", callback_data=f"reply|{discord_msg_id}")]]
    sent = await telegram_handler.app.bot.send_message(
        chat_id=telegram_handler.TELEGRAM_GROUP_ID,
        text=format_discord_message(author, content, is_reply),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return sent.message_id
