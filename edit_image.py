from PIL import Image
import os
import requests

# تقليل حجم الصورة
def compress_image(image_path, output_path, quality=85):
    with Image.open(image_path) as img:
        img.save(output_path, "JPEG", quality=quality)

# التحقق من حجم الملف
def check_file_size(file_path):
    size_kb = os.path.getsize(file_path) / 1024
    return size_kb

# استخدام OCR.space
def ocr_space(image_path, api_key, language='ara'):
    url = "https://api.ocr.space/parse/image"
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            url,
            files={"file": image_file},
            data={"apikey": api_key, "language": language}
        )
    return response.json()

# الخطوات الرئيسية
if __name__ == "__main__":
    # تقليل حجم الصورة
    compress_image('1000423999.jpg', 'compressed_image.jpg', quality=85)

    # التحقق من حجم الملف
    size = check_file_size('compressed_image.jpg')
    print(f"حجم الملف المضغوط: {size:.2f} KB")

    # استخدام OCR.space
    api_key = 'YOUR_OCR_SPACE_API_KEY'  # استبدل هذا بمفتاح API الخاص بك
    result = ocr_space('compressed_image.jpg', api_key)

    # طباعة النتيجة
    print(result)