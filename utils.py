# utils.py

def format_discord_message(author, content, is_reply):
    return f"<b>{author}</b>\n{content}"

def format_telegram_reply(name, text):
    return text  # Hanya isi pesan saja, tanpa nama pengirim Telegram
