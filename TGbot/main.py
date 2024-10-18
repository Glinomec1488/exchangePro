#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import random
import sys
import asyncio
import logging
import time
from aiogram.types import CallbackQuery,FSInputFile,InlineKeyboardButton,InlineQuery, InputTextMessageContent, InlineQueryResultArticle,InputMediaPhoto
from aiogram import Bot, Dispatcher, types,Router
from aiogram.dispatcher.fsm.context import FSMContext
from keyboards.default import keyboards as default 
from keyboards.inline import keyboards as inline 
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
import data.config as config
from utils.db_api import requests as db_api
from states.user import states
from PIL import Image, ImageDraw,ImageFont
from datetime import datetime


db_api.createDb()

form_router = Router()
storage = MemoryStorage()
dp = Dispatcher(storage=storage)



async def main(bot: Bot) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    dp.include_router(form_router)
    bot = Bot(f'{config.BotToken}', parse_mode="HTML")
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot,drop_pending_updates=True)
    except:
        logging.info("Polling task Canceled")

@form_router.message(state=states.Answer.text)
async def rf(message: types.Message,bot: Bot, state: FSMContext):
    data = await state.get_data()
    user_id = data['userId']
    text = message.text
    dt = datetime.now()
    ts = int(datetime.timestamp(dt) * 1000)
    db_api.addMsg(user_id,text, ts)
    await bot.send_message(message.chat.id,'Ушло')
    await state.clear()

@form_router.message(state=states.addProfit.user_id)
async def rf(message: types.Message,bot: Bot, state: FSMContext):
    data = await state.get_data()
    user_id = message.text
    profit_amount = '1488'
    db_api.addProfit(user_id, profit_amount)
    await bot.send_message(message.chat.id,'Поздравляю с профитом!')
    await state.clear()

@form_router.message(state=states.changeReq.wallet)
async def rf(message: types.Message,bot: Bot, state: FSMContext):
    data = await state.get_data()
    coin = data['value']
    wallet = message.text
    db_api.changeStatus(coin,wallet)
    await bot.send_message(message.chat.id,'Реквизит успешно изменен!')
    await state.clear()


@form_router.message(commands={"start"})
async def start_cmd(message: types.Message,bot: Bot,state: FSMContext):
    usr = db_api.checkUser(message.from_user.id)
    if not usr:
        pas = ''
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        for x in range(8): 
            pas = pas + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
        db_api.registerUser(message.from_user.id,f'@{message.from_user.username}',pas,ts)
    await bot.send_message(message.chat.id,text = f"""<b>Добро пожаловать в нашу нищую тиму, {message.from_user.first_name}</b>""",reply_markup=default.main_keyboard(message.from_user.id))



@form_router.message(content_types = ['text'])
async def get_text(message: types.Message,bot: Bot) -> None:
    if message.text == '💎 Мой профиль':
        img = Image.open("example.jpg")
        d1 = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("Roboto-Bold.ttf", 50)
        fnt1 = ImageFont.truetype("Roboto-Bold.ttf", 40)
        fnt2 = ImageFont.truetype("Roboto-Regular.ttf", 18)
        fnt3 = ImageFont.truetype("Roboto-Regular.ttf", 21)
        fnt4= ImageFont.truetype("Roboto-Bold.ttf", 30)
        fnt5= ImageFont.truetype("Roboto-Bold.ttf", 30)
        count = db_api.getProfitsCount(message.from_user.id)
        amount = db_api.getProfitsAmount(message.from_user.id)
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        days = int((ts - db_api.getRegistration(message.from_user.id))/86400)
        d1.text(
                    (102,50),
                    f"Воркер:",font=fnt,
                    fill=('#000000')
                    )
        d1.text(
                    (102,110),
                    f'@dispire',font=fnt1,
                    fill=('#000000')
                    )
        d1.text(
                    (102,170),
                    f'{days} дней в нашей команде',font=fnt2,
                    fill=('#000000')
                    )
        d1.text(
                    (102,260),
                    f'{count} профитов',font=fnt3,
                    fill=('#000000')
                    )
        d1.text(
                    (102,290),
                    f'На сумму {amount} $',font=fnt4,
                    fill=('#000000')
                    )
        d1.text(
                    (102,390),
                    f'@glinomecWorkBot',font=fnt5,
                    fill=('#000000')
                    )
        img.save('abc.jpeg')
        code = db_api.getRefCode(message.from_user.id)
        await bot.send_photo(message.chat.id,caption = f"""<b>💎 Твой профиль [{message.from_user.id}]</b>

<b>Реферальный код:</b> <code>{code}</code>

<b>Общий профит:</b> <code>{amount}$</code>
<b>Кол-во профитов:</b> <code>{count}</code>

<b>В команде:</b> {days} дней""",photo = FSInputFile('abc.jpeg'))
    elif message.text == '🔗 Мои домены':
        await bot.send_message(message.chat.id,text = '<b>В разработке</b>')
    elif message.text == '📖 Как работать?':
        code = db_api.getCode(message.from_user.id)
        await bot.send_message(message.chat.id,text = f"""<b>📖 Как работать в нашем проекте</b>

<b>Ссылки на наши обменники:</b>
— https://bromo.com

<b>Твой реферальный код:</b> <code>{code}</code>

<b>Твои реферальные ссылки:</b>
— https://bromo.com?ref={code}


<b>Связки для мамонтов:</b>
<b>XMR/USDT</b> - https://telegra.ph/Novaya-arbitrazhnaya-svyazka-06-19
<b>LTC/USDT</b> - https://telegra.ph/Novaya-arbitrazhnaya-svyazka-06-19-2
<b>TRX/USDT</b> - https://telegra.ph/Novaya-arbitrazhnaya-svyazka-06-19-3

<i>⚠️ Мамонт обязательно должен ввести на сайте реферальный код который указан в твоем профиле</i>""",reply_markup=inline.faqButtons(),disable_web_page_preview=True)
    elif message.text == '👩🏻‍💻 О проекте':
        await bot.send_message(message.chat.id,text = """👩🏻‍💻 О нашем проекте

Мы открылись не важно когда
У нас 0 профитов на сумму 0$
Средняя сумма профита: 0

📞 Наши контакты:
Тс / кодер: @maslo_1488
Тс: @inbox77xxx

⚠️ Ворк по укр РАЗРЕШЁН
💸 Не выплачиваем

⚠️ Все логи в черную после 2 профитов""")
    elif message.text == '⚙️ Админ меню':
        await bot.send_message(message.chat.id,text= f'<b>Hello</b>',reply_markup=inline.apanel())
    else:
        pass



@form_router.callback_query(lambda c: c.data,)
async def ans(call: CallbackQuery,bot: Bot,state: FSMContext,) -> None:
    if 'uans' in call.data:
        id = call.data.split('_')[1]
        await state.update_data(userId = id)
        await bot.send_message(call.message.chat.id,text = 'Введите текст')
        await state.set_state(states.Answer.text)
    #elif call.data == 'addprofit':
    #    await bot.send_message(call.message.chat.id,text = '<b>Введите ID пользователя:</b>')
    #    await state.set_state(states.addProfit.user_id)
    elif call.data == 'changereq':
        await bot.send_message(call.message.chat.id,text = '<b>Выберите коин:</b>',reply_markup=inline.change_coins())
    elif 'ch_' in call.data:
        await state.update_data(value = call.data.split('_')[1])
        await bot.send_message(call.message.chat.id,'Введите новый реквизит')
        await state.set_state(states.changeReq.wallet)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main(bot = Bot))