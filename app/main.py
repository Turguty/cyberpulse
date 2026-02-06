import os
import time
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper import fetch_all_news, get_enterprise_ai_analysis
from database import init_db, is_news_exists, save_news
from feeds import WATCH_KEYWORDS
import requests

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(news):
    message = (
        f"🌪️ *SOC ANALİZ RAPORU*\n\n"
        f"📌 *Başlık:* {news['title']}\n"
        f"🛡 *Risk:* {news['criticality']}\n\n"
        f"🤖 *Analiz:*\n{news['ai_analysis']}\n\n"
        f"🔗 [Haber Detayı]({news['link']})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}, timeout=15)
    except:
        pass

@app.route('/api/ai-analyze', methods=['POST'])
def ai_analyze():
    data = request.json
    news_title = data.get('title', '')
    
    # Burada AI modeline gönderilecek promptu hazırlıyoruz
    prompt = f"Aşağıdaki siber güvenlik haberini analiz et ve 3 kısa maddede risklerini açıkla: {news_title}"
    
    try:
        # Örnek: Eğer Gemini veya başka bir AI entegrasyonun varsa burada çağırabilirsin.
        # Şimdilik stabilite için hızlı bir analiz taslağı döndürüyoruz:
        result = f"🔍 AI Analizi ({news_title}):\n1. Potansiyel sızma riski barındırıyor.\n2. Sistem yamalarının kontrol edilmesi önerilir.\n3. İlgili portlar izlenmelidir."
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": "AI analizi sırasında bir hata oluştu."}), 500



if __name__ == "__main__":
    init_db()
    print("CyberPulse SOC Engine Aktif (Dual AI Mode)...")
    
    while True:
        try:
            news_list = fetch_all_news()
            for item in news_list:
                if not is_news_exists(item['link']):
                    is_imp = any(k in item['title'].lower() for k in WATCH_KEYWORDS) or "🔴" in item['criticality']
                    
                    if is_imp:
                        item['ai_analysis'] = get_enterprise_ai_analysis(item['title'], item['summary'])
                        send_to_telegram(item)
                        save_news(item['title'], item['link'], item['criticality'], item['ai_analysis'])
                        time.sleep(2)
            
            time.sleep(900)
        except Exception as e:
            print(f"Hata: {e}")
            time.sleep(60)
