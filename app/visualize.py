import plotly.graph_objects as go

def visualize_patterns(df):
    fig = go.Figure()

    
    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Candlestick"
    ))

    
    hammer_df = df[df['Hammer']]
    fig.add_trace(go.Scatter(
        x=hammer_df['Date'],
        y=hammer_df['Low'], 
        mode='markers',
        name='Hammer',
        marker=dict(color='blue', size=10, symbol='triangle-up')
    ))

   
    doji_df = df[df['Doji']]
    fig.add_trace(go.Scatter(
        x=doji_df['Date'],
        y=doji_df['Close'],  
        mode='markers',
        name='Doji',
        marker=dict(color='orange', size=10, symbol='circle')
    ))

    
    engulfing_df = df[df['Engulfing']]
    fig.add_trace(go.Scatter(
        x=engulfing_df['Date'],
        y=engulfing_df['High'],  
        mode='markers',
        name='Engulfing',
        marker=dict(color='green', size=10, symbol='square')
    ))

    
    fig.update_layout(
        title="Interactive Candlestick Chart with Patterns",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        height=600,
    )

    
    return fig
