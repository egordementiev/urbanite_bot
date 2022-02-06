from Telegram.Config import bot, database, dp, anti_flood
from Telegram.Keyboards.Keyboards import *
from Units.User import User


def is_admin(_id):
    return False


@dp.throttled(anti_flood,rate=2)
async def start(message: types.Message):
    keyboard = client_menu_keyboard() if not is_admin(message.chat.id) else admin_menu_keyboard()
    await bot.send_message(message.chat.id, 'Привет! Ты можешь воспользоваться ' 
                                            'клавиатурой кнопок для удобного пользования ботом',
                           reply_markup=keyboard)
    user = User(message.from_user.id, [], False)
    database.add_user(user)
