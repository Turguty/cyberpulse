import os
import time
import datetime
import sys
from dotenv import load_dotenv

# Path ayarı
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
        f"🚨 *YENİ TEHDİT ANALİZİ*\n\n"
        f"📌 *Başlık:* {news['title']}\n"
        f"🛡 *Kritiklik:* {news['criticality']}\n\n"
        f"🤖 *AI Analizi:*\n{news['ai_analysis']}\n\n"
        f"🔗 [Kaynağa Git]({news['link']})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        print(f"Telegram Hatası: {e}")

if __name__ == "__main__":
    init_db()
    print(f"[{datetime.datetime.now()}] CyberPulse SOC Engine Aktif...")
    
    while True:
        try:
            news_list = fetch_all_news()
            for item in news_list:
                if not is_news_exists(item['link']):
                    # Önemli haber kontrolü
                    is_important = any(k in item['title'].lower() for k in WATCH_KEYWORDS) or "🔴" in item['criticality']
                    
                    if is_important:
                        item['ai_analysis'] = get_enterprise_ai_analysis(item['title'], item['summary'])
                        send_to_telegram(item)
                        save_news(item['title'], item['link'], item['criticality'], item['ai_analysis'])
                        time.sleep(5) # API Kotasını korumak için bekleme
            
            print(f"[{datetime.datetime.now()}] Tarama tamamlandı. 15 dk uyku...")
            time.sleep(900)
        except Exception as e:
            print(f"Hata oluştu: {e}")
            time.sleep(60)
