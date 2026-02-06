#!/bin/bash

# Renk tanımlamaları (Görsel geri bildirim için)
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # Renk Yok

echo -e "${BLUE}[1/4] GitHub'a Pushlanıyor...${NC}"

# Git işlemlerini sırasıyla yap
git add .
git commit -m "Auto-Update: $(date +'%Y-%m-%d %H:%M:%S')"

# Not: Eğer remote ayarın yapılmadıysa burası hata verebilir.
if git push origin main; then
    echo -e "${GREEN}>> GitHub başarıyla güncellendi.${NC}"
else
    echo -e "${RED}>> GitHub push başarısız! (Yine de Docker işlemleri devam ediyor...)${NC}"
fi

echo -e "${BLUE}[2/4] Mevcut Containerlar Durduruluyor...${NC}"
# Mevcut containerları durdur ve sil
docker-compose down

echo -e "${BLUE}[3/4] İmajlar Yeniden Build Ediliyor...${NC}"
# Cache kullanmadan tertemiz bir build al
docker-compose build --no-cache

echo -e "${BLUE}[4/4] Sistem Başlatılıyor...${NC}"
# Arka planda çalıştır
docker-compose up -d

echo -e "-----------------------------------------------"
echo -e "${GREEN}TEBRİKLER! Sistem güncellendi ve yayına alındı.${NC}"
echo -e "Dashboard: http://localhost:5000"
echo -e "-----------------------------------------------"

# Çalışan containerları göster
#docker ps
