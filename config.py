import os
from telethon import TelegramClient
api_id = 14560088
api_hash = "74a2665339484da3eaaed5f4fe16da79"
bot_token = "5524381543:AAH-s7TDhvA_Ng2k9U5z9pvgiRPy5ChNve8"
skeleton_url = ""
auth_users = 1925020999
auth_groups = -1001577326035

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
skeleton_url = os.environ.get('SKELETON_URL')
auth_users = os.environ.get('AUTH_USERS').split()
auth_groups = os.environ.get('AUTH_GROUPS').split()
for i in range(len(auth_users)):
    auth_users[i] = int(auth_users[i])
for i in range(len(auth_groups)):
    auth_groups[i] = int(auth_groups[i])

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


