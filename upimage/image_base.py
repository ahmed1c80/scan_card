import requests
from PIL import Image
import io
import base64

def compress_image_bytes(image_bytes, quality=85):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        output_buffer = io.BytesIO()
        image.save(output_buffer, format='JPEG', quality=quality)
        return output_buffer.getvalue()
    except Exception as e:
        print(f"Error compressing image: {e}")
        return None

def ocr_space(compressed_bytes, api_key, language='ara'):
    url = "https://api.ocr.space/parse/image"
    try:
        response = requests.post(
            url,
            files={"file": ("compressed.jpg", compressed_bytes)},
            data={"apikey": api_key, "language": language}
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def check_ocr_result(result):
    if result.get("IsErroredOnProcessing", True):
        error_message = result.get("ErrorMessage", ["Unknown error"])[0]
        return (False, error_message)
    else:
        parsed_text = result.get("ParsedResults", [{}])[0].get("ParsedText", "")
        return (True, parsed_text)
# مثال لاستخدام الكود
def getImage(original_bytes):
    # قراءة الصورة الأصلية كبايتات (مثال)
    #with open("1000423999.jpg", "rb") as f:
        #original_bytes = f.read()

    # ضغط الصورة
    compressed_bytes = compress_image_bytes(original_bytes, quality=70)

    if compressed_bytes:
        # استخدام OCR.space
        api_key = 'K87444439688957'
        result = ocr_space(compressed_bytes, api_key)
        print(result)
        return result
    else:
        print("Failed to compress image.")