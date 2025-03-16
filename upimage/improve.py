from flask import Flask, request, jsonify,render_template
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import requests
from arabic_reshaper import reshape
from bidi.algorithm import get_display

def add_arabic_text(image_path, output_path):
    # فتح الصورة
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # تحميل الخط
    font = ImageFont.truetype("Amiri-Regular.ttf", 40)
    
    # النص العربي
    text = "احمد"
    
    # معالجة النص
    reshaped_text = reshape(text)
    bidi_text = get_display(reshaped_text)
    
    # إضافة النص إلى الصورة
    draw.text(
        (50, 50),  # الإحداثيات
        bidi_text,
        fill=(255, 0, 0),  # لون أحمر
        font=font
    )
    
    # حفظ الصورة
    img.save(output_path)

# استخدام الدالة
#add_arabic_text("input.jpg", "output.jpg")


def enhance_image(img):
    # تحسين الجودة الأساسي
    img = img.convert('RGB')
    
    # زيادة الدقة (مثال بسيط)
    new_size = (img.width * 2, img.height * 2)
    img = img.resize(new_size, Image.LANCZOS)
    
    # إضافة نص
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('noto_fonts/NotoSansArabic-Regular.ttf', 40)
    except:
        font = ImageFont.load_default()
    
    text = "نص تجريبي"
        # معالجة النص
    reshaped_text = reshape(text)
    bidi_text = get_display(reshaped_text)
    
    # إضافة النص إلى الصورة
    draw.text(
        (50, 50),  # الإحداثيات
        bidi_text,
        fill=(255, 0, 0),  # لون أحمر
        font=font
    )
    
    #draw.text((20, 20), text, fill=(255, 0, 0), font=font)
    
    return img

def process_image_imporve():
    try:
        # استلام الصورة
        file = request.files['image']
        if not file:
            return jsonify({'error': 'لم يتم إرسال صورة'})
        
        # معالجة الصورة
        img = Image.open(file.stream)
        enhanced_img = enhance_image(img)
        
        # حفظ الصورة المحسنة
        output_buffer = io.BytesIO()
        enhanced_img.save(output_buffer, format='JPEG', quality=90)
        output_buffer.seek(0)
        
        # إرجاع النتيجة
        encoded_image = base64.b64encode(output_buffer.getvalue()).decode()
        return jsonify({
            'image_url': f'data:image/jpeg;base64,{encoded_image}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})