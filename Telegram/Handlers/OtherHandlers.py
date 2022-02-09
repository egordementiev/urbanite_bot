from Telegram.Config import bot, database, dp, anti_flood, anti_flood_rate
from Telegram.Keyboards.Keyboards import *
from Units.Stat import Stat
from Units.User import User


def is_admin(_id):
    return False


@dp.throttled(anti_flood, rate=anti_flood_rate)
async def start(message: types.Message):
    sm = message.text.split(' ')
    print(sm)
    print(f'len(sm) = {len(sm)}')
    if len(sm) > 1:
        print(f'sm = {sm}')
        sm.pop(0)
        sm = ''.join(sm)
        stat = database.get_stat_by_title(sm)
        if not stat:
            stat = Stat(None, sm, 1)
            database.add_stat(stat)
        else:
            stat.users += 1
            database.update_stat(stat)

    elif len(sm) == 1:
        stat = database.get_stat_by_title('telegram_search')
        print(stat)
        if not stat:
            stat = Stat(None, 'telegram_search', 1)
            database.add_stat(stat)
        else:
            stat.users += 1
            print(f'stat = {stat}')
            database.update_stat(stat)

    keyboard = client_menu_keyboard() if not is_admin(message.chat.id) else admin_menu_keyboard()
    await bot.send_message(message.chat.id, 'Привет! Ты можешь воспользоваться ' 
                                            'клавиатурой кнопок для удобного пользования ботом',
                           reply_markup=keyboard)
    user = User(message.from_user.id, [], False)
    database.add_user(user)
