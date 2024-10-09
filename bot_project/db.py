import sqlite3 as sql

con = sql.connect('gold_users.db')

with con:
    db = con.cursor()
    db.execute("""CREATE TABLE IF NOT EXISTS `users`
            (id INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 0, 
            vk_id STRING,
            name STRING,
            surname STRING,
            clicks INTEGER DEFAULT 0,
            gold INTEGER DEFAULT 0,
            day_bonus STRING DEFAULT NONE)
            """)
    con.commit()


def rows():
    db.execute("SELECT COUNT(*) FROM 'users'")
    con.commit()
    values = db.fetchone()
    return int(values[0])

class UsersInfo:
    def is_reg(user_vk_id):
        db.execute(f"SELECT * FROM 'users' WHERE vk_id= '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        if values is None:
            return False
        else:
            return True

    def insert(user_vk_id, name, surname):
        db.execute(f"INSERT INTO 'users' (vk_id, name, surname) VALUES (?, ?, ?)", (user_vk_id, name, surname))
        con.commit()

    def get_clicks(user_vk_id):
        db.execute(f"SELECT clicks FROM 'users' WHERE vk_id = '{user_vk_id}'")
        con.commit()
        values = db.fetchone()
        return values[0]
    def get_gold(user_vk_id):
        db.execute(f'SELECT gold FROM "users" WHERE vk_id = {user_vk_id}')
        con.commit()
        values = db.fetchone()
        return values[0]
    def get_info(user_vk_id):
        db.execute(f'SELECT name, surname FROM "users" WHERE vk_id = {user_vk_id}')
        value = db.fetchone()
        return value
    def check_get_bonus(user_vk_id, now):
        db.execute(f'SELECT day_bonus FROM "users" WHERE vk_id = {user_vk_id}')
        value = db.fetchone()[0]
        con.commit()
        if str(value) == str(now):
            return False
        else:
            db.execute(f'UPDATE "users" SET day_bonus = {str(now)} WHERE vk_id = {user_vk_id}')
            con.commit()
            return True

    def update(user_vk_id, clicks):
        db.execute(f"UPDATE 'users' SET clicks = {clicks} WHERE vk_id = {user_vk_id}")
        con.commit()
    def update_gold(user_vk_id, gold):
        db.execute(f'UPDATE "users" SET gold = {gold} WHERE vk_id = {user_vk_id}')
        con.commit()
    def check_prime(user_vk_id):
        db.execute(f'SELECT prime_status FROM "users" WHERE vk_id = {user_vk_id}')
        value = db.fetchone()[0]
        if value != 'bought':
            return 'Отсутствует'
        else:
            return 'Куплен'
    def buy_prime(user_vk_id):
        db.execute(f'UPDATE "users" SET prime_status = bought WHERE vk_id = {user_vk_id}')
        con.commit()


    def get_top(count):
        db.execute(f"SELECT vk_id, clicks FROM 'users' ORDER BY clicks DESC LIMIT {count}")
        con.commit()
        values = db.fetchall()
        return values
