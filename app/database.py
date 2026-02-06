import sqlite3

def init_db():
    conn = sqlite3.connect('cyberpulse.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT UNIQUE,
            title TEXT,
            criticality TEXT,
            published_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_news_exists(link):
    conn = sqlite3.connect('cyberpulse.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM news WHERE link = ?', (link,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_news(title, link, criticality):
    conn = sqlite3.connect('cyberpulse.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO news (title, link, criticality) VALUES (?, ?, ?)', 
                       (title, link, criticality))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Zaten varsa kaydetme
    finally:
        conn.close()
