import logging
from Telegram.Config import bot, dp
from Telegram.Handlers import *
from aiogram import executor, types

register_handlers(dp)

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
