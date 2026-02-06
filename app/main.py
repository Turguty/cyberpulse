import os
import json
import requests
from flask import Flask, render_template, jsonify, request
from datetime import datetime
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

app = Flask(__name__)

# Yapılandırmayı ortam değişkenlerinden çekiyoruz
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "mistralai/mistral-7b-instruct:free"

def get_cyber_news():
    # Mevcut haber botu fonksiyonunuzla burayı besleyebilirsiniz
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
        return jsonify({"result": "Analiz için başlık iletilmedi."}), 400

    if not OPENROUTER_API_KEY:
        return jsonify({"result": "Hata: API anahtarı .env dosyasında bulunamadı!"}), 500

    prompt = (
        f"Sen profesyonel bir siber güvenlik analistisin. Aşağıdaki haber başlığını analiz et: '{title}'. "
        f"Bu olayın teknik risklerini ve SOC ekiplerinin alması gereken 3 somut önlemi kısa maddeler halinde Türkçe olarak açıkla."
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
            return jsonify({"result": f"AI Servis Hatası (Kod: {response.status_code})"}), 500

    except Exception as e:
        return jsonify({"result": f"Bağlantı Hatası: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
