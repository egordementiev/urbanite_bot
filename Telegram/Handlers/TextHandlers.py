from Telegram.Handlers.MainMenuClient.MainMenuClientHandlers import *


async def text_handler(message):
    text = ''.join([letter for letter in message.text if letter.isalpha()]).lower()
    if text in ['контакты']:
        await contacts(message)

    elif text in ['доставка']:
        await delivery(message)

    elif text in ['каталог']:
        await catalog(message)

    elif text in ['корзина']:
        await cart(message)

    elif text in ['онас']:
        await about(message)
