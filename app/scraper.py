import feedparser
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_mistral_api(prompt):
    """Mistral AI REST API - Ana Analiz Motoru."""
    if not MISTRAL_API_KEY:
        return "HATA: Mistral API Key eksik."
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MISTRAL_API_KEY}"
    }
    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Mistral Analiz Hatası: {str(e)}"

def call_openrouter_api(prompt):
    """OpenRouter API - Daha güncel model (Llama 3.1 70B veya Gemini 2.0)."""
    if not OPENROUTER_API_KEY:
        return "OpenRouter API Key tanımlanmadı."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "CyberPulse SOC"
    }
    
    # Not: Llama 3.1 (70B) çok daha güncel ve zekidir. 
    # Alternatif olarak OpenRouter üzerinden "google/gemini-2.0-flash-001" de kullanabilirsin (Sorunsuz çalışır).
    payload = {
        "model": "meta-llama/llama-3.1-70b-instruct", 
        "messages": [
            {"role": "system", "content": "Sen kıdemli bir siber güvenlik analistisin. Verilen CVE veya tehdidi elindeki bilgilerle en iyi şekilde yorumla."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"OpenRouter Hatası: {str(e)}"

def analyze_criticality(title, summary):
    text = (title + " " + (summary or "")).lower()
    critical_keywords = ['rce', 'zero-day', 'exploit', 'critical', 'active attack', 'ransomware']
    if any(word in text for word in critical_keywords):
        return "🔴 KRİTİK"
    return "🟢 DÜŞÜK"

def get_enterprise_ai_analysis(title, summary):
    prompt = f"Senior SOC Analisti olarak şu haberi Türkçe analiz et:\n{title}\nÖzet: {summary}"
    return call_mistral_api(prompt)

def get_ai_analysis_for_tool(q_type, q_val):
    if q_type == "CVE":
        prompt = f"{q_val} kodlu siber güvenlik zafiyetini incele. Bu zafiyet yeni olabilir, genel zafiyet türüne göre (örn: RCE, SQLi) olası riskleri ve çözüm yollarını Türkçe raporla."
    else:
        prompt = f"{q_val} değerini tehdit istihbaratı açısından analiz et. Risk skorunu Türkçe belirt."
    
    mistral_res = call_mistral_api(prompt)
    openrouter_res = call_openrouter_api(prompt)
    
    return f"🛡️ [MISTRAL SOC ANALİZİ]\n{mistral_res}\n\n" \
           f"-----------------------------------\n\n" \
           f"🚀 [OPENROUTER (LLAMA-3.1) ANALİZİ]\n{openrouter_res}"

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
