import feedparser
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini_api(prompt):
    """Google Gemini v1 (Stable) REST API çağrısı."""
    # API URL'sini v1beta'dan v1'e (kararlı) çektik
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 800,
            "topP": 0.8
        }
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 429:
            return "⚠️ Kota doldu. Lütfen 1 dakika bekleyin."
            
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"AI Analiz Hatası: {str(e)}"

def analyze_criticality(title, summary):
    text = (title + " " + (summary or "")).lower()
    critical_keywords = ['rce', 'zero-day', 'exploit', 'critical', 'active attack', 'ransomware', 'unauthenticated']
    if any(word in text for word in critical_keywords):
        return "🔴 KRİTİK"
    return "🟢 DÜŞÜK"

def get_enterprise_ai_analysis(title, summary):
    """Haberler için otomatik analiz."""
    prompt = f"Senior SOC Analisti olarak bu siber güvenlik haberini analiz et:\nBaşlık: {title}\nÖzet: {summary}\n\nFormat: Kısa Teknik Analiz ve Acil Tavsiye (Türkçe)."
    return call_gemini_api(prompt)

def get_ai_analysis_for_tool(q_type, q_val):
    """DASHBOARD'daki CVE/IP sorgusu için gereken EKSİK FONKSİYON."""
    if q_type == "CVE":
        prompt = f"{q_val} kodlu siber güvenlik zafiyetini (CVE) derinlemesine araştır. Etkilenen sistemleri ve kapatma yöntemlerini Türkçe raporla."
    else:
        prompt = f"{q_val} değerini Tehdit İstihbaratı (TI) açısından analiz et. İtibar ve risk durumunu Türkçe açıkla."
    return call_gemini_api(prompt)

def fetch_all_news():
    from feeds import RSS_FEEDS
    all_extracted_news = []
    seen_links = set()
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                if entry.link not in seen_links:
                    all_extracted_news.append({
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.get('summary', ''),
                        "tr_link": f"https://translate.google.com/translate?sl=en&tl=tr&u={entry.link}",
                        "criticality": analyze_criticality(entry.title, entry.get('summary', ''))
                    })
                    seen_links.add(entry.link)
        except:
            continue
    return all_extracted_news
