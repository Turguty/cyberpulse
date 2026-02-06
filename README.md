# 🛡️ CyberPulse - Siber Güvenlik Haber Botu & Dashboard

Bu proje, çeşitli siber güvenlik kaynaklarından RSS üzerinden haberleri çeken, 
kritiklik seviyesini analiz eden ve sonuçları hem bir Telegram botu üzerinden 
gönderen hem de yerel bir web dashboard'unda görselleştiren bir araçtır.

## 🚀 Özellikler
- **Haber Takibi:** 5+ farklı siber güvenlik kaynağından anlık veri çekme.
- **Kritiklik Analizi:** Anahtar kelime bazlı risk seviyesi belirleme.
- **Telegram Entegrasyonu:** Anlık bildirimler ve Türkçe çeviri linkleri.
- **Dashboard:** Flask ve Chart.js ile veri görselleştirme.
- **Containerize:** Docker Compose ile tek komutla kurulum.

## 🛠️ Kurulum
1. `.env` dosyasını oluşturun ve `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` bilgilerini girin.
2. `docker-compose up --build` komutunu çalıştırın.
3. Dashboard'a `http://localhost:5000` adresinden erişin.
