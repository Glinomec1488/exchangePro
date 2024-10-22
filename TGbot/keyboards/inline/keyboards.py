from audioop import add
from subprocess import call
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder
from regex import E
from data import config
from utils.db_api import requests as db_api


def faqButtons():
    first = InlineKeyboardButton(text = '📖  Первый мануал',url = 'https://telegra.ph/Manual-po-rabote-v-Workers-Club-Exchange-06-19')
    second = InlineKeyboardButton(text = '📖  Второй мануал',url = 'https://telegra.ph/Manual-po-rabote-v-Workers-Club-Exchange-v2-06-19')
    keyboard = KeyboardBuilder(button_type=InlineKeyboardButton)
    keyboard.add(first,second)
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()

def apanel():
    first = InlineKeyboardButton(text = 'Добавить залет',callback_data= 'addprofit')
    second = InlineKeyboardButton(text = 'Изменить реквизиты',callback_data = 'changereq')
    third = InlineKeyboardButton(text = 'Очистить старые чаты ТП', callback_data='rmoldchats')
    fourth = InlineKeyboardButton(text = 'Удалить воркера', callback_data='rmuser')
    fifth = InlineKeyboardButton(text = 'Дать общий варн', callback_data='msgeveryone')
    keyboard = KeyboardBuilder(button_type=InlineKeyboardButton)
    keyboard.add(first,second,third,fourth,fifth)
    keyboard.adjust(2, repeat=True)
    return keyboard.as_markup()

def regUser():
    first = InlineKeyboardButton(text = 'Подтвердить', callback_data='')
    keyboard = KeyboardBuilder(button_type=InlineKeyboardButton)
    keyboard.add(first)
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()

def change_coins():
    btc = InlineKeyboardButton(text = 'BTC',callback_data= 'ch_BTC')
    btc1 = InlineKeyboardButton(text = 'ETH',callback_data= 'ch_ETH')
    btc2 = InlineKeyboardButton(text = 'BNB',callback_data= 'ch_BNB')
    btc3 = InlineKeyboardButton(text = 'BCH',callback_data= 'ch_BCH')
    btc4 = InlineKeyboardButton(text = 'ETC',callback_data= 'ch_ETC')
    btc5 = InlineKeyboardButton(text = 'ZEC',callback_data= 'ch_ZEC')
    btc6 = InlineKeyboardButton(text = 'FTM',callback_data= 'ch_FTM')
    btc7 = InlineKeyboardButton(text = 'SOL',callback_data= 'ch_SOL')
    btc8 = InlineKeyboardButton(text = 'LTC',callback_data= 'ch_LTC')
    btc9 = InlineKeyboardButton(text = 'TRX',callback_data= 'ch_TRX')
    btc10 = InlineKeyboardButton(text = 'ZRX(ERC20)',callback_data= 'ch_ZRX')
    btc11 = InlineKeyboardButton(text = 'XRP',callback_data= 'ch_XRP')
    btc12 = InlineKeyboardButton(text = 'USDT(ERC20)',callback_data= 'ch_USDT')
    btc13 = InlineKeyboardButton(text = 'USDT(TRC20)',callback_data= 'ch_USDTTRC')
    btc14 = InlineKeyboardButton(text = 'ADA',callback_data= 'ch_ADA')
    btc15 = InlineKeyboardButton(text = 'XTZ',callback_data= 'ch_XTZ')
    btc16 = InlineKeyboardButton(text = 'MATIC(POLYGON)',callback_data= 'ch_MATIC')
    btc17 = InlineKeyboardButton(text = 'XMR',callback_data= 'ch_XMR')
    btc18 = InlineKeyboardButton(text = 'DASH',callback_data= 'ch_DASH')
    btc19 = InlineKeyboardButton(text = 'SHIB(ERC20)',callback_data= 'ch_SHIB')
    btc20 = InlineKeyboardButton(text = 'DOGE',callback_data= 'ch_DOGE')
    btc21 = InlineKeyboardButton(text = 'DOT',callback_data= 'ch_DOT')
    keyboard = KeyboardBuilder(button_type=InlineKeyboardButton)
    keyboard.add(btc,btc1,btc2,btc3,btc4,btc5,btc6,btc7,btc8,btc9,btc10,btc11,btc12,btc13,btc14,btc15,btc16,btc17,btc18,btc19,btc20,btc21)
    keyboard.adjust(2, repeat=True)
    return keyboard.as_markup()




