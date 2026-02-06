import os
import time
import requests
from dotenv import load_dotenv
from scraper import fetch_all_news
from database import init_db, is_news_exists, save_news

# .env dosyasını yükle
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(news):
    message = (
        f"🚨 *YENİ SİBER HABER*\n\n"
        f"📌 *Başlık:* {news['title']}\n"
        f"🛡 *Seviye:* {news['criticality']}\n\n"
        f"🔗 [Orijinal Haber]({news['link']})\n"
        f"🇹🇷 [Türkçe Çeviri]({news['tr_link']})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": False}
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram gönderme hatası: {e}")
        return False

def start_bot():
    init_db()
    print("Sistem aktif, haberler taranıyor...")
    
    while True:
        news_list = fetch_all_news()
        new_items_found = 0
        
        for item in news_list:
            # Veritabanında yoksa gönder ve kaydet
            if not is_news_exists(item['link']):
                if send_to_telegram(item):
                    save_news(item['title'], item['link'], item['criticality'])
                    new_items_found += 1
                    time.sleep(3) # Telegram API limiti için bekleme
        
        if new_items_found > 0:
            print(f"{new_items_found} yeni haber gönderildi.")
        
        # 30 dakikada bir kontrol et
        print("Kontrol tamamlandı, 30 dakika bekleniyor...")
        time.sleep(1800)

if __name__ == "__main__":
    start_bot()
