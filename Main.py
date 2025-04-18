import pandas as pd
from app.Fetch_data import fetch_data, preprocess_data
from app.Patterns import is_hammer, is_doji, is_engulfing
from app.Visualize import visualize_patterns

# Function to fetch data from fetch_data function for given date.
df = fetch_data("AAPL", "2023-01-01", "2023-01-31")
df = preprocess_data(df)

# Apply is_hammer,is_doji,is_engulfing function on all the rows of data.
df['Hammer'] = df.apply(is_hammer, axis=1)
df['Doji'] = df.apply(is_doji, axis=1)
df['Engulfing'] = df.apply(
    lambda row: is_engulfing(row, df.iloc[df.index.get_loc(row.name) - 1]) if row.name > 0 else False,
    axis=1
)


print(df[['Date', 'Hammer', 'Doji', 'Engulfing']].head())
visualize_patterns(df)