import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

# 주식 가격 데이터를 입력받는 함수
def get_stock_data():
    dates = input("날짜를 입력하세요 (콤마로 구분, 형식: YYYY-MM-DD): ").split(',')
    prices = list(map(float, input("가격을 입력하세요 (콤마로 구분): ").split(',')))
    data = {'Date': dates, 'Close': prices}
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

# 데이터 준비
df = get_stock_data()

# ARIMA 모델 예측
def arima_predict(df, periods):
    arima_model = ARIMA(df['Close'], order=(5, 1, 0))
    arima_model_fit = arima_model.fit()
    forecast = arima_model_fit.forecast(steps=periods)
    return forecast

# Prophet 모델 예측
def prophet_predict(df, periods):
    prophet_df = df.reset_index().rename(columns={'Date': 'ds', 'Close': 'y'})
    prophet_model = Prophet()
    prophet_model.fit(prophet_df)
    future = prophet_model.make_future_dataframe(periods=periods)
    forecast = prophet_model.predict(future)
    return forecast[['ds', 'yhat']].set_index('ds')

# LSTM 모델 예측
def lstm_predict(df, periods):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df)

    look_back = 3  # 3일간의 데이터를 보고 예측
    X, Y = create_dataset(scaled_data, look_back)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    lstm_model = Sequential()
    lstm_model.add(LSTM(50, return_sequences=True, input_shape=(look_back, 1)))
    lstm_model.add(LSTM(50))
    lstm_model.add(Dense(1))
    lstm_model.compile(loss='mean_squared_error', optimizer='adam')
    lstm_model.fit(X, Y, epochs=100, batch_size=1, verbose=2)

    test_data = scaled_data[-look_back:]
    test_data = np.reshape(test_data, (1, look_back, 1))

    forecast = []
    for _ in range(periods):
        pred = lstm_model.predict(test_data)
        forecast.append(pred[0][0])
        test_data = np.append(test_data[:, 1:, :], [[pred]], axis=1)

    forecast = scaler.inverse_transform(np.array(forecast).reshape(-1, 1))
    return pd.Series(forecast.flatten(), index=pd.date_range(start=df.index[-1], periods=periods + 1, closed='right'))

# LSTM 데이터셋 생성 함수
def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

# 예측 수행
periods = 10  # 10일 동안 예측

arima_forecast = arima_predict(df, periods)
prophet_forecast = prophet_predict(df, periods)
lstm_forecast = lstm_predict(df, periods)

# 결과 출력 및 시각화
print("ARIMA 예측:\n", arima_forecast)
print("Prophet 예측:\n", prophet_forecast)
print("LSTM 예측:\n", lstm_forecast)

plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Close'], label='Actual')
plt.plot(arima_forecast.index, arima_forecast, label='ARIMA Forecast')
plt.plot(prophet_forecast.index, prophet_forecast['yhat'], label='Prophet Forecast')
plt.plot(lstm_forecast.index, lstm_forecast, label='LSTM Forecast')
plt.legend()
plt.show()
