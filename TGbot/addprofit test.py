import sqlite3

def addProfit(user_id,profits_amount):
    with sqlite3.connect("database.db",check_same_thread=False) as conn:
        cursor = conn.cursor()
    amount = cursor.execute(f'''
    UPDATE users 
    SET profits_count = profits_count + 1, 
        profits_amount = profits_amount + {profits_amount} 
    WHERE user_id = {user_id}
''')
    cursor.close()
    return amount.execute

print(addProfit(7524127341, 1161.0))