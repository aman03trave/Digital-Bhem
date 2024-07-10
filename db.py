import sqlite3

# Connect to the database
conn = sqlite3.connect('bmi_calculator.db')

# Create a cursor
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                name TEXT,
                age INTEGER,
                height REAL,
                weight REAL)''')

# Commit and close the connection
conn.commit()
conn.close()