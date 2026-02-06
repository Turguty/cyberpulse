import os
import time
from dotenv import load_dotenv
from scraper import fetch_all_news, get_enterprise_ai_analysis
from database import init_db, is_news_exists, save_news
from feeds import WATCH_KEYWORDS
import requests

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(news):
    message = f"🚨 *{news['title']}*\n🛡 Seviye: {news['criticality']}\n\n🤖 *Analiz:*\n{news['ai_analysis']}\n\n🔗 [Haber]({news['link']})"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

if __name__ == "__main__":
    init_db()
    while True:
        try:
            news_list = fetch_all_news()
            for item in news_list:
                if not is_news_exists(item['link']):
                    is_ent = any(k in item['title'].lower() for k in WATCH_KEYWORDS)
                    if is_ent or "🔴" in item['criticality']:
                        item['ai_analysis'] = get_enterprise_ai_analysis(item['title'], item['summary'])
                        send_to_telegram(item)
                        save_news(item['title'], item['link'], item['criticality'], item['ai_analysis'])
            time.sleep(900)
        except Exception as e:
            time.sleep(60)
