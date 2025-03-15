import pytesseract
from PIL import Image
import base64
import io
from flask import Flask, request, render_template,jsonify

import os
app = Flask(__name__)



# جلب مسار ملفات اللغة
tessdata_prefix = os.environ.get('TESSDATA_PREFIX')
print(f"مسار ملفات اللغة (tessdata): {tessdata_prefix}")
# جلب إصدار Tesseract
tesseract_version = pytesseract#.get_tesseract_version()
print(f"إصدار Tesseract المثبت: {tesseract_version}")

# جلب مسار tesseract
#tesseract_path = pytesseract.pytesseract.tesseract_cmd
#print(f"مسار Tesseract: {tesseract_path}")
#print(f'********{pytesseract.pytesseract.tesseract_cmd}')
# تحديد المسار إلى ملفات اللغة
pytesseract.pytesseract.tesseract_cmd = r'/usr/share/tessdata'#bin/tesseract'  # إذا كان Tesseract مثبتًا
os.environ['TESSDATA_PREFIX'] = os.path.join(os.getcwd(), 'tessdata')

@app.route('/')
def index():
    return render_template('ready_image.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'لم يتم تحميل أي صورة!'}), 400

    try:
        # تحويل base64 إلى صورة
        image_data = data['image'].split(',')[1]  # إزالة الجزء الأول من base64
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

        # استخراج النص باستخدام pytesseract
        text = pytesseract.image_to_string(image, lang='ara')
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)