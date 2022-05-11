import re
from translation import LuciferMoringstar

id_pattern = re.compile(r'^.\d+$')


def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "on"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "off"]:
        return False
    else:
        return default


# ==================================
API_ID = 7769505
API_HASH = '33f551652408cce07cf7e7621560021a'
B_KEYS = '2037096447:AAFWSo_F_u1wPrGSjNdQ4TQ8t2ZgjT9wLxM'
START_MSG = LuciferMoringstar.DEFAULT_MSG
BOT_PICS = ['bot.png']
SUPPORT = "t.me/Gavindu_Tharaka"
SPELL_MODE = is_enabled('', True)
SET_SPEL_M = LuciferMoringstar.SPELL_CHECK
LOG_CHANNEL = -1001774917523
DATABASE_URI = 'mongodb+srv://GavinduTharaka:Gavindu123@sinhalasubdownbot.1v9ix.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
FORCE = '-1001590852342'
CUSTOM_FILE_CAPTION = None
DEV_NAME = 'Gavindu Tharaka'
ADMINS = [1376213565]
CHANNELS = []
AUTH_GROUPS = []
auth_users = []

# ==================================
# Empty 😂
COLLECTION_NAME = 'Telegram_files'
CACHE_TIME = 300
USE_CAPTION_FILTER = True
BUTTONS = {}
CURRENT = 2
CANCEL = False
FORCES_SUB = int(FORCE) if FORCE and id_pattern.search(FORCE) else FORCE
DATABASE_NAME = 'SSD_DATABASE'
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
DATABASE_CHANNELS = []

# ==================================
# About Bot 🤖
class bot_info(object):
    BOT_NAME = 'Sinhala Sub Down Bot'
    BOT_USERNAME = 'SinhalaSubDown_Bot'
    BOT_ID = 2037096447
