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
    set_next_photo = State()


def register_update_shopper_handlers(dispatcher: Dispatcher):
    print('register_shopper_shopper_handlers')
    dispatcher.register_message_handler(update_shopper, commands=['updateshopper'])
    dispatcher.register_message_handler(set_name, state=UpdateShopperStates.set_name)
    dispatcher.register_message_handler(set_name, commands=['/skip'], state=UpdateShopperStates.set_name)
    dispatcher.register_message_handler(set_description, state=UpdateShopperStates.set_description)
    dispatcher.register_message_handler(set_description, commands=['/skip'], state=UpdateShopperStates.set_description)
    dispatcher.register_message_handler(set_material, state=UpdateShopperStates.set_material)
    dispatcher.register_message_handler(set_material, commands=['/skip'], state=UpdateShopperStates.set_material)
    dispatcher.register_message_handler(set_price, state=UpdateShopperStates.set_price)
    dispatcher.register_message_handler(set_price, commands=['/skip'], state=UpdateShopperStates.set_price)
    dispatcher.register_message_handler(set_photo, state=UpdateShopperStates.set_photo, content_types=['photo', 'text'])
    dispatcher.register_message_handler(set_photo, state=UpdateShopperStates.set_photo, commands=['/skip'])
    # # dispatcher.register_message_handler(set_photo, content_types=['photo'])
    dispatcher.register_message_handler(set_next_photo, content_types=['photo', 'text'],
                                        state=UpdateShopperStates.set_next_photo)
    dispatcher.register_message_handler(set_next_photo, state=UpdateShopperStates.set_next_photo, commands=['/skip'])


async def update_shopper(message: Message, state: FSMContext):
    try:
        user = [user for user in database.get_users() if str(user.ID) == str(message.from_user.id)][0]
    except:
        await bot.send_message(message.chat.id, 'Эта команда доступна только администратору')
        return

    if not user.is_admin:
        await bot.send_message(message.chat.id, 'Эта команда доступна только администратору')
        return

    split_msg = message.text.split(' ')
    if len(split_msg) != 2 or not split_msg[1].isnumeric():
        await bot.send_message(message.chat.id, 'Некоректно написаная команда, введите:\n'
                                                '"/updateshopper id_шоппера(это число)"')

    shopper_id = split_msg[1]
    shoppers = [shopper for shopper in database.get_shoppers() if int(shopper.ID) == int(shopper_id)]
    if len(shoppers) < 1:
        await bot.send_message(message.chat.id, f'Шоппер с id {shopper_id} не найден')
        return

    shopper = shoppers[0]
    print(shopper)
    await state.update_data(shopper=shopper)
    await bot.send_message(message.chat.id, 'Введите новое название для шоппера, или '
                                            '/skip, что бы оставить как есть', reply_markup=cancel_keyboard())
    await UpdateShopperStates.set_name.set()


async def set_name(message: Message, state: FSMContext):
    if message.text == '/skip':
        await bot.send_message(message.chat.id, 'Введите новое описание для шоппера, или '
                                                '/skip, что бы оставить как есть', reply_markup=cancel_keyboard())
        await UpdateShopperStates.set_description.set()
        return

    state_data = await state.get_data()
    shopper = state_data.get('shopper')

    shopper.title = message.text
    print(shopper)
    await state.update_data(shopper=shopper)
    await bot.send_message(message.chat.id, 'Введите новое описание для шоппера, или '
                                            '/skip, что бы оставить как есть', reply_markup=cancel_keyboard())
    await UpdateShopperStates.set_description.set()


async def set_description(message: Message, state: FSMContext):
    if message.text == '/skip':
        await bot.send_message(message.chat.id, 'Введите новые материалы для шоппера, или '
                                                '/skip, что бы оставить как есть', reply_markup=cancel_keyboard())
        await UpdateShopperStates.set_material.set()
        return

    state_data = await state.get_data()
    shopper = state_data.get('shopper')

    shopper.description = message.text
    print(shopper)
    await state.update_data(shopper=shopper)
    await bot.send_message(message.chat.id, 'Введите новые материалы для шоппера, или '
                                            '/skip, что бы оставить как есть', reply_markup=cancel_keyboard())
    await UpdateShopperStates.set_material.set()


async def set_material(message: Message, state: FSMContext):
    if message.text == '/skip':
        await bot.send_message(message.chat.id, 'Введите новую цену шоппера, или '
                                                '/skip, что бы оставить как есть', reply_markup=cancel_keyboard())
        await UpdateShopperStates.set_price.set()
        return

    state_data = await state.get_data()
    shopper = state_data.get('shopper')

    shopper.material = message.text
    print(shopper)
    await state.update_data(shopper=shopper)
    await bot.send_message(message.chat.id, 'Введите новую цену шоппера, или '
                                            '/skip, что бы оставить как есть', reply_markup=cancel_keyboard())
    await UpdateShopperStates.set_price.set()


async def set_price(message: Message, state: FSMContext):
    if message.text == '/skip':
        await bot.send_message(message.chat.id, 'Отправьте новую фотографию для шоппера, или '
                                                '/skip, что бы оставить как есть', reply_markup=cancel_keyboard())
        await UpdateShopperStates.set_photo.set()
        return

    state_data = await state.get_data()
    shopper = state_data.get('shopper')

    shopper.price = message.text
    print(shopper)
    await state.update_data(shopper=shopper)
    await bot.send_message(message.chat.id, 'Отправьте новую фотографию для шоппера, или '
                                            '/skip, что бы оставить как есть', reply_markup=cancel_keyboard())
    await UpdateShopperStates.set_photo.set()


async def set_photo(message: Message, state: FSMContext):
    if message.text == '/skip':
        state_data = await state.get_data()
        shopper = state_data.get('shopper')
        print(f'shopper = {shopper}')
        database.update_shopper(shopper)
        await bot.send_message(message.chat.id, 'Шоппер был обновлен', reply_markup=cancel_keyboard())
        await state.reset_state()
        return

    if not message.content_type == 'photo':
        await bot.send_message(message.chat.id, 'Отправьте фотографию!', reply_markup=cancel_keyboard())
        await UpdateShopperStates.set_photo.set()
        return

    state_data = await state.get_data()
    shopper = state_data.get('shopper')

    shopper.photos = [message.photo[0].file_id]
    await state.update_data(shopper=shopper)
    await bot.send_message(message.chat.id, 'Отправьте следующию фотографию', reply_markup=cancel_keyboard())
    await UpdateShopperStates.set_next_photo.set()


async def set_next_photo(message: Message, state: FSMContext):
    if message.text == '/skip':
        state_data = await state.get_data()
        shopper = state_data.get('shopper')

        if len(shopper.photos) < 2:
            await bot.send_message(message.chat.id, 'Недостаточно фотографий, отправьте еще хотя бы одну фотографию')
            return

        database.update_shopper(shopper)
        await bot.send_message(message.chat.id, 'Шоппер был обновлен')
        await state.reset_state()
        return

    if not message.content_type == 'photo':
        await bot.send_message(message.chat.id, 'Отправьте фотографию!', reply_markup=cancel_keyboard())
        await UpdateShopperStates.set_photo.set()
        return

    state_data = await state.get_data()
    shopper = state_data.get('shopper')

    shopper.photos.append(message.photo[0].file_id)
    await state.update_data(shopper=shopper)
    await bot.send_message(message.chat.id, 'Отправьте следующию фотографию, или /skip что бы сохранить изменения',
                           reply_markup=cancel_keyboard())
    await UpdateShopperStates.set_next_photo.set()
