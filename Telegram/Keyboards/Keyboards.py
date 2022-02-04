from aiogram import types


def client_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton(text='📖 Каталог 📖'), types.KeyboardButton(text='🛒 Корзина 🛒'))
    keyboard.row(types.KeyboardButton(text='📦 Доставка 📦'))
    keyboard.row(types.KeyboardButton(text='👥 Контакты 👥'), types.KeyboardButton(text='❓ О нас ❓'))
    return keyboard


def admin_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton(text='➕ Добавить шопер ➕'), types.KeyboardButton(text='➖ Удалить шопер ➖'))
    keyboard.row(types.KeyboardButton(text='🔁 Изменить шопер 🔁'), types.KeyboardButton(text='➖ Удалить ➖'))
    keyboard.row(types.KeyboardButton(text='📖 Каталог 📖'))
    return keyboard


def contacts_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.row(types.InlineKeyboardButton(text='Instagram',
                                            url='https://instagram.com/urbanite.ua?utm_medium=copy_link'),
                 types.InlineKeyboardButton(text='Telegram(канал)',
                                            url='https://t.me/urbaniteua'))
    keyboard.row(types.InlineKeyboardButton(text='Tik-Tok',
                                            url='https://vm.tiktok.com/ZMLL9nh6F'))
    return keyboard


def delivery_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text='Остались вопросы', callback_data='contacts'))
    return keyboard


def shopper_keyboard(ID, shopper_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='◀️', callback_data=f'shopper_left_id={ID-1}'),
                 types.InlineKeyboardButton(text='▶️', callback_data=f'shopper_right_id={ID+1}'),
                 types.InlineKeyboardButton(text='🖼 Больше фото 🖼', callback_data=f'more_photo_id={ID}'),
                 types.InlineKeyboardButton(text='🛒 В корзину 🛒', callback_data=f'add_to_cart_id={shopper_id}'))
    return keyboard


def shopper_more_photo_keyboard(ID, shopper_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.row(types.InlineKeyboardButton(text='🛒 В корзину 🛒', callback_data=f'add_to_cart_id={shopper_id}'),
                 types.InlineKeyboardButton(text='📖 Назад 📖', callback_data=f'back_to_catalog_id={ID}'))
    return keyboard


def add_shopper_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text='➕ Сохранить ➕', callback_data=f'save_shopper'))
    keyboard.add(types.InlineKeyboardButton(text='🚫 Отмена 🚫', callback_data='cancel'))
    return keyboard


def cart_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.row(types.InlineKeyboardButton(text='🗑 Очистить 🗑', callback_data=f'empty_cart_id={user_id}'),
                 types.InlineKeyboardButton(text='💳 Оформить заказ 💳', callback_data=f'checkout_id={user_id}'))
    return keyboard


def cancel_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text='🚫 Отмена 🚫', callback_data='cancel'))
    return keyboard


def set_post_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Новая почта', callback_data='post=новаяпочта'),
                 types.InlineKeyboardButton(text='Justin', callback_data='post=justin'),
                 types.InlineKeyboardButton(text='Meest', callback_data='post=meest'),
                 types.InlineKeyboardButton(text='Курьер', callback_data='post=курьер'),
                 types.InlineKeyboardButton(text='Самовывоз', callback_data='post=самовывоз'),
                 types.InlineKeyboardButton(text='🚫 Отмена 🚫', callback_data='cancel'))
    return keyboard
