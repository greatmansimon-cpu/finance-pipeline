import yfinance as yf
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

def update_ticker(ticker_symbol, table_name):
    stock = yf.Ticker(ticker_symbol)
    new_fetch = stock.history(period="5d").reset_index()
    new_fetch["Date"] = new_fetch["Date"].dt.tz_localize(None)

    try:
        existing = pd.read_sql(f"SELECT DISTINCT Date FROM {table_name}", engine)
        existing_dates = existing["Date"].tolist()
    except:
        existing_dates = []

    new_data = new_fetch[~new_fetch["Date"].isin(existing_dates)]

    if len(new_data) > 0:
        new_data.to_sql(table_name, engine, if_exists="append", index=False)
        print(f"{ticker_symbol}: added {len(new_data)} new rows")
    else:
        print(f"{ticker_symbol}: no new data to add")

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

for ticker in tickers:
    table_name = f"{ticker}_prices"
    update_ticker(ticker, table_name)

## notebooks are built for one to interact with (by clicking a cell), they are not designed to be triggered automatically
## .py scripts on the other side can do that, reasons why all the codes were brought down here so when can schedule our dataset updating