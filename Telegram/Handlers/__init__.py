from aiogram import Dispatcher
from Telegram.Handlers.OtherHandlers import *
from Telegram.Handlers.MainMenuClient.MainMenuClientHandlers import *
from Telegram.Handlers.MainMenuAdmin.MainMenuAdminHandlers import *
from Telegram.Handlers.MainMenuAdmin.AddShopper import *
from Telegram.Handlers.TextHandlers import *
from Telegram.Handlers.CallbackQueryHandlers import *


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start, commands=['start'])
    dispatcher.register_message_handler(contacts, commands=['contacts'])
    dispatcher.register_message_handler(delivery, commands=['delivery'])
    dispatcher.register_message_handler(catalog, commands=['shop', 'catalog'])
    dispatcher.register_message_handler(cart, commands=['cart'])
    dispatcher.register_message_handler(add_shopper, commands=['addshopper'], state='*')
    register_add_shopper_handlers(dispatcher)
    register_checkout_handlers(dispatcher)
    register_admin_main_handlers(dispatcher)
    dispatcher.register_message_handler(text_handler, content_types=['text'], state='*')
    dispatcher.register_callback_query_handler(callback_handlers, state='*')
