import sqlite3

con = sqlite3.connect(r"data\savings\starsRecorder.sqlite")
cur = con.cursor()

req = f"""SELECT * FROM test"""
result = list(cur.execute(req).fetchone())
print(result)
