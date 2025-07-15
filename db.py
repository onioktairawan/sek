from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.discord_telegram_bridge
messages = db.messages

def save_message(discord_id, telegram_id, author, is_reply=False):
    messages.insert_one({
        "discord_id": discord_id,
        "telegram_id": telegram_id,
        "author": author,
        "is_reply": is_reply
    })

def get_discord_id_by_telegram_id(telegram_id):
    data = messages.find_one({"telegram_id": telegram_id})
    return data["discord_id"] if data else None

def is_mention_or_reply(discord_user_id, msg):
    return (msg.reference is not None or f"<@{discord_user_id}>" in msg.content)
