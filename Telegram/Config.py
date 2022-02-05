from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Units.DataBase import SQLAlchemy


MANAGERS_IDS = ['981881436', '604008726']
MANAGER_ID = MANAGERS_IDS[1]


TOKEN = '5193197247:AAF1EkmzegWMFfMC2vnoBTCZyhtGlUvkSXc'
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

database = SQLAlchemy()

# '604008726 - id rachka'
