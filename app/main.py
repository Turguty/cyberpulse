from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

# Örnek veri çekme fonksiyonu (Haberler için)
def get_cyber_news():
    # Bu kısım senin mevcut haber çekme mantığına göre düzenlenmiştir
    # Örnek statik veri (API'den geliyormuş gibi)
    return [
        {
            "published_date": datetime.now().strftime("%H:%M:%S"),
            "title": "Yeni Critical RCE Zafiyeti Tespit Edildi (CVE-2026-XXXX)",
            "link": "https://example.com/news1",
            "criticality": "YÜKSEK"
        },
        {
            "published_date": datetime.now().strftime("%H:%M:%S"),
            "title": "Büyük Bir Botnet Ağı Çökertildi",
            "link": "https://example.com/news2",
            "criticality": "ORTA"
        }
    ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    news = get_cyber_news()
    return jsonify({"news": news})

# --- HIZLI ANALİZ ÜNİTESİ (CVE / IP SORGULAMA) ---
@app.route('/api/tool', methods=['POST'])
def run_tool():
    data = request.json
    tool_type = data.get('type')
    value = data.get('value', '').strip()

    if not value:
        return jsonify({"result": "Lütfen bir değer girin."})

    if tool_type == 'cve':
        # Burada gerçek bir CVE API'si (örn. NVD) bağlanabilir
        result = f"🔍 {value} Analizi: Bu zafiyet kritik seviyede olup acil yama gerektirmektedir."
    elif tool_type == 'ip':
        # Burada bir IP Intel API'si (örn. VirusTotal/AbuseIPDB) bağlanabilir
        result = f"🌐 {value} Analizi: Bu IP adresi zararlı faaliyetler ile ilişkilendirilmiştir."
    else:
        result = "Bilinmeyen araç tipi."

    return jsonify({"result": result})

# --- YENİ: AI ANALİZ ÜNİTESİ (AI SOR BUTONU İÇİN) ---
@app.route('/api/ai-analyze', methods=['POST'])
def ai_analyze():
    data = request.json
    title = data.get('title', '')
    
    if not title:
        return jsonify({"result": "Analiz edilecek başlık bulunamadı."}), 400

    # Bu alan ileride gerçek bir AI (Gemini/GPT) API'si ile değiştirilebilir.
    # Mevcut tasarımda 'tool-result' kutusuna profesyonel bir analiz döner.
    analysis = (
        f"🤖 **CyberPulse AI Analizi**\n\n"
        f"**Konu:** {title}\n"
        f"**Değerlendirme:** Bu olay siber güvenlik ekosisteminde orta-yüksek risk barındırmaktadır.\n"
        f"**Öneri:** Sistem loglarını inceleyin, ağ trafiğini bu başlığa göre filtreleyin ve zafiyet varsa yamaları kontrol edin."
    )
    
    return jsonify({"result": analysis})

if __name__ == '__main__':
    # Docker konteyner içinde çalışması için host='0.0.0.0' şart
    app.run(debug=True, host='0.0.0.0', port=5000)
