from flask import Flask, render_template
import sqlite3
import pandas as pd

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('cyberpulse.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    # Son 20 haberi çek
    news_list = conn.execute('SELECT * FROM news ORDER BY published_date DESC LIMIT 20').fetchall()
    
    # Grafik verileri için kritiklik sayılarını hesapla
    stats = conn.execute('SELECT criticality, COUNT(*) as count FROM news GROUP BY criticality').fetchall()
    
    conn.close()
    
    # Grafik için etiketler ve veriler
    labels = [row['criticality'] for row in stats]
    values = [row['count'] for row in stats]
    
    return render_template('index.html', news=news_list, labels=labels, values=values)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
