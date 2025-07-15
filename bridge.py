from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_handler import telegram_bot

def build_keyboard(discord_message_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Balas", callback_data=f"reply|{discord_message_id}")]
    ])

async def send_to_telegram(author, content, is_reply, discord_message_id):
    try:
        prefix = "Balasan untuk Anda:" if is_reply else "Pesan Baru:"
        text = f"👤 {author}\n{prefix}\n{content}"
        keyboard = build_keyboard(discord_message_id)

        msg = await telegram_bot.send_message(
            chat_id=telegram_bot.group_chat_id,
            text=text,
            reply_markup=keyboard
        )
        return msg.message_id
    except Exception as e:
        print(f"[Bridge] ❌ Gagal kirim ke Telegram: {e}")
        return None
