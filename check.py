import os
import pandas as pd 
import pandas_ta as ta
import plotly.graph_objects as go


dataframes = {}

for filename in os.listdir('Dataset/SmallCap'):
    symbol = filename.split('.')[0]
    #print(symbol)
    
    df = pd.read_csv('Dataset/SmallCap/{}'.format(filename)) 
    if df.empty:
        continue  
    df['20sma'] = df['Close'].rolling(window=20).mean()
    df['stddev'] = df['Close'].rolling(window=20).std()
    df['LowerBand'] = df['20sma'] - (2* df['stddev'])
    df['UpperBand'] = df['20sma'] + (2* df['stddev'])
    df['TR'] = abs(df['High'] - df['Low'])
    
    df['ATR'] = df['TR'].rolling(window=20).mean()

    df['lower_keltner'] = df['20sma'] - (df['ATR'] * 2)
    df['upper_keltner'] = df['20sma'] + (df['ATR'] * 2)
    
    
    def in_squeeze(df):
        return df['LowerBand'] > df['lower_keltner'] and df['UpperBand'] < df['upper_keltner']

    df['squeeze_on'] = df.apply(in_squeeze, axis=1)

    if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
        print("{} is coming out the squeeze".format(symbol))
    
    if symbol == 'KFINTECH':
        itc_df = df


    #dataframes[symbol] = df
#def chart(df): 
     
candlestick = go.Candlestick(x=itc_df['Date'],open=itc_df['Open'],high=itc_df['High'],low=itc_df['Low'],close=itc_df['Close'])
upper_band = go.Scatter(x=itc_df['Date'], y=itc_df['UpperBand'], name='Upper Bollinger Band', line={'color': 'red'})
lower_band = go.Scatter(x=itc_df['Date'], y=itc_df['LowerBand'], name='Lower Bollinger Band', line={'color': 'red'})
upper_keltner = go.Scatter(x=itc_df['Date'], y=itc_df['upper_keltner'], name='Upper Keltner Channel', line={'color': 'blue'})
lower_keltner = go.Scatter(x=itc_df['Date'], y=itc_df['lower_keltner'], name='Lower Keltner Channel', line={'color': 'blue'})
    
fig = go.Figure(data=[candlestick,upper_band,lower_band,upper_keltner,lower_keltner])
fig.layout.xaxis.type = 'category'
fig.layout.xaxis.rangeslider.visible = False
fig.show()    

