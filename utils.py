def format_discord_message(author, content, is_reply):
    prefix = "\ud83d\udd01 Balasan untuk Anda" if is_reply else "\ud83d\udce9 Pesan Baru"
    return f"{prefix}\n\n\ud83d\udc64 <b>{author}</b>\n{content}"


def format_telegram_reply(name, text):
    return f"{name} membalas:\n{text}"
