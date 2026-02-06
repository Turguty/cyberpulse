FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --upgrade google-genai python-dotenv flask feedparser requests
COPY . .
RUN mkdir -p /app/app/data && chmod -R 777 /app/app/data
CMD ["python", "app/main.py"]
