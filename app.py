import pytesseract
from PIL import Image
import base64
import io
import requests
from flask import Flask, request, render_template,jsonify
from image_base import getImage
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)  # سيسمح لجميع النطاقات بالوصول



# إنشاء قارئ EasyOCR (تحديد اللغة العربية)
#reader = easyocr.Reader(['ar'])

# قراءة النص من الصورة


# عرض النتائج


# جلب إصدار Tesseract
#tesseract_version = pytesseract#.get_tesseract_version()
#print(f"إصدار Tesseract المثبت: {tesseract_version}")

# جلب مسار tesseract
#tesseract_path = pytesseract.pytesseract.tesseract_cmd
#print(f"مسار Tesseract: {tesseract_path}")
#print(f'********{pytesseract.pytesseract.tesseract_cmd}')
# تحديد المسار إلى ملفات اللغة
#pytesseract.pytesseract.tesseract_cmd = '/usr/share/tesseract'  # إذا كان Tesseract مثبتًا
#os.environ['TESSDATA_PREFIX'] = os.path.join(os.getcwd(), 'tessdata')
# جلب مسار ملفات اللغة
#tessdata_prefix = os.environ.get('TESSDATA_PREFIX')
#print(f"مسار ملفات اللغة (): {tessdata_prefix}")
@app.route('/')
def index():
    return render_template('ready_image.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'لم يتم تحميل أي صورة!'}), 400

    try:
      #  print(f"{data['image']}")
    # تحويل base64 إلى بايتات
        image_data = data['image'].split(',')[1]  # إزالة الجزء الأول من base64
        image_bytes = io.BytesIO(base64.b64decode(image_data))
        print(image_bytes)
        # تحويل base64 إلى صورة
        #image_data = data['image'].split(',')[1]  # إزالة الجزء الأول من base64
        #image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        #result = reader.readtext(image)
        # استخراج النص باستخدام pytesseract
        text =getImage(base64.b64decode(image_data))#,'K87444439688957')# pytesseract.image_to_string(image)
        return text#jsonify({'text': text})
    except Exception as e:
        print(f"*****{e}")
        return jsonify({'error': str(e)}), 500




def ocr_space(image_bytes, api_key,language='ara'):
        url = "https://api.ocr.space/parse/image"
        payload = {
        "apikey": api_key,
        "language": language,
        "isOverlayRequired": False,
        "filetype": "JPG",  # تحديد نوع الملف يدويًا إذا لزم الأمر
        }
        files = {"file": image_bytes}
        response = requests.post(
              url,
              files=files,
              data=payload
              )
        print(f"response.json()****{response.json()}")      
        return response.json()
 
 
'''
  with open(image_path, 'rb') as image_file:
                response = requests.post(
                    url,
                    files={image_path: image_file},
                    data={"apikey": api_key}
                )
            return response.json()
'''
        #result = ocr_space('path_to_your_image.png', 'YOUR_OCR_SPACE_API_KEY')
        #print(result)
        #return result

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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)