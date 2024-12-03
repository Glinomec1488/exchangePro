#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import random
import sys
import asyncio
import logging
import time
import requests
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineQuery,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InputMediaPhoto,
    InlineKeyboardMarkup,
    Message,
)
from aiogram import Bot, Dispatcher, types, Router
from aiogram.dispatcher.fsm.context import FSMContext
from keyboards.default import keyboards as default
from keyboards.inline import keyboards as inline
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
import data.config as config
from utils.db_api import requests as db_api
from states.user import states
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from aiogram import Router, F, Bot, Dispatcher


db_api.createDb()

form_router = Router()
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
basicPriv = "basic"
superadminPriv = "superadmin"
managerPriv = "manager"


async def main(bot: Bot) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    dp.include_router(form_router)
    bot = Bot(f"{config.BotToken}", parse_mode="HTML")
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot, drop_pending_updates=True)
    except:
        logging.info("Polling task Canceled")


@form_router.message(state=states.Answer.text)
async def rf(message: types.Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    user_id = data["userId"]
    text = message.text
    dt = datetime.now()
    ts = int(datetime.timestamp(dt) * 1000)
    db_api.addMsg(user_id, text, ts)
    await bot.send_message(message.chat.id, "Ушло")
    await state.clear()


@form_router.message(state=states.addProfit.user_id)
async def rf(message: types.Message, bot: Bot, state: FSMContext):
    user_id = message.text.split(":")[0]
    amount = message.text.split(":")[1]
    intId = int(user_id)
    floatAmout = float(amount)
    usr = db_api.checkUser(intId)
    if not usr:
        await bot.send_message(
            message.chat.id, f"Воркера <code>{usr}</code> не существует"
        )
        await bot.send_message(
            message.chat.id, text=f"<b>Привет 🩸</b>", reply_markup=inline.apanel()
        )
        await state.clear()
    else:
        db_api.addProfit(intId, floatAmout)
        await bot.send_message(intId, f"{usr}, поздравляю с профитом!\n{amount}$")
        await bot.send_message(
            message.chat.id, text=f"<b>Привет 🩸</b>", reply_markup=inline.apanel()
        )
        await state.clear()


@form_router.message(state=states.changeReq.wallet)
async def rf(message: types.Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    coin = data["value"]
    wallet = message.text
    db_api.changeStatus(coin, wallet)
    await bot.send_message(
        message.chat.id,
        f"Реквизит <code>{coin}</code> успешно изменен на :\n<code>{wallet}</code>",
    )
    await bot.send_message(
        message.chat.id, text=f"<b>Привет 🩸</b>", reply_markup=inline.apanel()
    )
    await state.clear()


@form_router.message(state=states.RemoveUserForm.user_id)
async def rmus(message: types.Message, bot: Bot, state: FSMContext):
    user_id = message.text
    usr = db_api.checkUser(user_id)
    if not usr:
        await bot.send_message(message.chat.id, text="Таких Дэбилов у нас нет")
        await state.clear()
    else:
        inline_keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "Да",
                        "callback_data": f"banuser_{user_id}",
                    }
                ],
                [
                    {
                        "text": "Нет",
                        "callback_data": f"returnToPanel",
                    }
                ],
            ]
        }
        db_api.removeUser(user_id)
        await bot.send_message(
            message.chat.id,
            text=f"{user_id} - ЛИКВИДИРОВАН, желаете ли отправить его в спам-лист?",
            reply_markup=inline_keyboard,
        )
        await state.clear()


@form_router.message(state=states.msgEveryone.message)
async def sendMessage(message: types.Message, bot: Bot, state: FSMContext):
    allIds = db_api.getAllUsers()
    if message.text:
        message = message.text
        for i in allIds:
            await bot.send_message(i, text=f"""{message}""")
    elif message.photo:
        message = message.photo[-1].file_id
        for i in allIds:
            await bot.send_photo(i, photo=message)
    elif message.video:
        message = message.video.file_id
        for i in allIds:
            await bot.send_video(i, video=message)
    await state.clear()


@form_router.message(commands={"start"})
async def start_cmd(message: types.Message, bot: Bot, state: FSMContext):
    banned = db_api.checkIfBanned(message.from_user.id)
    if not banned:
        usr = db_api.checkUser(message.from_user.id)
        if not usr:
            if message.from_user.id in config.admins:
                pas = ""

                dt = datetime.now()
                ts = datetime.timestamp(dt)
                for x in range(8):
                    pas = pas + random.choice(
                        list(
                            "1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ"
                        )
                    )
                db_api.registerUser(
                    message.from_user.id,
                    f"@{message.from_user.username}",
                    pas,
                    ts,
                    superadminPriv,
                )
                await bot.send_message(message.chat.id, text=f"🦣💪")
            else:
                await bot.send_message(
                    message.chat.id,
                    text=f"""<b>Добро пожаловать , {message.from_user.first_name}, отпиши нашему админу. {config.coderUS}</b>""",
                )
                inline_keyboard = {
                    "inline_keyboard": [
                        [
                            {
                                "text": "Подтвердить заявку",
                                "callback_data": f"register;{message.chat.id}.{message.from_user.username}",
                            }
                        ],
                        [
                            {
                                "text": "В спам",
                                "callback_data": f"banuser_{message.chat.id}",
                            }
                        ],
                    ]
                }
                for i in config.admins:
                    await bot.send_message(
                        i,
                        text=f"""{message.from_user.first_name}, ({message.from_user.id}) ожидает подтверждения""",
                        reply_markup=inline_keyboard,
                    )
        else:
            await bot.send_message(
                message.chat.id,
                text=f"""<b>Сап</b>""",
                reply_markup=default.main_keyboard(message.from_user.id),
            )
    else:
        pass


@form_router.message(content_types=["text"])
async def get_text(message: types.Message, bot: Bot) -> None:
    usr = db_api.checkUser(message.from_user.id)
    if usr:
        if message.text == "💎 Мой профиль":
            img = Image.open("./example.jpg")
            d1 = ImageDraw.Draw(img)
            fnt = ImageFont.truetype("Roboto-Bold.ttf", 50)
            fnt1 = ImageFont.truetype("Roboto-Bold.ttf", 40)
            fnt2 = ImageFont.truetype("Roboto-Regular.ttf", 18)
            fnt3 = ImageFont.truetype("Roboto-Regular.ttf", 21)
            fnt4 = ImageFont.truetype("Roboto-Bold.ttf", 30)
            fnt5 = ImageFont.truetype("Roboto-Bold.ttf", 30)
            count = db_api.getProfitsCount(message.from_user.id)
            amount = db_api.getProfitsAmount(message.from_user.id)
            dt = datetime.now()
            ts = datetime.timestamp(dt)
            days = int((ts - db_api.getRegistration(message.from_user.id)) / 86400)
            d1.text((102, 50), f"Воркер:", font=fnt, fill=("#000000"))
            d1.text(
                (102, 110), f"{message.from_user.username}", font=fnt1, fill=("#000000")
            )
            d1.text(
                (102, 170), f"{days} дней в нашей команде", font=fnt2, fill=("#000000")
            )
            d1.text((102, 260), f"{count} профитов", font=fnt3, fill=("#000000"))
            d1.text((102, 290), f"На сумму {amount} $", font=fnt4, fill=("#000000"))
            d1.text((102, 390), f"@extasy_team_bot", font=fnt5, fill=("#000000"))
            img.save("abc.jpeg")
            code = db_api.getRefCode(message.from_user.id)
            await bot.send_photo(
                message.chat.id,
                caption=f"""<b>💎 Твой профиль [{message.from_user.id}]</b>

    <b>Реферальный код:</b> <code>{code}</code>

    <b>Общий профит:</b> <code>{amount}$</code>
    <b>Кол-во профитов:</b> <code>{count}</code>

    <b>В команде:</b> {days} дней""",
                photo=FSInputFile("abc.jpeg"),
            )
        elif message.text == "🔗 Мои домены":
            await bot.send_message(message.chat.id, text="<b>В разработке</b>")
        elif message.text == "📖 Как работать?":
            code = db_api.getCode(message.from_user.id)
            await bot.send_message(
                message.chat.id,
                text=f"""<b>📖 Как работать в нашем проекте</b>

    <b>Ссылки на наши обменники:</b>
    — https://bestexc.pro

    <b>Твой реферальный код:</b> <code>{code}</code>

    <b>Твои реферальные ссылки:</b>
    — https://bestexc.pro?ref={code}


    <b>Связки для мамонтов:</b>
    <b>XMR/USDT</b> - https://telegra.ph/Novaya-arbitrazhnaya-svyazka-06-19
    <b>LTC/USDT</b> - https://telegra.ph/Novaya-arbitrazhnaya-svyazka-06-19-2
    <b>TRX/USDT</b> - https://telegra.ph/Novaya-arbitrazhnaya-svyazka-06-19-3

    <i>⚠️ Мамонт обязательно должен ввести на сайте реферальный код который указан в твоем профиле</i>""",
                reply_markup=inline.faqButtons(),
                disable_web_page_preview=True,
            )
        elif message.text == "👩🏻‍💻 О проекте":
            await bot.send_message(
                message.chat.id,
                text=f"""👩🏻‍💻 О нашем проекте

    Вашингтон тоже не за один день построен

    📞 Наши контакты:
    Тс / кодер: {config.coderUS}

    💸 Выплаты на CryptoBot или в BTC

    ⚠️ """,
            )
        elif message.text == "🍷 Админ Меню":
            print(db_api.checkPriv(message.from_user.id))
            if db_api.checkPriv(message.from_user.id) == superadminPriv:
                await bot.send_message(
                    message.chat.id,
                    text=f"<b>Привет 🩸</b>",
                    reply_markup=inline.apanel(),
                )
            else:
                pass
        elif message.text == "⚙️ Панель Управления":
            if db_api.checkPriv(message.from_user.id) == managerPriv or superadminPriv:
                await bot.send_message(
                    message.chat.id,
                    text=f"<b>Панель Управления</b>",
                    reply_markup=inline.managementPanel(),
                )
            else:
                pass
        elif message.text == "🛠 Настройки":
            await bot.send_message(
                message.chat.id,
                text=f"<b>В разработке</b>",
            )
        else:
            pass
    else:
        pass


@form_router.callback_query(
    lambda c: c.data,
)
async def ans(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    if "uans" in call.data:
        id = call.data.split("_")[1]
        await state.update_data(userId=id)
        await bot.send_message(call.message.chat.id, text="Введите текст")
        await state.set_state(states.Answer.text)
    elif "rmchat" in call.data:
        id = call.data.split("_")[1]
        await state.update_data(userId=id)
        db_api.clMsg(id)
        await bot.send_message(call.message.chat.id, text=f"Чат у {id} очищен")
    elif "rmoldchats" in call.data:
        db_api.delete_old_messages()
        await bot.edit_message_text(
            f"старые чаты очищены",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline.managementPanelBack(),
        )
    elif "register" in call.data:
        filterRegPrefiix = call.data.split(";")[1]
        id = filterRegPrefiix.split(".")[0]
        name = filterRegPrefiix.split(".")[1]
        usr = db_api.checkUser(id)
        if not usr:
            pas = ""
            dt = datetime.now()
            ts = datetime.timestamp(dt)
            for x in range(8):
                pas = pas + random.choice(
                    list(
                        "1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ"
                    )
                )
            db_api.registerUser(id, f"@{name}", pas, ts, basicPriv)
            await bot.send_message(
                call.message.chat.id,
                "Пользователь добавлен! Не забудьте вбить его логи в черную",
            )
            await bot.send_message(
                id, "Вы были добавлены администратором! Напишите /start"
            )
        else:
            await bot.send_message(call.message.chat.id, "Уже добавлен")
    elif call.data == "rmuser":
        await bot.edit_message_text(
            f"<b>Введите ID пользователя:</b>",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline.adminBack(),
        )
        await state.set_state(states.RemoveUserForm.user_id)
    elif call.data == "msgeveryone":
        await bot.edit_message_text(
            f"Введите текст или киньте картинку",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline.managementPanelBack(),
        )
        await state.set_state(states.msgEveryone.message)
    elif call.data == "addprofit":
        await bot.edit_message_text(
            f"введите профит в формате telegramID:сумма$",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline.adminBack(),
        )
        await state.set_state(states.addProfit.user_id)
    elif call.data == "changereq":
        await bot.edit_message_text(
            text="<b>Выберите коин:</b>",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline.change_coins(),
        )
    elif "confirm_" in call.data:
        data = call.data.split("_")[1]
        db_api.changeStatusToReturned(data)
        payload = {"transID": data}
        response = requests.post(f"{config.serverUrl}/send-message", json=payload)
        if response.status_code == 200:
            print("200")
        else:
            print("error", response)
    elif "custErr_" in call.data:
        data = call.data.split("_")[1]
        db_api.changeStatusToErr(data)
        payload = {"transID": data}
        response = requests.post(f"{config.serverUrl}/send-message", json=payload)
        if response.status_code == 200:
            print("200")
        else:
            print("error", response)
    elif call.data == "lsusers":
        data = db_api.listUserDb()
        await bot.edit_message_text(
            text=f"Лист пользователей:\n{data} ",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline.adminBack(),
        )
    elif "ch_" in call.data:
        await state.update_data(value=call.data.split("_")[1])
        await bot.edit_message_text(
            "Введите новый реквизит",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline.adminBack(),
        )
        await state.set_state(states.changeReq.wallet)
    elif "banuser" in call.data:
        user_id = call.data.split("_")[1]
        banned = db_api.checkIfBanned(user_id)
        if not banned:
            db_api.ban(user_id)
            await bot.edit_message_text(  # $
                f"Пользователь {user_id} был отправлен в спам-лист",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=inline.adminBack(),
            )
        else:
            await bot.send_message(
                call.message.chat.id,
                f"{user_id} - Уже в бане",
            )
    elif "returnToPanel" in call.data:
        await state.clear()
        await bot.edit_message_text(
            f"<b>Привет 🩸</b>",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline.apanel(),
        )
    elif "returnToManagementPanel" in call.data:
        await state.clear()
        await bot.edit_message_text(
            f"<b>Панель Управления</b>",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline.managementPanel(),
        )
    elif "hideChat_" in call.data:
        data = call.data.split("_")[1]
        db_api.chatBan(data)
        payload = {"id": data}
        response = requests.post(f"{config.serverUrl}/hideChat", json=payload)
    elif "promote_" in call.data:
        userId = call.data.split("_")[1]
        await bot.edit_message_text(  # $
            f"Пользователь {user_id} был повышен до ",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline.adminBack(),
        )
    elif "show_banlist" in call.data:
        banlist = db_api.show_banlist()
        await bot.edit_message_text(
            text=f"Лист забаненных пользователей:\n{banlist} ",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=inline.adminBack(),
        )
        # if response.status_code == 200:
        #    print("200")
        # else:
        #    print("error", response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main(bot=Bot))
