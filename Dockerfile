FROM python:3.10-slim

WORKDIR /app

# Sistem bağımlılıklarını kur
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıkları kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm dosyaları kopyala
COPY . .

# Python path'ini ayarla (Klasör hatalarını çözer)
ENV PYTHONPATH=/app/app

# Çalıştırma komutu main.py üzerinden (Docker-compose ile ezilebilir)
CMD ["python", "app/main.py"]
