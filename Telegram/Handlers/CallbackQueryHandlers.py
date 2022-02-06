from Telegram.Handlers.MainMenuClient.MainMenuClientHandlers import *
from Telegram.Handlers.MainMenuClient.CheckoutClientHandlers import *
from Telegram.Handlers.MainMenuAdmin.AddShopper import *
from aiogram.types import CallbackQuery


async def callback_handlers(call: CallbackQuery, state: FSMContext):
    if call.data in ['contacts']:
        await contacts(call.message)

    elif call.data.startswith('add_to_cart_id_'):
        pass

    elif call.data.startswith('shopper_left_id'):
        ID = int(call.data.split('=')[-1])
        print(ID)
        await slide_shopper_left(call.message, ID)

    elif call.data.startswith('shopper_right_id'):
        ID = int(call.data.split('=')[-1])
        print(f'ID = {ID}')
        await slide_shopper_right(call.message, ID)

    elif call.data == 'save_shopper':
        await save_shopper(call.message, state)

    elif call.data.startswith('more_photo'):
        ID = int(call.data.split('=')[-1])
        print(f'ID = {ID}')
        await more_photo(call.message, ID)

    elif call.data.startswith('add_to_cart_id'):
        ID = int(call.data.split('=')[-1])
        print(f'ID = {ID}')
        await bot.answer_callback_query(call.id, 'Добавлено в корзину')
        await add_to_cart(call.from_user.id, ID)

    elif call.data.startswith('empty_cart_id'):
        ID = int(call.data.split('=')[-1])
        print(f'ID = {ID}')
        await empty_cart(call.message, ID)
        await bot.answer_callback_query(call.id, 'Корзина очищена')

    elif call.data.startswith('checkout_id'):
        ID = int(call.data.split('=')[-1])
        print(f'ID = {ID}')
        await checkout_init(call.message, state, ID)

    elif call.data in ['cancel']:
        await state.reset_state()
        await bot.edit_message_text('Операция была отменина', call.message.chat.id, call.message.message_id)
        await bot.answer_callback_query(call.id, 'Операция была отменена')

