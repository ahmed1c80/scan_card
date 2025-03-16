import pytesseract

from flask import Flask, request, jsonify,render_template
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import requests
from upimage.image_base import getImage
from upimage.improve import process_image_imporve
from flask_cors import CORS
import os
app = Flask(__name__)
  # سيسمح لجميع النطاقات بالوصول

CORS(app, resources={
    r"/analyze": {
        "origins": ["https://dcash.shamil-bkp.com", "http://localhost:*"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] ='*'
    # 'https://dcash.shamil-bkp.com'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS,GET,HEAD'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Max-Age'] = 86400
    return response
#CORS(app, resources={r"/analyze": {"origins": "https://dcash.shamil-bkp.com"}})

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


@app.route('/analyze', methods=['POST', 'OPTIONS','GET'])
def analyze_image():
    print(f"********analyze_image {request}")
    if request.method == 'OPTIONS':
      return jsonify({"message": "CORS allowed"}), 200
    if request.method == 'HEAD':
      return jsonify({"message": "CORS allowed"}), 200
      #res=getanalyze_image()
      #return res
    if request.method == 'GET':
      json_data = request.args.get('data')
      res=getanalyze_image_json(json_data)
      return res
    if request.method == 'POST':
      res=getanalyze_image()
      return res
        #return jsonify({'success': 'run data options'}), 200
    
    return jsonify({'error': 'لم يتم تحميل أي صورة!'}), 400




def getanalyze_image():
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
        print(f"***{data}**{e}")
        return jsonify({'error': str(e)}), 500
 
 
 
def getanalyze_image_json(data):
    #data = request.get_json()
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
        print(f"***{data}**{e}")
        return jsonify({'error': str(e)}), 500
 
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





@app.route('/edit_image')
def edit_image():
    return render_template('edit_image.html')


app.config['UPLOAD_FOLDER'] = 'temp'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/process', methods=['POST'])
def process_image():
  res= process_image_imporve()
  return res
  
  
  
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)