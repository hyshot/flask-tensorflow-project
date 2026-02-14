FROM python:3.9-slim

WORKDIR /app

# Gerekli sistem paketlerini yükle (OpenCV vb. gerekirse buraya eklenebilir)
RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Geçici dosya yüklemeleri için static klasörüne yazma izni ver
RUN mkdir -p static && chmod 777 static

# Hugging Face Spaces 7860 portunu kullanır
EXPOSE 7860

# Uygulamayı başlat
CMD ["gunicorn", "run:app", "-b", "0.0.0.0:7860"]
