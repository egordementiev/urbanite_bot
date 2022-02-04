from Telegram.Config import bot, database, MANAGER_ID
from Telegram.Keyboards.Keyboards import *
from aiogram.types import InputMedia, InputMediaPhoto, Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher import Dispatcher


class CheckoutStates(StatesGroup):
    set_phone = State()
    set_email = State()
    set_post = State()
    post_courier = State()
    pickup = State()


class Checkout:
    def __init__(self, user):
        self.user = user
        self.phone = 0
        self.email = ''
        self.post = ''
        self.post_address = ''

    def render(self):
        cart = self.user.cart
        text = f'Номер телефона: {self.phone}\n' \
               f'Email: {self.email}\n' \
               f'Доставка: {self.post}'
        if self.post_address:
            text += f'\nОтделение/адрес: {self.post_address}'
        text += '\n⬇️ Товары ⬇️:'
        return [cart, text]


def register_checkout_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(checkout_set_phone, state=CheckoutStates.set_phone)
    dispatcher.register_message_handler(checkout_set_email, state=CheckoutStates.set_email)
    dispatcher.register_callback_query_handler(checkout_set_post, run_task=lambda call: call.data.startswith('post'),
                                               state=CheckoutStates.set_post)
    dispatcher.register_message_handler(checkout_post_address, state=CheckoutStates.post_courier)


async def checkout_init(message: Message, state: FSMContext, user_id):
    await bot.send_message(message.chat.id, 'Введите ваш номер телефона:', reply_markup=cancel_keyboard())
    await CheckoutStates.first()
    user = database.get_user(user_id)
    checkout = Checkout(user)
    await state.update_data(checkout=checkout)


async def checkout_set_phone(message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Введите вашу электронную почту:', reply_markup=cancel_keyboard())
    await CheckoutStates.set_email.set()
    data = await state.get_data()
    checkout = data.get('checkout')
    checkout.phone = message.text
    await state.update_data(checkout=checkout)


async def checkout_set_email(message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Выберите способ доставки, который хотите использовать:',
                           reply_markup=set_post_keyboard())
    await CheckoutStates.set_post.set()
    data = await state.get_data()
    checkout = data.get('checkout')
    checkout.email = message.text
    await state.update_data(checkout=checkout)


async def checkout_set_post(call, state: FSMContext):
    post = call.data.split('=')[-1]
    print(post)
    data = await state.get_data()
    checkout = data.get('checkout')
    checkout.post = post
    await state.update_data(checkout=checkout)
    if post == 'новаяпочта':
        await bot.send_message(call.message.chat.id, 'Введите номер отделения новой почты:',
                               reply_markup=cancel_keyboard())
        await CheckoutStates.post_courier.set()
    elif post == 'justin':
        await bot.send_message(call.message.chat.id, 'Введите номер отделения Justin:',
                               reply_markup=cancel_keyboard())
        await CheckoutStates.post_courier.set()
    elif post == 'messt':
        await bot.send_message(call.message.chat.id, 'Введите номер отделения Messt:',
                               reply_markup=cancel_keyboard())
        await CheckoutStates.post_courier.set()
    elif post == 'курьер':
        await bot.send_message(call.message.chat.id, 'Введите адресс, по которому будет доставлен товар:',
                               reply_markup=cancel_keyboard())
        await CheckoutStates.post_courier.set()
    elif post == 'самовывоз':
        await pickup(call.message, state)


async def checkout_post_address(message, state: FSMContext):
    data = await state.get_data()
    checkout = data.get('checkout')
    checkout.post_address = message.text
    msgs_to_manager = checkout.render()
    await bot.send_message(MANAGER_ID, msgs_to_manager[1])
    price = 0
    position = 0
    for ID in msgs_to_manager[0]:
        try:
            shopper = [shopper for shopper in database.get_shoppers() if shopper.ID == ID][0]
            price += int(shopper.price)
            position += 1
            await bot.send_photo(MANAGER_ID, photo=shopper.photos[0], caption=shopper.render_big_profile())
        except Exception as e:
            print(e)
    await bot.send_message(MANAGER_ID, f'Итого: {position} товаров, на сумму {price}грн')
    await bot.send_message(message.chat.id, 'Ваша заявка отправлена, ожидайте звонка от '
                                            'менеджера в течении одного рабочего дня', reply_markup=delivery_keyboard())
    await state.reset_state()


async def pickup(message: Message, state: FSMContext):
    data = await state.get_data()
    checkout = data.get('checkout')
    msgs_to_manager = checkout.render()
    await bot.send_message(MANAGER_ID, msgs_to_manager[1])
    price = 0
    position = 0
    for ID in msgs_to_manager[0]:
        try:
            shopper = [shopper for shopper in database.get_shoppers() if shopper.ID == ID][0]
            price += int(shopper.price)
            position += 1
            await bot.send_photo(MANAGER_ID, photo=shopper.photos[0], caption=shopper.render_big_profile())
        except Exception as e:
            print(e)
    await bot.send_message(MANAGER_ID, f'Итого: {position} товаров, на сумму {price}грн')
    await bot.send_message(message.chat.id, 'Ваша заявка отправлена, ожидайте звонка от '
                                            'менеджера в течении одного рабочего дня', reply_markup=delivery_keyboard())
    await state.reset_state()
