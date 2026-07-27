import sqlite3

conn = sqlite3.connect("banlist.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS blacklist")

cursor.execute("""
CREATE TABLE blacklist (

    user_id INTEGER PRIMARY KEY,
    username TEXT,
    nome TEXT,
    motivo TEXT,
    data TEXT

)
""")

conn.commit()
conn.close()

print("Database aggiornato correttamente")