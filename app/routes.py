import requests
import pandas as pd
import datetime
import io
import plotly.graph_objects as go
import plotly.io as pio
from flask import Flask, render_template, request, redirect, url_for, send_file
from app import app
import app.func as func

def fetch_stock_data(symbol, start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp())}&period2={int(datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp())}&interval=1d&events=history'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = io.StringIO(response.text)
        df = pd.read_csv(data)
        return df
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def plot_candlestick_chart(df, symbol):
    if df is not None:
        df['Date'] = pd.to_datetime(df['Date'])
        fig = go.Figure(data=[go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close']
        )])
        fig.update_layout(
            title='Stock Price Over Time',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(
                family="Arial, sans-serif",
                size=14,
                color="#000000"
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgray',
                tickangle=-45,
                rangeslider=dict(visible=True),
                type="date"
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgray'
            ),
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255,255,255,0.5)',
                bordercolor='black',
                borderwidth=1
            ),
            autosize=True,
            height=None,
        )
        return fig.to_html(full_html=False, config={'responsive': True})
    else:
        return "<div>No data available</div>"


@app.route('/')
def home():
    return redirect(url_for('table_view'))


@app.route('/table', methods=['GET', 'POST'])
def table_view():
    if request.method == 'POST':
        symbol = request.form.get('symbol', 'AAPL')
        period = request.form.get('period', '10')
    else:
        symbol = 'AAPL'
        period = '10'
    global last_days
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    if period == '10':
        start_date = (datetime.datetime.today() - datetime.timedelta(days=10)).strftime('%Y-%m-%d')
    elif period == '15':
        start_date = (datetime.datetime.today() - datetime.timedelta(days=15)).strftime('%Y-%m-%d')
    elif period == '20':
        start_date = (datetime.datetime.today() - datetime.timedelta(days=20)).strftime('%Y-%m-%d')
    elif period == '60':
        start_date = (datetime.datetime.today() - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
    elif period == '180':
        start_date = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
    elif period == '365':
        start_date = (datetime.datetime.today() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
    elif period == '730':
        start_date = (datetime.datetime.today() - datetime.timedelta(days=730)).strftime('%Y-%m-%d')
    else:
        start_date = (datetime.datetime.today() - datetime.timedelta(days=10)).strftime('%Y-%m-%d')
    df = fetch_stock_data(symbol, start_date, end_date)
    if df is not None:
        last_days = df.tail(int(period)).to_dict('records')[::-1]
    else:
        last_days = []
    
    df = fetch_stock_data(symbol, (datetime.datetime.today() - datetime.timedelta(days=1500)).strftime('%Y-%m-%d'), end_date)
    predicted_data = func.predict(df)

    # Combining the past datas with predicted datas
    combined_df = pd.concat([pd.DataFrame(last_days), predicted_data], ignore_index=True)

    # Generate candlestick graph with color differentiation
    last_days = pd.DataFrame(last_days)
    last_days['Date'] = pd.to_datetime(last_days['Date'])
    candlestick_past = go.Candlestick(
        x=last_days['Date'],
        open=last_days['Open'],
        high=last_days['High'],
        low=last_days['Low'],
        close=last_days['Close'],
        increasing_line_color='green', decreasing_line_color='red',
        name='Past Data'
    )
    
    candlestick_predicted = go.Candlestick(
        x=predicted_data['Date'],
        open=predicted_data['Open'],
        high=predicted_data['High'],
        low=predicted_data['Low'],
        close=predicted_data['Close'],
        increasing_line_color='blue', decreasing_line_color='orange',
        name='Predicted Data'
    )

    fig = go.Figure(data=[candlestick_past, candlestick_predicted])
    fig.update_layout(title='Stock Price Data', yaxis_title='Stock Price (USD)')
    graph_html = pio.to_html(fig, full_html=False)

    predicted_data = predicted_data.to_dict('records')
    last_days['Date'] = last_days['Date'].dt.strftime('%Y-%m-%d')
    last_days = last_days.to_dict('records')
    return render_template('table.html', last_10_days=last_days, symbol=symbol,
                           period=period, predicted_data=predicted_data,graph_html=graph_html)

@app.route('/download_csv', methods=['POST'])
def download_csv():
    df = pd.DataFrame(last_days)
    csv = df.to_csv(index=False)
    return send_file(io.BytesIO(csv.encode()), mimetype='text/csv', as_attachment=True, download_name='data.csv')


@app.route('/graph', methods=['GET', 'POST'])
def graph_view():
    if request.method == 'POST':
        symbol = request.form.get('symbol', 'AAPL')
        period = request.form.get('period', '1M')
    else:
        symbol = 'AAPL'
        period = '1M'
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    if period == '1M':
        start_date = (datetime.datetime.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    elif period == '6M':
        start_date = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
    elif period == '1Y':
        start_date = (datetime.datetime.today() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
    else:
        start_date = (datetime.datetime.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    df = fetch_stock_data(symbol, start_date, end_date)
    graph_html = plot_candlestick_chart(df, symbol)
    return render_template('graph.html', symbol=symbol, period=period, graph_html=graph_html)

