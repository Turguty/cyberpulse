import feedparser
import os
import requests
import json
from dotenv import load_dotenv
from feeds import RSS_FEEDS

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
# REST API endpoint - v1beta yerine v1 (stable) kullanıyoruz
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def call_gemini_api(prompt):
    """SDK hatalarından kaçınmak için doğrudan HTTP POST isteği atar."""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 800}
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"API Hatası: {e}")
        return "Analiz şu an yapılamıyor, lütfen API anahtarınızı veya bağlantınızı kontrol edin."

def analyze_criticality(title, summary):
    text = (title + " " + (summary or "")).lower()
    critical = ['rce', 'zero-day', 'critical', 'exploit', 'active attack', 'ransomware']
    if any(word in text for word in critical): return "🔴 KRİTİK"
    if any(word in text for word in ['patch', 'update', 'fix', 'cve-202']): return "🟠 ORTA"
    return "🟢 DÜŞÜK"

def get_enterprise_ai_analysis(title, summary):
    prompt = f"Senior SOC Analisti olarak bu haberi analiz et: {title}\nÖzet: {summary}\nFormat: Önem, Teknik Çözüm ve Tavsiye (Türkçe, kısa)."
    return call_gemini_api(prompt)

def get_ai_analysis_for_tool(q_type, q_val):
    if q_type == "CVE":
        prompt = f"{q_val} kodlu zafiyeti araştır. Teknik detay ve çözüm yollarını Türkçe raporla."
    else:
        prompt = f"{q_val} değerini siber tehdit istihbaratı açısından analiz et. Risk durumunu Türkçe belirt."
    return call_gemini_api(prompt)

def fetch_all_news():
    all_extracted_news = []
    seen_links = set()
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                if entry.link not in seen_links:
                    all_extracted_news.append({
                        "title": entry.title, "link": entry.link,
                        "summary": entry.get('summary', ''),
                        "tr_link": f"https://translate.google.com/translate?sl=en&tl=tr&u={entry.link}",
                        "criticality": analyze_criticality(entry.title, entry.get('summary', ''))
                    })
                    seen_links.add(entry.link)
        except: continue
    return all_extracted_news
