import sqlite3
import os

txJumpStart = [
    ("110lnzd9imbe...", "188719", "tz1NqA", "tz1DfN...", "431.23 XTZ"),
    ("cmla53spvik...", "798642", "NBxFrD", "DVxdDa...", "8.18 LTC"),
    ("kesdqohj1oh...", "588726", "BD4dMC...", "TH3BmQ...", "2801.35 ZRX"),
    ("x3dtmhwnddf...", "774009", "3FZbgi", "P2PKdd...", "0.04 BTC"),
    ("8ifg8ctwpa8...", "553990", "1C15FE", "0F96B6...", "1824.46 XRP"),
    ("hkvqxdxvybs...", "353175", "4f1494...", "0abc4e...", "10620.48 XLM"),
    ("wgggoaslmqb...", "372017", "TR7NHq...", "TH3BmQ...", "9835.35 TRX"),
    ("t6z9t6otlb...", "109767", "0xb794...", "0x165C...", "0.49 ETH"),
]

coinDB = [
    ("BITCOIN", "BTC", "BTC", "wallet3"),
    ("Ethereum", "ETH", "ETH", "wallet3"),
    ("BINANCE SMART CHAIN", "LTC", "BNB", "wallet3"),
    ("BITCOIN CASH", "BCH", "BCH", "wallet3"),
    ("ZCASH", "ZEC", "ZEC", "wallet3"),
    ("FANTOM", "FTM", "FTM", "wallet3"),
    ("SOLANA", "SOL", "SOL", "wallet3"),
    ("LITECOIN", "LTC", "LTC", "wallet3"),
    ("TRON", "TRX", "TRX", "wallet3"),
    ("0X (ERC20)", "ZRX(ERC20)", "ZRX", "wallet3"),
    ("RIPPLE", "XRP", "XRP", "wallet3"),
    ("TETHER (ERC20)", "USDT(ERC20)", "USDT", "wallet3"),
    ("TETHER (TRC20)", "USDT(TRC20)", "USDTTRC", "wallet3"),
    ("CARDANO", "ADA", "ADA", "wallet3"),
    ("TEZOS", "XTZ", "XTZ", "wallet3"),
    ("POLYGON (POLYGON)", "MATIC(POLYGON)", "MATIC", "wallet3"),
    ("MONERO", "XMR", "XRP", "wallet3"),
    ("DASH", "DASH", "DASH", "wallet3"),
    ("SHIBA INU (ERC20)", "SHIB(ERC20)", "SHIB", "wallet3"),
    ("DOGE", "DOGE", "DOGE", "wallet3"),
    ("POLKADOT", "DOT", "DOT", "wallet3"),
]


def create_db():
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS coins (fullName TEXT, shortName TEXT, image TEXT, wallet TEXT)"""
    )
    cursor.execute("""CREATE TABLE IF NOT EXISTS chat_users (id INTEGER)""")
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS messages (text TEXT,userId INTEGER,timestamp INTEGER,user TEXT)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS categories (id INTEGER,name TEXT,thumb_url FLOAT)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS items (id INTEGER,name TEXT,description TEXT,thumb_url FLOAT,price FLOAT,category_id INTEGER)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS transactions (txHash TEXT, block TEXT, fromm TEXT, tos TEXT, value TEXT)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS changes (orderId INTEGER, receiveAmount FLOAT, receiveCurrency TEXT, sendAmount FLOAT, sendCurrency TEXT, receiver TEXT, email TEXT, referalCode TEXT, status TEXT)"""
    )
    cursor.close()


def defaultCoinsCreate():
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("""DELETE FROM coins""")
    cursor.executemany(
        """INSERT OR IGNORE INTO coins (fullName, shortName, image, wallet)VALUES (?, ?, ?, ?)
 """,
        coinDB,
    )
    conn.commit()
    cursor.close()


def defaultTxCreate():
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("""DELETE FROM transactions""")
    cursor.executemany(
        """INSERT OR IGNORE INTO transactions (txHash, block, fromm, tos, value)VALUES (?, ?, ?, ?, ?)
 """,
        txJumpStart,
    )
    conn.commit()
    cursor.close()


def checkUser(user_id):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("select * from chat_users where id = ?", (user_id,))
    usr = cursor.fetchone()
    cursor.close()
    return usr


def registerUser(user_id, ip_addr, online):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_users values (:id, :ip_addr, :online);",
        {"id": user_id, "ip_addr": ip_addr, "online": online},
    )
    conn.commit()
    cursor.close()
    return


def getId():
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    ids = cursor.execute(f"SELECT id FROM chat_users").fetchall()
    ids = [i[0] for i in ids]
    receiveAmount = int(ids[-1]) + 1
    cursor.close()
    return receiveAmount


def addMsg(text, userId, timestamp, user):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages values (:text,:userId,:timestamp,:user);",
        {"text": text, "userId": userId, "timestamp": timestamp, "user": user},
    )
    conn.commit()
    cursor.close()
    return


def addOrder(
    orderId,
    receiveAmount,
    receiveCurrency,
    sendAmount,
    sendCurrency,
    receiver,
    email,
    referalCode,
    status,
):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO changes values (:orderId,:receiveAmount,:receiveCurrency,:sendAmount,:sendCurrency,:receiver,:email,:referalCode,:status);",
        {
            "orderId": orderId,
            "receiveAmount": receiveAmount,
            "receiveCurrency": receiveCurrency,
            "sendAmount": sendAmount,
            "sendCurrency": sendCurrency,
            "receiver": receiver,
            "email": email,
            "referalCode": referalCode,
            "status": status,
        },
    )
    conn.commit()
    cursor.close()
    return


def getUserId(user_id):
    # with sqlite3.connect(os.path.join("TGbot", "../database.db"),check_same_thread=False) as conn:
    with sqlite3.connect("../TGbot/database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    amount = cursor.execute(
        f'SELECT user_id FROM users WHERE code = "{user_id}"'
    ).fetchone()[0]
    cursor.close()
    return amount


def changeStatus(orderId):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(
        f'UPDATE changes SET status = "confirmed" WHERE orderId = "{orderId}"'
    )
    conn.commit()
    cursor.close()


def changeStatusToReturned(orderId):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(f'UPDATE changes SET status = "passed" WHERE orderId = "{orderId}"')
    conn.commit()
    cursor.close()


def getOrderInfo(orderId):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    receiveAmount = cursor.execute(
        f'SELECT receiveAmount FROM changes WHERE orderId = "{orderId}"'
    ).fetchone()[0]
    receiveCurrency = cursor.execute(
        f'SELECT receiveCurrency FROM changes WHERE orderId = "{orderId}"'
    ).fetchone()[0]
    sendAmount = cursor.execute(
        f'SELECT sendAmount FROM changes WHERE orderId = "{orderId}"'
    ).fetchone()[0]
    sendCurrency = cursor.execute(
        f'SELECT sendCurrency FROM changes WHERE orderId = "{orderId}"'
    ).fetchone()[0]
    receiver = cursor.execute(
        f'SELECT receiver FROM changes WHERE orderId = "{orderId}"'
    ).fetchone()[0]
    email = cursor.execute(
        f'SELECT email FROM changes WHERE orderId = "{orderId}"'
    ).fetchone()[0]
    referalCode = cursor.execute(
        f'SELECT referalCode FROM changes WHERE orderId = "{orderId}"'
    ).fetchone()[0]
    status = cursor.execute(
        f'SELECT status FROM changes WHERE orderId = "{orderId}"'
    ).fetchone()[0]
    wallet = cursor.execute(
        f'SELECT wallet FROM coins WHERE shortName = "{sendCurrency}"'
    ).fetchone()[0]
    cursor.close()
    return (
        receiveAmount,
        receiveCurrency,
        sendAmount,
        sendCurrency,
        receiver,
        email,
        referalCode,
        status,
        wallet,
    )


def checkOrder(user_id):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("select * from changes where orderId = ?", (user_id,))
    usr = cursor.fetchone()
    cursor.close()
    return usr


def get_coins():
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(coins);")
    ids = cursor.execute(f"SELECT fullName FROM coins").fetchall()
    ids = [i[0] for i in ids]
    idd = cursor.execute(f"SELECT shortName FROM coins").fetchall()
    idd = [i[0] for i in idd]
    ida = cursor.execute(f"SELECT image FROM coins").fetchall()
    ida = [i[0] for i in ida]
    cursor.close()
    return ids, idd, ida


def get_categories():
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    id = cursor.execute(f"SELECT id FROM categories").fetchall()
    id = [i[0] for i in id]
    name = cursor.execute(f"SELECT name FROM categories").fetchall()
    name = [i[0] for i in name]
    thumb_url = cursor.execute(f"SELECT thumb_url FROM categories").fetchall()
    thumb_url = [i[0] for i in thumb_url]
    cursor.close()
    return id, name, thumb_url


def get_items(ids):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    id = cursor.execute(f"SELECT id FROM items WHERE category_id = {ids}").fetchall()
    id = [i[0] for i in id]
    name = cursor.execute(
        f'SELECT name FROM items WHERE category_id = "{ids}"'
    ).fetchall()
    name = [i[0] for i in name]
    description = cursor.execute(
        f'SELECT description FROM items WHERE category_id = "{ids}"'
    ).fetchall()
    description = [i[0] for i in description]
    thumb_url = cursor.execute(
        f'SELECT thumb_url FROM items WHERE category_id = "{ids}"'
    ).fetchall()
    thumb_url = [i[0] for i in thumb_url]
    cursor.close()
    return id, name, description, thumb_url


def getMessages(ids):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    messages = cursor.execute(
        f"SELECT text FROM messages WHERE userId = {ids}"
    ).fetchall()
    messages = [i[0] for i in messages]
    timestamp = cursor.execute(
        f"SELECT timestamp FROM messages WHERE userId = {ids}"
    ).fetchall()
    timestamp = [i[0] for i in timestamp]
    user = cursor.execute(f"SELECT user FROM messages WHERE userId = {ids}").fetchall()
    user = [i[0] for i in user]
    cursor.close()
    return messages, timestamp, user


def get_message(timestamp):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    msg = cursor.execute(
        f'SELECT text FROM messages WHERE timestamp = "{timestamp}"'
    ).fetchone()[0]
    cursor.close()
    return msg


def get_user(timestamp):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    receiveAmount = cursor.execute(
        f'SELECT user FROM messages WHERE timestamp = "{timestamp}"'
    ).fetchone()[0]
    cursor.close()
    return receiveAmount


def transactions():
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    txHash = cursor.execute(f"SELECT txHash FROM transactions").fetchall()
    txHash = [i[0] for i in txHash]
    block = cursor.execute(f"SELECT block FROM transactions").fetchall()
    block = [i[0] for i in block]
    fromm = cursor.execute(f"SELECT fromm FROM transactions").fetchall()
    fromm = [i[0] for i in fromm]
    to = cursor.execute(f"SELECT tos FROM transactions").fetchall()
    to = [i[0] for i in to]
    value = cursor.execute(f"SELECT value FROM transactions").fetchall()
    value = [i[0] for i in value]
    cursor.close()
    return txHash, block, fromm, to, value
