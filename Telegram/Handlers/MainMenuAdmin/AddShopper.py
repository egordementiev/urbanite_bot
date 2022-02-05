from Telegram.Config import bot, database, dp, MANAGERS_IDS
from Units.Shopper import Shopper
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, InputMediaPhoto, MediaGroup
from Telegram.Keyboards.Keyboards import *


class AddShopperStates(StatesGroup):
    set_name = State()
    set_description = State()
    set_material = State()
    set_price = State()
    set_photo = State()
    next_photo = State()


def register_add_shopper_handlers(dispatcher: Dispatcher):
    print('register_add_shopper_handlers')
    dispatcher.register_message_handler(add_shopper, commands=['addshopper'], state='*')
    dispatcher.register_message_handler(set_name, state=AddShopperStates.set_name)
    dispatcher.register_message_handler(set_description, state=AddShopperStates.set_description)
    dispatcher.register_message_handler(set_material, state=AddShopperStates.set_material)
    dispatcher.register_message_handler(set_price, state=AddShopperStates.set_price)
    dispatcher.register_message_handler(set_photo, state=AddShopperStates.set_photo, content_types=['photo', 'text'])
    # dispatcher.register_message_handler(set_photo, content_types=['photo'])
    dispatcher.register_message_handler(next_img, content_types=['photo'], state=AddShopperStates.next_photo)


async def add_shopper(message: Message):
    print('add_shopper')
    try:
        users = [user for user in database.get_users() if str(user.ID) ==  str(message.chat.id)]
        print(users)
        user = users[0]
    except:
        print('except')
        await bot.send_message(message.chat.id, 'Эта функция доступная только администратору')
        return

    print(f'user.ID = {[str(user.ID)]}, MANAGERS_IDS = {MANAGERS_IDS}')
    if str(user.ID) not in MANAGERS_IDS:
        await bot.send_message(message.chat.id, 'Эта функция доступная только администратору')
        return

    msg = await bot.send_message(message.chat.id, 'Введите название шопера:', reply_markup=cancel_keyboard())
    # dp.register_next_step_handler(msg, set_name)
    await AddShopperStates.set_name.set()
    print('next step handler registered')


async def set_name(message: Message, state: FSMContext):
    print('add_shopper-set_name')
    shopper = Shopper(title=message.text)
    await state.update_data(shopper=shopper)
    await bot.send_message(message.chat.id, 'Введите описание шопера:', reply_markup=cancel_keyboard())
    # dp.register_next_step_handler_by_chat_id(message.chat.id, set_description, shopper)
    await AddShopperStates.set_description.set()


async def set_description(message: Message, state: FSMContext):
    print('add_shopper-set_description')
    data = await state.get_data()
    shopper = data.get("shopper")
    shopper.description = message.text
    print(f'shopper(func = set_description) = {shopper}')
    await state.update_data(shopper=shopper)
    await bot.send_message(message.chat.id, 'Введите материал шопера:', reply_markup=cancel_keyboard())
    # dp.register_next_step_handler_by_chat_id(message.chat.id, set_name, shopper)
    await AddShopperStates.set_material.set()


async def set_material(message: Message, state: FSMContext):
    print('add_shopper-set_material')
    data = await state.get_data()
    print(data.get("shopper"))
    shopper = data.get("shopper")
    shopper.material = message.text
    print(f'shopper(func = set_material) = {shopper}')
    await state.update_data(shopper=shopper)
    await bot.send_message(message.chat.id, 'Введите цену шопера:', reply_markup=cancel_keyboard())
    # dp.register_next_step_handler_by_chat_id(message.chat.id, set_price, shopper)
    await AddShopperStates.set_price.set()


async def set_price(message: Message, state: FSMContext):
    print('add_shopper-set_price')
    data = await state.get_data()
    print(data.get("shopper"))
    shopper = data.get("shopper")
    if not message.text.isnumeric():
        await bot.send_message(message.chat.id, 'Введите цену шопера (Это должно быть целое число):'
                               , reply_markup=cancel_keyboard())
        # dp.register_next_step_handler_by_chat_id(message.chat.id, set_price, shopper)
        await AddShopperStates.set_price.set()
        return

    shopper.price = int(message.text)
    print(f'shopper(func = set_price) = {shopper}')
    await state.update_data(shopper=shopper)

    await bot.send_message(message.chat.id, 'Отправьте фотографию шопера:', reply_markup=cancel_keyboard())
    # dp.register_next_step_handler_by_chat_id(message.chat.id, set_photo, shopper)
    await AddShopperStates.set_photo.set()


async def set_photo(message: Message, state: FSMContext):
    print('add_shopper-set_photo')
    print(message)
    data = await state.get_data()
    print(data.get("shopper"))
    shopper = data.get("shopper")
    if not message.content_type == 'photo':
        await bot.send_message(message.chat.id, 'Отправьте фотографию!', reply_markup=cancel_keyboard())
        # dp.register_next_step_handler_by_chat_id(message.chat.id, set_photo)
        await AddShopperStates.set_photo.set()
        return

    # photos = [InputMediaPhoto(media=message.photo[-1].file_id, caption=shopper.render_big_profile())]
    # photos = [InputMediaPhoto(media=message.photo[1].file_id, caption=shopper.render_big_profile())]
    # photos = [InputMediaPhoto(media=message.media_group_id, caption=shopper.render_big_profile())]
    photos = message.photo
    shopper.photos = [photos[0].file_id]
    print(f'shopper(func = set_photo) = {shopper}')
    await state.update_data(shopper=shopper)
    await bot.send_message(message.chat.id, 'Фото успешно добавленно, отправьте следующее:',
                           reply_markup=add_shopper_keyboard())

    await AddShopperStates.next_photo.set()


async def next_img(message: Message, state: FSMContext):
    print('add_shopper-next_img')
    data = await state.get_data()
    print(data.get("shopper"))
    shopper = data.get("shopper")
    if len(shopper.photos) >= 8:
        shopper.photo.append(message.photo[-1].file_id)
        print(f'shopper(func = next_img(финал)) = {shopper}')
        await bot.send_message(message.chat.id, 'Максимальное количество фотографий задано, '
                               'шоппер сохранен в базу данных, '
                               'вот как выглядет его страница:')
        database.add_shopper(shopper)
        await state.finish()
        return

    shopper.photos.append(message.photo[-1].file_id)
    print(f'shopper(func = next_img) = {shopper}')
    await state.update_data(shopper=shopper)

    await bot.send_message(message.chat.id, 'Фото успешно добавленно, отправьте следующее:',
                           reply_markup=add_shopper_keyboard())


async def save_shopper(message: Message, state: FSMContext):
    data = await state.get_data()
    shopper = data.get("shopper")
    print(shopper)
    database.add_shopper(shopper)
    await bot.send_message(message.chat.id, 'Шоппер успешно добавлен в каталог')
    await state.finish()
