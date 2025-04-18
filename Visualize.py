import plotly.graph_objects as go

def visualize_patterns(df):
    """
    Creates an interactive candlestick chart using Plotly and highlights patterns.
    
    Parameters:
        df (DataFrame): The data containing Open, High, Low, Close, and patterns.
    """
    fig = go.Figure()

    # Add Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Candlestick"
    ))

    # Highlight Hammer pattern
    hammer_df = df[df['Hammer']]
    fig.add_trace(go.Scatter(
        x=hammer_df['Date'],
        y=hammer_df['Low'],  # Highlight at the lowest price of the day
        mode='markers',
        name='Hammer',
        marker=dict(color='blue', size=10, symbol='triangle-up')
    ))

    # Highlight Doji pattern
    doji_df = df[df['Doji']]
    fig.add_trace(go.Scatter(
        x=doji_df['Date'],
        y=doji_df['Close'],  # Highlight at the closing price of the day
        mode='markers',
        name='Doji',
        marker=dict(color='orange', size=10, symbol='circle')
    ))

    # Highlight Engulfing pattern
    engulfing_df = df[df['Engulfing']]
    fig.add_trace(go.Scatter(
        x=engulfing_df['Date'],
        y=engulfing_df['High'],  # Highlight at the highest price of the day
        mode='markers',
        name='Engulfing',
        marker=dict(color='green', size=10, symbol='square')
    ))

    # Update layout for better visualization
    fig.update_layout(
        title="Interactive Candlestick Chart with Patterns",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        height=600,
    )

    # Show the figure
    fig.show()
