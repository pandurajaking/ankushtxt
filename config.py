import os
from telethon import TelegramClient
API_ID = 14560088
API_HASH = "74a2665339484da3eaaed5f4fe16da79"
BOT_TOKEN = "5524381543:AAH-s7TDhvA_Ng2k9U5z9pvgiRPy5ChNve8"
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')


bot = TelegramClient("bot", api_id = API_ID, api_hash = API_HASH,bot_token = BOT_TOKEN)

