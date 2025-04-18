# Function to check candle is hammer or not
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
    
# Function to check candle is doji or not
def is_doji(row):
    try:
        return abs(row['Close'] - row['Open']) / (row['High'] - row['Low']) < 0.1
    except ZeroDivisionError:
        return False
    
#Function to check candle is engulfing or not
def is_engulfing(curr_row, prev_row):
    try:
        return (
            (curr_row['Open'] < prev_row['Close'] and curr_row['Close'] > prev_row['Open'])
            or (curr_row['Open'] > prev_row['Close'] and curr_row['Close'] < prev_row['Open'])
        )
    except Exception:
        return False
