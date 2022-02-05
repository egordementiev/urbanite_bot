from Telegram.Config import bot, database, dp, MANAGERS_IDS
from Units.Shopper import Shopper
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, InputMediaPhoto, MediaGroup
from Telegram.Keyboards.Keyboards import *


class UpdateShopperStates(StatesGroup):
    set_name = State()
    set_description = State()
    set_material = State()
    set_price = State()
    set_photo = State()
    next_photo = State()


def register_update_shopper_handlers(dispatcher: Dispatcher):
    print('register_shopper_shopper_handlers')
    dispatcher.register_message_handler(update_shopper, commands=['updateshopper'])
    dispatcher.register_message_handler(set_name, state=UpdateShopperStates.set_name)
    dispatcher.register_message_handler(set_name, state=UpdateShopperStates.set_name)
    # dispatcher.register_message_handler(set_description, state=UpdateShopperStates.set_description)
    # dispatcher.register_message_handler(set_material, state=UpdateShopperStates.set_material)
    # dispatcher.register_message_handler(set_price, state=UpdateShopperStates.set_price)
    # dispatcher.register_message_handler(set_photo, state=UpdateShopperStates.set_photo, content_types=['photo', 'text'])
    # # dispatcher.register_message_handler(set_photo, content_types=['photo'])
    # dispatcher.register_message_handler(next_photo, content_types=['photo'], state=UpdateShopperStates.next_photo)
    pass


def update_shopper(message: Message, state: FSMContext):
    await UpdateShopperStates.set_name.set()


def set_name(message: Message, state: FSMContext):
    pass