import sqlite3

# Connect to the database
connection = sqlite3.connect('diary.db')
cursor = connection.cursor()

# Create the entries table if it doesn’t exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        date TEXT NOT NULL,
        deleted INTEGER DEFAULT 0
    )
''')

# Commit changes and close the connection
connection.commit()
connection.close()
print("Database initialized successfully.")
