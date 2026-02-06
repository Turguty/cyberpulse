RSS_FEEDS = [
    # Vendor & Enterprise Security
    "https://www.paloaltonetworks.com/content/pan/en_US/rss/advisories.xml",
    "https://my.f5.com/manage/s/feed-security-advisories",
    "https://www.crowdstrike.com/blog/feed/",
    "https://www.trendmicro.com/vinfo/us/security/news/rss",
    
    # CVE & Vulnerability Feeds
    "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml",
    "https://cvefeed.io/rssfeed/latest.xml",
    "https://www.securityweek.com/vulnerability-management/feed",
    
    # General Intelligence
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://www.darkreading.com/rss.xml"
]

# Takip edilecek özel anahtar kelimeler
WATCH_KEYWORDS = [
    'f5', 'palo alto', 'splunk', 'crowdstrike', 'trend micro', 
    'bluecoat', 'windows server', 'guardicore', 'twistlock', 'nac',
    'cve-202', 'zero-day', 'rce', 'bypass'
]
