from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder
from utils.db_api import requests as db_api
from data import config

def main_keyboard(id):
    profile = KeyboardButton(text = '💎 Мой профиль')
    faq = KeyboardButton(text = '📖 Как работать?')
    about = KeyboardButton(text ='👩🏻‍💻 О проекте')
    domains = KeyboardButton(text ='🔗 Мои домены')
    keyboard = KeyboardBuilder(button_type=KeyboardButton)
    keyboard.add(profile,faq,about,domains)
    if id in config.admins:
        keyboard.add(KeyboardButton(text = '⚙️ Админ меню'))
    keyboard.adjust(2, repeat=True)
    return keyboard.as_markup(resize_keyboard=True)




