# استخدام صورة أساسية تحتوي على Python
FROM python:3.9-slim

# تثبيت Tesseract-OCR وملفات اللغة
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملفات اللغة إلى المجلد الصحيح
COPY tessdata /usr/share/tessdata

# نسخ ملفات التطبيق
COPY . /app
WORKDIR /app

# تثبيت متطلبات Python
RUN pip install -r requirements.txt

# تشغيل التطبيق
CMD ["gunicorn", "app:app"]