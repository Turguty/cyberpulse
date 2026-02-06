import os
import json
import requests
from flask import Flask, render_template, jsonify, request
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# --- .ENV YOLU DÜZELTMESİ ---
# main.py'nin bulunduğu klasörün (app) bir üst dizinine git ve .env'yi bul
base_path = Path(__file__).resolve().parent.parent
env_path = os.path.join(base_path, '.env')
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# Yapılandırma
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "mistralai/mistral-7b-instruct:free"

# Debug için (Terminalde/Loglarda anahtarın gelip gelmediğini gör)
print(f"--- BAŞLATMA ---")
print(f"Aranan .env yolu: {env_path}")
print(f"API Anahtarı Yüklendi mi: {bool(OPENROUTER_API_KEY)}")
print(f"----------------")

def get_cyber_news():
    return [
        {
            "published_date": datetime.now().strftime("%H:%M:%S"),
            "title": "Microsoft Outlook Spoofing Vulnerability (CVE-2024-XXXX)",
            "link": "https://cve.mitre.org",
            "criticality": "YÜKSEK"
        }
    ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    return jsonify({"news": get_cyber_news()})

@app.route('/api/tool', methods=['POST'])
def run_tool():
    data = request.json
    tool_type = data.get('type')
    value = data.get('value', '').strip()
    result = f"🔍 {value} için {tool_type.upper()} sorgusu tamamlandı."
    return jsonify({"result": result})

@app.route('/api/ai-analyze', methods=['POST'])
def ai_analyze():
    data = request.json
    title = data.get('title', '')
    
    if not title:
        return jsonify({"result": "Başlık bulunamadı."}), 400

    if not OPENROUTER_API_KEY:
        return jsonify({"result": "Hata: .env dosyası kök dizinde bulunamadı veya anahtar boş!"}), 500

    prompt = (
        f"Sen bir siber güvenlik uzmanısın. Şu haberi analiz et: '{title}'. "
        f"3 kısa maddede riskleri ve önlemleri Türkçe açıkla."
    )

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": prompt}]
            }),
            timeout=20
        )
        
        if response.status_code == 200:
            ai_response = response.json()['choices'][0]['message']['content']
            return jsonify({"result": ai_response})
        else:
            return jsonify({"result": f"AI Servis Hatası: {response.status_code}"}), 500

    except Exception as e:
        return jsonify({"result": f"Bağlantı Hatası: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
