import os
from telethon import TelegramClient
api_id = 14560088
api_hash = "74a2665339484da3eaaed5f4fe16da79"
bot_token = "5503878652:AAFPZWeZ0q_PAPub8JO3nOQxVCi5lmaGl3A"
skeleton_url = ""

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
skeleton_url = os.environ.get('SKELETON_URL')


bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


