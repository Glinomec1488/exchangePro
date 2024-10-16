import sqlite3
import os




def createDb():
    with sqlite3.connect("database.db",check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER,user_name TEXT,code TEXT,registration INTEGER,profits_count INTEGER,profits_amount FLOAT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS code (value INTEGER)""")
    cursor.close()
    
def checkUser(user_id):
    with sqlite3.connect("database.db",check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("select * from users where user_id = ?",(user_id,))
    usr = cursor.fetchone()
    cursor.close()
    return usr

def registerUser(user_id,user_name,code,ts):
    with sqlite3.connect("database.db",check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("INSERT INTO users values (:user_id,:user_name,:code,:registration, :profits_count, :profits_amount);" ,
            {'user_id': user_id,
            'user_name': user_name,
            'code': code,
            'registration': ts,
            'profits_count': 0,
            'profits_amount': 0})
    conn.commit()
    cursor.close()
    return

def addMsg(user_id,text,ts):
    with sqlite3.connect("/Users/levanta1s/Desktop/dev/Worker's Club/exchange_back/database.db",check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("INSERT INTO messages values (:text, :userId, :timestamp, :user);" ,
            {'text': text,
            'userId': user_id,
            'timestamp': ts,
            'user': 'false'})
    conn.commit()
    cursor.close()
    return


def getCurrentCode():
    with sqlite3.connect("database.db",check_same_thread=False) as conn:
        cursor = conn.cursor()
    code = cursor.execute(f'SELECT value FROM code').fetchone()[0]
    cursor.close()
    return code

current_path = os.path.dirname(os.path.abspath(__file__))

# Создаем путь к файлу в папке server
server_file_path = os.path.join(current_path, "..", "..", "..", "server", "database.db")
print(server_file_path)

def changeStatus(coin,wallet):
    with sqlite3.connect('../server/database.db',check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(f'UPDATE coins SET wallet = "{wallet}" WHERE image = "{coin}"')
    conn.commit()
    cursor.close()

def getRefCode(user_id):
    with sqlite3.connect("database.db",check_same_thread=False) as conn:
        cursor = conn.cursor()
    code = cursor.execute(f'SELECT code FROM users WHERE user_id = {user_id}').fetchone()[0]
    cursor.close()
    return code

def getProfitsCount(user_id):
    with sqlite3.connect("database.db",check_same_thread=False) as conn:
        cursor = conn.cursor()
    count = cursor.execute(f'SELECT profits_count FROM users WHERE user_id = {user_id}').fetchone()[0]
    cursor.close()
    return count

def getCode(user_id):
    with sqlite3.connect("database.db",check_same_thread=False) as conn:
        cursor = conn.cursor()
    amount = cursor.execute(f'SELECT code FROM users WHERE user_id = {user_id}').fetchone()[0]
    cursor.close()
    return amount

def getProfitsAmount(user_id):
    with sqlite3.connect("database.db",check_same_thread=False) as conn:
        cursor = conn.cursor()
    amount = cursor.execute(f'SELECT profits_amount FROM users WHERE user_id = {user_id}').fetchone()[0]
    cursor.close()
    return amount

def getRegistration(user_id):
    with sqlite3.connect("database.db",check_same_thread=False) as conn:
        cursor = conn.cursor()
    code = cursor.execute(f'SELECT registration FROM users WHERE user_id = {user_id}').fetchone()[0]
    cursor.close()
    return code


