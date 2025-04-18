import pandas as pd
import yfinance as yf

def fetch_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
    data.reset_index(inplace=True)
    return data

# Fetch the data
df = fetch_data("AAPL", "2023-01-01", "2023-12-31")
print(df.head())


# Fix column names if they are incorrectly prefixed
if len(df.columns) == 7:  # Expecting ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    df.columns = ['Date', 'Adj Close','Close','High', 'Low', 'Open', 'Volume']
elif len(df.columns) == 6:  # Sometimes 'Adj Close' is not present
    df.columns = ['Date','Close', 'High', 'Low','Open','Volume']
else:
    raise KeyError(f"Unexpected DataFrame structure: {df.columns}")

#print(df.head())

# Check for missing columns
missing_columns = [col for col in ['Open', 'Close', 'Low', 'High'] if col not in df.columns]
if missing_columns:
    raise KeyError(f"Missing columns in DataFrame: {missing_columns}")

# Convert to numeric and clean data
df[['Open', 'Close', 'Low', 'High']] = df[['Open', 'Close', 'Low', 'High']].apply(pd.to_numeric, errors="coerce")
df.dropna(subset=['Open', 'Close', 'Low', 'High'], inplace=True)

# Add pattern columns
def is_hammer(row):
    try:
        body = abs(row['Open'] - row['Close'])
        if row['Close'] > row['Open']:
            lower_wick = row['Open'] - row['Low']
            upper_wick = row['High'] - row['Close']
        else:
            lower_wick = row['Close'] - row['Low']
            upper_wick = row['High'] - row['Open']
        return lower_wick > 2 * body and body > upper_wick
    except Exception:
        return False

def is_doji(row):
    try:
        return abs(row['Close'] - row['Open']) / (row['High'] - row['Low']) < 0.1
    except ZeroDivisionError:
        return False

def is_engulfing(curr_row, prev_row):
    try:
        return (
            (curr_row['Open'] < prev_row['Close'] and curr_row['Close'] > prev_row['Open'])
            or (curr_row['Open'] > prev_row['Close'] and curr_row['Close'] < prev_row['Open'])
        )
    except Exception:
        return False

df['Hammer'] = df.apply(is_hammer, axis=1)
df['Doji'] = df.apply(is_doji, axis=1)
df['Engulfing'] = df.apply(
    lambda row: is_engulfing(row, df.iloc[df.index.get_loc(row.name) - 1]) if row.name > 0 else False,
    axis=1
)

print(df[['Date', 'Hammer', 'Doji', 'Engulfing']].tail())
