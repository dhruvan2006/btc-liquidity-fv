import streamlit as st
import pandas as pd
import statsmodels.api as sm
import plotly.express as px


st.title("Bitcoin Fair Value")
st.write("Exploring to find a relationship between GLI and bitcoin and establish _fair value_")

# Load data
df = pd.read_csv('btc-gl.csv')
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df.set_index('Date', inplace=True)

# Line chart
fig = px.line(df, x=df.index, y=['BTC', 'GLI'], title='Bitcoin and GLI')
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="BTC",
    yaxis=dict(
        title="BTC",
    ),
    yaxis2=dict(
        title="GLI",
        overlaying="y",
        side="right",
        showgrid=False,
    ),
)
fig.data[0].update(line=dict(color='orange'))
fig.data[1].update(line=dict(color='white'), yaxis="y2")

st.plotly_chart(fig)

# Scatter plot
fig = px.scatter(x=df['GLI'], y=df['BTC'], title='GLI vs BTC')
fig.update_traces(marker=dict(color='white'))
fig.update_xaxes(title_text='GLI')
fig.update_yaxes(title_text='BTC')

st.plotly_chart(fig)
