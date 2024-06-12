import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Bitcoin Fair Value")
st.write("Exploring to find a relationship between GLI and bitcoin and establish _fair value_")

# Display original image
file_path = 'cbc-11-06-2024.png'

col1, col2 = st.columns(2)
with col1:
    st.image(file_path, f'Last updated on {file_path[4:-4]}')

# Load data
df = pd.read_csv('btc-gli.csv')
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df.set_index('Date', inplace=True)

# Line chart
fig = px.line(df, x=df.index, y=['BTC', 'GLI'])#, title='Bitcoin and GLI')
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
    legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
    margin=dict(t=25, b=25)
)
fig.data[0].update(line=dict(color='orange'))
fig.data[1].update(line=dict(color='white'), yaxis="y2")

with col2:
    st.plotly_chart(fig)

# Scatter plot
st.subheader('Scatter plot')

fig = px.scatter(x=df['GLI'], y=df['BTC'], height=650)#, title='GLI vs BTC')
fig.update_traces(marker=dict(color='orange', size=10))
fig.update_xaxes(title_text='GLI')
fig.update_yaxes(title_text='BTC')
fig.update_layout(margin=dict(t=25, b=100))

st.plotly_chart(fig)

# Polynomial Regression
col1, col2 = st.columns(2)
with col1:
    st.subheader('Polynomial Regression')
with col2:
    degree = st.number_input('Enter the degree of the polynomial', min_value=1, max_value=10, value=1, step=1)

poly_features = np.vander(df['GLI'], N=degree+1, increasing=True)

model = sm.OLS(df['BTC'], poly_features)
results = model.fit()

stddev = np.std(results.resid)

fig = px.scatter(x=df['GLI'], y=df['BTC'])
fig.update_traces(marker=dict(color='orange'))
fig.update_xaxes(title_text='GLI')
fig.update_yaxes(title_text='BTC')

x_range = np.linspace(df['GLI'].min(), df['GLI'].max(), 100)
x_poly_range = np.vander(x_range, N=degree+1, increasing=True)
y_range = results.predict(x_poly_range)

fig.add_scatter(x=x_range, y=y_range, mode='lines', name='Regression Line', line=dict(color='white'))
fig.add_scatter(x=x_range, y=y_range + stddev, mode='lines', line=dict(dash='dash', color='red'), name='Upper Band')
fig.add_scatter(x=x_range, y=y_range - stddev, mode='lines', line=dict(dash='dash', color='red'), name='Lower Band')
fig.update_layout(showlegend=False)

fair_value = results.predict(poly_features)
fig2 = px.line(x=df.index, y=df['BTC'])
fig2.update_traces(line_color='orange')
fig2.add_scatter(x=df.index, y=fair_value, mode='lines', line=dict(color='white'))
fig2.add_scatter(x=df.index, y=fair_value + stddev, mode='lines', line=dict(dash='dash', color='red'))
fig2.add_scatter(x=df.index, y=fair_value - stddev, mode='lines', line=dict(dash='dash', color='red'))
fig2.update_layout(
    xaxis_title='Date',
    yaxis_title='Value',
    showlegend=False
)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig)
    st.plotly_chart(fig2)
with col2:
    st.write(results.summary())
