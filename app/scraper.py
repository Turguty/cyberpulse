import feedparser
from feeds import RSS_FEEDS

def analyze_criticality(title, summary):
    text = (title + " " + (summary or "")).lower()
    critical = ['rce', 'zero-day', 'critical', 'vulnerability', 'exploit', 'active attack', 'ransomware']
    medium = ['patch', 'update', 'security fix', 'malware', 'phishing']
    
    if any(word in text for word in critical):
        return "🔴 KRİTİK"
    if any(word in text for word in medium):
        return "🟠 ORTA"
    return "🟢 DÜŞÜK"

def fetch_all_news():
    all_extracted_news = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]: # Her kaynaktan son 10 haber
                all_extracted_news.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.get('summary', ''),
                    "tr_link": f"https://translate.google.com/translate?sl=en&tl=tr&u={entry.link}",
                    "criticality": analyze_criticality(entry.title, entry.get('summary', ''))
                })
        except Exception as e:
            print(f"Hata oluştu ({url}): {e}")
    return all_extracted_news
