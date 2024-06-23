import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Tesseract OCR을 사용하여 이미지에서 텍스트 추출
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# 텍스트를 기반으로 캔들패턴 판별 및 가격 정보 계산
def identify_candle_pattern_and_prices(text):
    # 패턴 목록 예시 및 가격 계산 규칙
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
            # 예시: 텍스트에서 가격 정보 추출 (실제 구현 시 텍스트 형식에 맞게 조정 필요)
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

# 웹페이지 전체를 스크린샷하는 함수
def take_screenshot_of_website(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(3)  # 페이지 로딩 대기

    # 페이지 높이를 얻어서 전체 스크린샷
    page_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, page_height)
    screenshot_path = 'full_screenshot.png'
    driver.save_screenshot(screenshot_path)
    driver.quit()

    return screenshot_path

# 사용자 입력 처리 및 웹사이트에서 스크린샷
def get_screenshot_from_url():
    url = input("웹사이트 URL을 입력하세요: ")
    return take_screenshot_of_website(url)

# 메인 함수
def main():
    try:
        screenshot_path = get_screenshot_from_url()
        extracted_text = extract_text_from_image(screenshot_path)
        print(f"추출된 텍스트: {extracted_text}")

        pattern_info = identify_candle_pattern_and_prices(extracted_text)
        if pattern_info:
            print(f"캔들패턴: {pattern_info['pattern']}")
            print(f"결과: {pattern_info['result']}")
            print(f"진입 가격: {pattern_info['entry_price']}")
            print(f"손절가: {pattern_info['stop_loss']}")
            print(f"수익 실현가: {pattern_info['take_profit']}")
        else:
            print("패턴을 인식할 수 없습니다.")

        # 다운로드된 스크린샷을 삭제 (선택 사항)
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
