import os
from telethon import TelegramClient
api_id = 23321997
api_hash = "3c0378a72f84d4dfe7d701bba5f3bbaa"
bot_token = "6307893638:AAHfJ_hTg_a9gTi6gyPO9E-VscPnsyhChCs"
skeleton_url = ""

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
skeleton_url = os.environ.get('SKELETON_URL')


bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


