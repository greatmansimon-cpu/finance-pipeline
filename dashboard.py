## Building the streamlit visualization
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=finance_pipeline;"
    "Trusted_Connection=yes;"
)

connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(connection_string)

st.title ("Finance Pipeline Dashboard")
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
ticker = st.selectbox("Choose a stock", tickers)
data = pd.read_sql(f"SELECT * FROM {ticker}_prices ORDER BY Date", engine)
## Introducing a moving average overlay on the chart
data["MA20"] = data["Close"].rolling(window=20).mean()

st.write(data)

## Creating a line chart
st.subheader(f"{ticker} Closing Price")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data["Date"], y=data["Close"],mode = "lines", name = "Close Price"))
fig.add_trace(go.Scatter(x=data["Date"], y = data["MA20"], mode = "lines", name = "20-Day MA"))
fig.update_layout(xaxis_title = "Date", yaxis_title = "Price (USD)")

st.plotly_chart(fig)


st.subheader(f"{ticker} Trading Volume")
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=data["Date"], y=data["Volume"], name="Volume"))
fig2.update_layout(xaxis_title="Date", yaxis_title="Shares Traded")

st.plotly_chart(fig2)
