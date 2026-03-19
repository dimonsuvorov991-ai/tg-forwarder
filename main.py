from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session = os.getenv("SESSION")

source_channel = os.getenv("SOURCE")
target_channel = os.getenv("TARGET")

client = TelegramClient(StringSession(session), api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    try:
        await client.forward_messages(target_channel, event.message)
    except Exception as e:
        print(e)

client.start()
print("Bot started...")
client.run_until_disconnected()
