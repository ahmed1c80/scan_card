import pytesseract
from PIL import Image
import base64
import io
from flask import Flask, request, render_template,jsonify

import os
app = Flask(__name__)




# جلب إصدار Tesseract
tesseract_version = pytesseract#.get_tesseract_version()
print(f"إصدار Tesseract المثبت: {tesseract_version}")

# جلب مسار tesseract
#tesseract_path = pytesseract.pytesseract.tesseract_cmd
#print(f"مسار Tesseract: {tesseract_path}")
#print(f'********{pytesseract.pytesseract.tesseract_cmd}')
# تحديد المسار إلى ملفات اللغة
#pytesseract.pytesseract.tesseract_cmd = r'/usr/share/tessdata'#bin/tesseract'  # إذا كان Tesseract مثبتًا
os.environ['TESSDATA_PREFIX'] = os.path.join(os.getcwd(), 'tessdata')
# جلب مسار ملفات اللغة
tessdata_prefix = os.environ.get('TESSDATA_PREFIX')
print(f"مسار ملفات اللغة (): {tessdata_prefix}")
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
        print(f"*****{e}")
        return jsonify({'error': str(e)}), 500



# دالة لسرد الملفات في مسار معين
def list_files_in_directory(path):
    try:
        # التحقق من وجود المسار
        if not os.path.exists(path):
            return None, f"المسار '{path}' غير موجود."
        
        # الحصول على قائمة الملفات والمجلدات
        files = os.listdir(path)
        return files, None
    except Exception as e:
        return None, str(e)

# نقطة نهاية API لسرد الملفات
@app.route('/list_files/<path:directory_path>', methods=['GET'])
def list_files(directory_path):
    # استبدال الشرطة المائلة العكسية بشرطة مائلة للأمام (للتأكد من توافق المسار)
    directory_path = directory_path.replace('\\', '/')
    
    # سرد الملفات في المسار
    files, error = list_files_in_directory(directory_path)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"path": directory_path, "files": files})

# صفحة HTML الرئيسية
@app.route('/dir')
def dir():
    return render_template('dir.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)