from Telegram.Config import bot, database, dp
from Units.Shopper import Shopper
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, InputMediaPhoto, MediaGroup
from Telegram.Keyboards.Keyboards import *


def register_admin_main_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(print_shoppers, commands='shoppers')
    dispatcher.register_message_handler(del_shopper, commands=['deleteshopper'])


async def print_shoppers(message: Message):
    user = database.get_user(message.from_user.id)
    if not user.is_admin:
        await bot.send_message(message.chat.id, 'Эта команда доступна только администратору')
        return

    shoppers = database.get_shoppers()
    if len(shoppers) == 0:
        await bot.send_message(message.chat.id, 'Шопперов не найденно')
        return

    shoppers_str = ''
    for shopper in shoppers:
        shoppers_str += f'{shopper.render_mini_profile()}\n'

    await bot.send_message(message.chat.id, shoppers_str)


async def del_shopper(message: Message):
    user = database.get_user(message.from_user.id)
    if not user.is_admin:
        await bot.send_message(message.chat.id, 'Эта команда доступна только администратору')
        return

    data = message.text.split(' ')
    print(f'data = {data}')
    if len(data) != 2:
        await bot.send_message(message.chat.id, 'Введите команду в формате:\n'
                                                '"/deleteshopper ID", где ID - id шопера который вы хотите удалить)')
        return

    shopper_id = data[1]
    if not shopper_id.isnumeric():
        await bot.send_message(message.chat.id, 'ID шоппера должно быть числом')
        return

    shoppers = [shopper for shopper in database.get_shoppers() if int(shopper.ID) == int(shopper_id)]
    if len(shoppers) < 1:
        await bot.send_message(message.chat.id, f'Шоппер с id {shopper_id} не найден')
        return

    shopper = shoppers[0]
    database.del_shopper(shopper)

    await bot.send_message(message.chat.id, f'Шоппер с id {shopper.ID} был удален')
    return

