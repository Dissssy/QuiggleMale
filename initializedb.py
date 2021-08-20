import sqlite3

database = sqlite3.connect("./botdata.db")
cursor = database.cursor()

cursor.execute('CREATE TABLE C4DATA (GRID TEXT PRIMARY KEY, INDICES TEXT)')
database.commit()
cursor.execute("SELECT * FROM C4DATA")