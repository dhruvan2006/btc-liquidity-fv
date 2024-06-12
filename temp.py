import pandas as pd
import yfinance as yf

df = pd.read_csv('gl.csv', parse_dates=['Date'])

btc_data = yf.download('BTC-USD', start=df['Date'].min(), end=df['Date'].max())

df['Date'] = pd.to_datetime(df['Date'])
btc_data = btc_data[['Close']].reset_index()
btc_data['Date'] = pd.to_datetime(btc_data['Date'])

merged_df = pd.merge(df, btc_data, how='left', on='Date')
merged_df['Close'] = merged_df['Close'].apply(lambda x: round(x, 2))
print(merged_df)

merged_df.to_csv('btc-gli.csv', index=False)
