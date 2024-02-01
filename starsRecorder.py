import sqlite3

con = sqlite3.connect(r"data\savings\starsRecorder.sqlite")
cur = con.cursor()


def firstTime():
    cur.execute("""CREATE TABLE IF NOT EXISTS stars(levelID INT PRIMARY KEY, isPassing INT, record INT, time INT)""")
    for i in range(1, 4):
        cur.execute(f"""
            INSERT INTO stars (levelID, isPassing, record, time) VALUES ({i}, 0, 0, 0) 
            ON CONFLICT (levelID) DO NOTHING
        """)
    con.commit()


def check_passing(whatLevel):
    req = f"""SELECT isPassing FROM stars WHERE levelID = {whatLevel}"""
    result = int(cur.execute(req).fetchone()[0])
    return result


def get_record(whatLevel):
    req = f"""SELECT record FROM stars WHERE levelID = {whatLevel}"""
    result = int(cur.execute(req).fetchone()[0])
    return result


def get_seconds(whatLevel):
    req = f"""SELECT time FROM stars WHERE levelID = {whatLevel}"""
    result = int(cur.execute(req).fetchone()[0])
    return result


def push_record(whatLevel, isPassing, record, time):
    req = f"""UPDATE stars SET isPassing = {isPassing}, record = {record}, time = {time} WHERE levelID = {whatLevel}"""
    cur.execute(req)
    con.commit()
