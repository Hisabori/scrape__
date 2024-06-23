from flask import Flask, jsonify, request
import pytesseract
from PIL import Image
from io import BytesIO
import base64
import os

app = Flask(__name__)

# Tesseract OCR을 사용하여 이미지에서 텍스트 추출
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# 텍스트를 기반으로 캔들패턴 판별 및 가격 정보 계산
def identify_candle_pattern_and_prices(text):
    patterns = {
        "bullish_engulfing": {
            "result": "상승",
            "entry_price": lambda o, c: c,
            "stop_loss": lambda o, c: o,
            "take_profit": lambda o, c: c + (c - o)
        },
        "bearish_engulfing": {
            "result": "하락",
            "entry_price": lambda o, c: c,
            "stop_loss": lambda o, c: o,
            "take_profit": lambda o, c: c - (o - c)
        },
        # 다른 패턴 추가 가능
    }

    for pattern, rules in patterns.items():
        if pattern in text.lower():
            open_price = 100  # 예시 값
            close_price = 110  # 예시 값

            entry_price = rules["entry_price"](open_price, close_price)
            stop_loss = rules["stop_loss"](open_price, close_price)
            take_profit = rules["take_profit"](open_price, close_price)

            return {
                "pattern": pattern,
                "result": rules["result"],
                "entry_price": entry_price,
                "stop_loss": stop_loss,
                "take_profit": take_profit
            }
    return None

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    image_base64 = data['image_url'].split(",")[1]
    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data))

    # 이미지에서 텍스트 추출 및 캔들패턴 분석
    extracted_text = extract_text_from_image(image)
    pattern_info = identify_candle_pattern_and_prices(extracted_text)

    return jsonify(pattern_info)

if __name__ == '__main__':
    app.run(debug=True)
