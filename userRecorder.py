import sqlite3

con = sqlite3.connect(r"data\savings\starsRecorder.sqlite")
cur = con.cursor()


def userIdentity(user_name):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS
            user(name TEXT, password TEXT, level_amount INT, time INT)
        """)
    req = """
        INSERT INTO user (name, password, level_amount, time)
        VALUES (?, ?, ?, ?)
    """
    cur.execute(req, (user_name, "12345", 0, 0))
    con.commit()


def get_user(user_name):
    req = f"""SELECT * FROM user WHERE name = '{user_name}'"""
    result = list(cur.execute(req).fetchone())
    return result


def check_existence():
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
    table_exists = cur.fetchone()
    print(table_exists)
    return table_exists
