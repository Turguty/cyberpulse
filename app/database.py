import sqlite3
import os

# Docker içindeki çalışma dizinine göre göreceli yol kullanıyoruz
# Bu sayede /app/data/cyberpulse.db oluşur
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'cyberpulse.db')

def init_db():
    """Veritabanını ve klasörünü güvenli bir şekilde oluşturur."""
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT UNIQUE,
            title TEXT,
            criticality TEXT,
            ai_analysis TEXT,
            published_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Veritabanı kontrol edildi: {DB_PATH}")

def is_news_exists(link):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM news WHERE link = ?', (link,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_news(title, link, criticality, ai_analysis):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO news (title, link, criticality, ai_analysis) 
            VALUES (?, ?, ?, ?)
        ''', (title, link, criticality, ai_analysis))
        conn.commit()
    except Exception as e:
        print(f"DB Kayıt Hatası: {e}")
    finally:
        conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
