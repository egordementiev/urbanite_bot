from Telegram.Config import bot, database, anti_flood, anti_flood_rate, dp
from Telegram.Keyboards.Keyboards import *
from Units.User import User
from aiogram.types import InputMedia, InputMediaPhoto, Message
from aiogram.dispatcher.storage import FSMContext


@dp.throttled(anti_flood, rate=anti_flood_rate)
async def contacts(message):
    contacts_text = 'Наши Контакты:\n\n' \
                    'C нами можно связаться несколькими способами:\n' \
                    '•  Телефон, Telegram, Viber - 0993867025\n' \
                    '•  Почта - urbaniteua@gmail.com\n' \
                    '•  Instagram(директ)\n' \
                    '\n' \
                    'Другие наши соц сети:\n' \
                    '•  Tik-Tok\n' \
                    '•  Telegram канал'
    await bot.send_message(message.chat.id, contacts_text, reply_markup=contacts_keyboard())


@dp.throttled(anti_flood, rate=anti_flood_rate)
async def about(message):
    about_text = 'Мы компания из Киева, наша цель - делать людей счастливыми. ' \
                 'Наши товары это: удобство, стиль и простота. Для нас, ' \
                 'главный показатель - качество продукции, а главная мотивация - счасливые клиенты.'
    await bot.send_message(message.chat.id, about_text, reply_markup=delivery_keyboard())


@dp.throttled(anti_flood, rate=anti_flood_rate)
async def delivery(message):
    delivery_text = 'Доставка📨:\n' \
                    '• Службы доставки(по всей Украине):\n' \
                    '   - Новая почта ~ 50грн\n' \
                    '   - Justin~25-30грн\n' \
                    '   - Meest~30-40грн\n' \
                    '• Доставка курьером по Соломенскому району🚚 - 35грн\n' \
                    '• Самовывоз(г. Киев, ул. Борщаговская 212)📦 - бесплатно'
    await bot.send_message(message.chat.id, delivery_text, reply_markup=delivery_keyboard())


@dp.throttled(anti_flood, rate=anti_flood_rate)
async def catalog(message):
    shoppers = database.get_shoppers()
    if len(shoppers) < 1:
        await bot.send_message(message.chat.id, 'Каталог пуст')
        return
    shopper = shoppers[0]
    print(f'shopper = {shopper}')
    await bot.send_photo(message.chat.id, photo=shopper.photos[0],
                         caption=shopper.render_big_profile(),
                         reply_markup=shopper_keyboard(0, shopper.ID))


async def slide_shopper_left(message: Message, ID: int):
    print(message)
    shoppers = database.get_shoppers()
    if len(shoppers) < 1:
        await bot.edit_message_text('Каталог пуст', message.chat.id, message.message_id)
        return

    if ID < 0:
        shopper = shoppers[-1]
        print(f'shopper = {shopper}')
        if len(shoppers) > 1:
            print('Edit message(ID=0)')
            await bot.edit_message_media(media=InputMedia(media=shopper.photos[0],
                                                          caption=shopper.render_big_profile()),
                                         chat_id=message.chat.id, message_id=message.message_id,
                                         reply_markup=shopper_keyboard(shoppers.index(shopper), shopper.ID))
        # await bot.send_photo(message.chat.id, photo=shopper.photos[0])
        return

    shopper = shoppers[ID]
    print(f'shopper = {shopper}')
    print('Edit message(ID=ID)')
    print(message.photo[0].file_id)
    print(shopper.photos[0])
    if message.photo[0].file_id != shopper.photos[0]:
        await bot.edit_message_media(media=InputMedia(media=shopper.photos[0], caption=shopper.render_big_profile()),
                                     chat_id=message.chat.id, message_id=message.message_id,
                                     reply_markup=shopper_keyboard(ID, shopper.ID))


async def slide_shopper_right(message: Message, ID: int):
    print(message)
    shoppers = database.get_shoppers()
    if len(shoppers) < 1:
        await bot.edit_message_text('Каталог пуст', message.chat.id, message.message_id)
        return

    if len(shoppers) <= ID:
        shopper = shoppers[0]
        print(f'shopper = {shopper}')
        if ID > 1:
            print('Edit message(ID=0)')
            await bot.edit_message_media(media=InputMedia(media=shopper.photos[0],
                                                          caption=shopper.render_big_profile()),
                                         chat_id=message.chat.id, message_id=message.message_id,
                                         reply_markup=shopper_keyboard(0, shopper.ID))
        # await bot.send_photo(message.chat.id, photo=shopper.photos[0])
        return

    shopper = shoppers[ID]
    print(f'shopper = {shopper}')
    print('Edit message(ID=ID)')
    print(message.photo[0].file_id)
    print(shopper.photos[0])
    if message.photo[0].file_id != shopper.photos[0]:
        await bot.edit_message_media(media=InputMedia(media=shopper.photos[0], caption=shopper.render_big_profile()),
                                     chat_id=message.chat.id, message_id=message.message_id,
                                     reply_markup=shopper_keyboard(ID, shopper.ID))

    # await bot.send_photo(message.chat.id, photo=shopper.photos[0])


@dp.throttled(anti_flood, rate=anti_flood_rate)
async def more_photo(message: Message, ID: int):
    shoppers = database.get_shoppers()
    if len(shoppers) <= ID:
        return

    shopper = shoppers[ID]
    if len(shopper.photos) > 1:
        media = [InputMediaPhoto(media=photo) for photo in shopper.photos]

    else:
        media = InputMediaPhoto(media=shopper.photos[0])
    print(media)
    await bot.send_media_group(media=media, chat_id=message.chat.id)


@dp.throttled(anti_flood, rate=anti_flood_rate)
async def add_to_cart(user_id: int, ID: int):
    user = database.get_user(user_id)
    if not user:
        database.add_user(User(user_id, [], False))
        user = database.get_user(user_id)

    user.cart.append(ID)
    database.update_user(user)


@dp.throttled(anti_flood, rate=anti_flood_rate)
async def cart(message: Message):
    user = database.get_user(message.from_user.id)
    cart = user.cart
    cost = 0
    print(f'-- user = {database.get_user(message.from_user.id)}')
    for shopper_id in cart:
        print(shopper_id)
        shopper = database.get_shopper(shopper_id)
        print(shopper)
        if not shopper:
            user.cart.remove(shopper_id)
            database.update_user(user)
            continue
        print(f'shopper_id = {shopper_id} | shopper = {shopper}')
        cost += int(shopper.price)
        await bot.send_photo(chat_id=message.chat.id, photo=shopper.photos[0], caption=shopper.render_big_profile())

    print(f'-- user = {database.get_user(message.from_user.id)}')
    if len(user.cart) < 1:
        await bot.send_message(message.chat.id, 'Ваша корзина пуста :(', reply_markup=checkout_false_keyboard())
        return

    await bot.send_message(message.chat.id, f'⬆️ Ваша корзина ⬆️\n'
                                            f'   Товаров 👜: {len(user.cart)}(шт)\n'
                                            f'   Сумма 💵: {cost}грн', reply_markup=cart_keyboard(message.from_user.id))


@dp.throttled(anti_flood, rate=anti_flood_rate)
async def empty_cart(message: Message, user_id: int):
    user = database.get_user(user_id)
    user.cart = []
    database.update_user(user)
    await bot.edit_message_text('Корзина очищена', message.chat.id, message.message_id,
                                reply_markup=checkout_false_keyboard())


@dp.throttled(anti_flood, rate=anti_flood_rate)
async def my_id(message: Message):
    await bot.send_message(message.chat.id, f'id чата = {message.chat.id}')


@dp.throttled(anti_flood, rate=anti_flood_rate)
async def my_status(message: Message):
    try:
        user = [user for user in database.get_users() if str(user.ID) == str(message.from_user.id)][0]
    except:
        await bot.send_message(message.chat.id, 'Вас не найденно в датабазе, напишите боту команду /start')
        return

    await bot.send_message(message.chat.id, f'Ваш пользователь = {user}')
