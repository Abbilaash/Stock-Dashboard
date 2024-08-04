import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def predict(data):
    # Convert list to DataFrame
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)

    predictions = []
    for feature in ['Open', 'High', 'Low', 'Close', 'Volume']:
        X = np.arange(len(df)).reshape(-1, 1)
        y = df[feature].values

        model = LinearRegression()
        model.fit(X, y)

        future_X = np.arange(len(df), len(df) + 7).reshape(-1, 1)
        future_y = model.predict(future_X)

        predictions.append(future_y)

    dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=7).strftime('%Y-%m-%d')
    predicted_data = pd.DataFrame({
        'Date': dates,
        'Open': predictions[0],
        'High': predictions[1],
        'Low': predictions[2],
        'Close': predictions[3],
        'Volume': predictions[4]
    })

    return predicted_data.round(6)

