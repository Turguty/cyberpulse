import feedparser
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini_api(prompt):
    # Endpoint v1 (Stable) olarak ayarlandı
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 600}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        # Kota hatası (429) kontrolü
        if response.status_code == 429:
            return "⚠️ API Kotası doldu (Free Tier). Lütfen 1 dakika bekleyin."
        
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Analiz Hatası: {str(e)}"

def analyze_criticality(title, summary):
    txt = (title + (summary or "")).lower()
    if any(x in txt for x in ['rce', 'exploit', 'critical', '0-day']): return "🔴 KRİTİK"
    return "🟢 DÜŞÜK"

def get_enterprise_ai_analysis(title, summary):
    prompt = f"Analist Notu: {title}\nÖzet: {summary}\nKısa Teknik Tavsiye ver (Türkçe)."
    return call_gemini_api(prompt)
