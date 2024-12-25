import sqlite3

def create_database():
    conn = sqlite3.connect("wiki_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wiki_pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            introduction TEXT NOT NULL,
            first_image TEXT,
            history_content TEXT  -- Allow NULL values
        )
    ''')
    conn.commit()
    conn.close()

create_database()

def insert_data(title, introduction, first_image, history_content):
    conn = sqlite3.connect("wiki_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO wiki_pages (title, introduction, first_image, history_content)
        VALUES (?, ?, ?, ?)
    ''', (title, introduction, first_image, history_content or ""))
    conn.commit()
    conn.close()
    print("Data inserted successfully!")
