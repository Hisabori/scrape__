import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 데이터_수집
def get_btc_data():
    btc = yf.download('BTC-USD', start='2020-01-01', end='2023-01-01')
    btc = btc[['Close']]  # 종가만 사용
    return btc

# 데이터 전처리
def preprocess_data(data):
    data['Prediction'] = data['Close'].shift(-30)  # 30일 뒤 예측
    X = data.drop(['Prediction'], axis=1)[:-30]
    y = data['Prediction'][:-30]
    return X, y

# 모델 학습
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model, X_test, y_test

# 예측 수행 및 평가
def predict_and_evaluate(model, X_test, y_test):
    predictions = model.predict(X_test)
    plt.figure(figsize=(14,7))
    plt.plot(y_test.index, y_test, label='Actual Price')
    plt.plot(y_test.index, predictions, label='Predicted Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    btc_data = get_btc_data()
    X, y = preprocess_data(btc_data)
    model, X_test, y_test = train_model(X, y)
    predict_and_evaluate(model, X_test, y_test)
