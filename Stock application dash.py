#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[3]:


import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import yfinance as yf
import pandas as pd


# Function definitions remain mostly the same, with adjustments for Dash compatibility
def fetch_stock_data(ticker, period):
    stock_data = yf.download(ticker, period=period)
    
    # Calculate SMA with a 20-day window
    stock_data['SMA'] = ta.trend.sma_indicator(stock_data['Close'], window=20)
    
    # Calculate RSI with a 14-day window
    stock_data['RSI'] = ta.momentum.rsi(stock_data['Close'], window=14)
    
    return stock_data

def calculate_mean_price(stock_data):
    mean_price = stock_data['Close'].mean()
    return mean_price

def generate_signals(stock_data, mean_price, threshold=0.05):
    signals = pd.DataFrame(index=stock_data.index)
    signals['Close'] = stock_data['Close']
    signals['Signal'] = 'Hold'  # Default to 'Hold'
    signals.loc[signals['Close'] < mean_price * (1 - threshold), 'Signal'] = 'Buy'
    signals.loc[signals['Close'] > mean_price * (1 + threshold), 'Signal'] = 'Sell'
    return signals

# Dash app setup
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Stock Analysis Tool"),
    dcc.Input(id='ticker-input', type='text', placeholder='Enter Ticker Symbol'),
    dcc.Dropdown(
        id='period-dropdown',
        options=[
            {'label': '1 Day', 'value': '1d'},
            {'label': '5 Days', 'value': '5d'},
            {'label': '1 Month', 'value': '1mo'},
            {'label': '3 Months', 'value': '3mo'},
            {'label': '6 Months', 'value': '6mo'},
            {'label': '1 Year', 'value': '1y'},
            {'label': '5 Years', 'value': '5y'},
            {'label': 'Max', 'value': 'max'},
            # Add more options as needed
        ],
        value='1mo'  # Default value
    ),
    html.Button('Submit', id='submit-button', n_clicks=0),
    dcc.Graph(id='stock-graph')
])

@app.callback(
    Output('stock-graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('ticker-input', 'value'),
     dash.dependencies.State('period-dropdown', 'value')]
)
def update_graph(n_clicks, ticker, period):
    if n_clicks > 0:
        stock_data = fetch_stock_data(ticker, period)
        mean_price = calculate_mean_price(stock_data)
        signals = generate_signals(stock_data, mean_price)
        
        # Plotly graph
        data = [
            go.Scatter(x=stock_data.index, y=stock_data['Close'], name='Close Price'),
            go.Scatter(x=stock_data.index, y=stock_data['SMA'], name='SMA 20', line=dict(color='orange', width=1.5)),
            go.Scatter(x=signals.index[signals['Signal'] == 'Buy'], y=signals['Close'][signals['Signal'] == 'Buy'], mode='markers', name='Buy', marker=dict(color='green', size=10)),
            go.Scatter(x=signals.index[signals['Signal'] == 'Sell'], y=signals['Close'][signals['Signal'] == 'Sell'], mode='markers', name='Sell', marker=dict(color='red', size=10)),
        ]
        
        layout = go.Layout(
            title='Stock Price, SMA and Trade Signals',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Price'),
            secondary_y=True
        )
        
        # RSI subplot
        data.append(go.Scatter(x=stock_data.index, y=stock_data['RSI'], name='RSI', marker=dict(color='purple')))
        layout.update(
            xaxis=dict(domain=[0, 1]),
            yaxis2=dict(title='RSI', overlaying='y', side='right')
        )
        
        return {'data': data, 'layout': layout}
    return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)


# In[2]:




# In[ ]:




