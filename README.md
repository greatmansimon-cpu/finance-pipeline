# Finance Data Pipeline & Dashboard

A live stock market data pipeline that automatically fetches, stores, and visualizes daily price data for 5 major tech stocks — built end-to-end with Python, SQL Server, and Streamlit.

## What it does

- Pulls live daily price data (Open, High, Low, Close, Volume) for AAPL, MSFT, GOOGL, AMZN, and TSLA using the Yahoo Finance API
- Stores it in a SQL Server database, with duplicate-safe logic that only inserts genuinely new data on each run
- Runs automatically every night via Windows Task Scheduler — no manual triggering required
- Visualizes the data in an interactive Streamlit dashboard, including price trends, a 20-day moving average, and trading volume

## Why I built this

I wanted hands-on experience with a full data pipeline — not just fitting a model to a static CSV, but sourcing data from a live API, handling real storage problems (duplicates, data types, scheduling), and presenting results visually. This project touches the core skills used in real data engineering and analytics work: APIs, databases, automation, and dashboarding.

## Tech stack

- **Python** — yfinance, pandas, sqlalchemy
- **SQL Server** — persistent storage
- **Windows Task Scheduler** — daily automation
- **Streamlit + Plotly** — interactive dashboard

## How it works

1. **Fetch** — `yfinance` pulls the latest 5 days of price data per ticker (a small buffer in case a scheduled run is missed)
2. **Check** — before inserting, the pipeline queries which dates are already stored and filters them out
3. **Store** — only new rows are appended to the SQL Server table, preventing duplicates
4. **Automate** — a scheduled task runs the update script daily, keeping the database current without manual input
5. **Visualize** — the Streamlit dashboard reads from the database and renders price charts, a moving average overlay, and volume bars, with a dropdown to switch between tickers

## Challenges solved along the way

- **Timestamp conflict:** SQL Server reserves a `TIMESTAMP` type unrelated to dates; timezone-aware dates from yfinance were misread as this type. Fixed by stripping timezone info before saving.
- **Duplicate inserts:** naive appends re-inserted the same rows on every run. Solved by comparing incoming data against existing stored dates before inserting.
- **Task Scheduler path issue:** Windows Task Scheduler couldn't resolve `python` as a command; fixed by pointing it to the full Python executable path.

## Project files

- `update_prices.py` — the daily update script (run by Task Scheduler)
- `dashboard.py` — the Streamlit dashboard
- `exploration_notes.ipynb` — development notebook showing the full build process, including debugging

## What's next

This is Project 1 of a 5-project roadmap. Project 4 will extend this pipeline to run in the cloud (AWS), and Project 5 will add a deployed, monitored prediction model built on top of this stored data.
