import sqlite3
import os
import time


def createDb():
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (user_id INTEGER,user_name TEXT,code TEXT,registration INTEGER,profits_count INTEGER,profits_amount FLOAT, privilege TEXT)"""
    )
    cursor.execute("""CREATE TABLE IF NOT EXISTS code (value INTEGER)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS banlist (id INTEGER)""")
    cursor.close()


# Создаем путь к файлу в папке server
current_path = os.path.dirname(os.path.abspath(__file__))
server_file_path = os.path.join(current_path, "..", "..", "..", "server", "database.db")


# USER MANAGEMENT ---------------------------------------------------------------------------------------------------------------------------


def checkUser(user_id):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("select * from users where user_id = ?", (user_id,))
    usr = cursor.fetchone()
    cursor.close()
    return usr


def registerUser(user_id, user_name, code, ts, priv):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users values (:user_id,:user_name,:code,:registration, :profits_count, :profits_amount, :privilege);",
        {
            "user_id": user_id,
            "user_name": user_name,
            "code": code,
            "registration": ts,
            "profits_count": 0,
            "profits_amount": 0,
            "privilege": priv,
        },
    )
    conn.commit()
    cursor.close()
    return


def removeUser(user_id):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    cursor.close()
    return


def getRefCode(user_id):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    code = cursor.execute(
        f"SELECT code FROM users WHERE user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    return code


def getProfitsCount(user_id):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    count = cursor.execute(
        f"SELECT profits_count FROM users WHERE user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    return count


def getCode(user_id):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    amount = cursor.execute(
        f"SELECT code FROM users WHERE user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    return amount


def getProfitsAmount(user_id):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    amount = cursor.execute(
        f"SELECT profits_amount FROM users WHERE user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    return amount


def addProfit(user_id, profits_amount):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    amount = cursor.execute(
        f"""
    UPDATE users 
    SET profits_count = profits_count + 1, 
        profits_amount = profits_amount + {profits_amount} 
    WHERE user_id = {user_id}
"""
    )
    conn.commit()
    cursor.close()
    return amount


def getAllUsers():
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()

    # SQL query to select all user_id from the users table
    query = "SELECT user_id FROM users;"

    try:
        # Execute the SQL query
        cursor.execute(query)

        # Fetch all results
        user_ids = cursor.fetchall()  # This returns a list of tuples

        # Extract user IDs from the tuples to a flat list if needed
        user_ids_list = [
            user_id[0] for user_id in user_ids
        ]  # Get the first element from each tuple

        # Print the list of user IDs

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
        return user_ids_list


def listUserDb():
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM users;"
        cursor.execute(query)
        table = cursor.fetchall()
        return table


def getRegistration(user_id):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    code = cursor.execute(
        f"SELECT registration FROM users WHERE user_id = {user_id}"
    ).fetchone()[0]
    cursor.close()
    return code


def ban(user_id):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("INSERT INTO banlist (id) VALUES (?)", (user_id,))
    conn.commit()
    cursor.close()


def checkIfBanned(user_id):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute("select * from banlist where id = ?", (user_id,))
    usr = cursor.fetchone()
    cursor.close()
    return usr


def checkPriv(userId):
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    priv = cursor.execute(
        f"SELECT privilege FROM users WHERE user_id = {userId}"
    ).fetchone()[0]
    cursor.close()
    return priv


# MESSAGE MANAGEMENT ---------------------------------------------------------------------------------------------------------------------------


def chatBan(user_id):
    with sqlite3.connect(server_file_path, check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(f"UPDATE chat_users SET chatbanned = True WHERE id = {user_id}")
    conn.commit()
    cursor.close()
    return


def addMsg(user_id, text, ts):
    with sqlite3.connect(server_file_path, check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages values (:text, :userId, :timestamp, :user);",
        {"text": text, "userId": user_id, "timestamp": ts, "user": "false"},
    )
    conn.commit()
    cursor.close()
    return


def clMsg(user_id):
    with sqlite3.connect(server_file_path, check_same_thread=False) as conn:
        cursor = conn.cursor()
    # SQL query to delete all records for the specified userId
    delete_query = """
        DELETE FROM messages
        WHERE userId = ?;
    """

    # Execute the query
    cursor.execute(delete_query, (user_id,))
    conn.commit()
    cursor.close()
    return


def delete_old_messages():
    conn = sqlite3.connect(server_file_path, check_same_thread=False)
    cursor = conn.cursor()

    # Get the current timestamp (you might need to adjust the format)
    current_time = int(time.time() * 1000)  # Current time in milliseconds
    five_minutes_ago = current_time - (5 * 60 * 1000)  # 5 minutes in milliseconds

    # SQL query to delete all records older than 5 minutes
    delete_query = """
        DELETE FROM messages
        WHERE timestamp < ?;
    """

    # Execute the query
    cursor.execute(delete_query, (five_minutes_ago,))

    # Commit the changes
    conn.commit()
    return


# MISC ------------------------------------------------------------------------------------------------------------


def getCurrentCode():
    with sqlite3.connect("database.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    code = cursor.execute(f"SELECT value FROM code").fetchone()[0]
    cursor.close()
    return code


def changeStatusToReturned(orderId):
    with sqlite3.connect(server_file_path, check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(f'UPDATE changes SET status = "passed" WHERE orderId = "{orderId}"')
    conn.commit()
    cursor.close()


def changeStatusToErr(orderId):
    with sqlite3.connect(server_file_path, check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(f'UPDATE changes SET status = "error" WHERE orderId = "{orderId}"')
    conn.commit()
    cursor.close()


def changeStatus(coin, wallet):
    with sqlite3.connect(server_file_path, check_same_thread=False) as conn:
        cursor = conn.cursor()
    cursor.execute(f'UPDATE coins SET wallet = "{wallet}" WHERE image = "{coin}"')
    conn.commit()
    cursor.close()
