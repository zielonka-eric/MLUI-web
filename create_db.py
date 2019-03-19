import sqlite3

conn = sqlite3.connect('database.db')

with open("schema.sql", mode="r") as f:
    conn.cursor().executescript(f.read())
conn.commit()