from datetime import datetime
from flask import Flask,request,render_template
from app.fetch_data import fetch_data
from app.preprocess_data import preprocess_data
from app.patterns import is_hammer, is_doji, is_engulfing
from app.visualize import visualize_patterns

app=Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form.get("ticker")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        # Check if the dates are valid
        today = datetime.today().date()
        if datetime.strptime(end_date, "%Y-%m-%d").date() > today:
            return render_template("index.html", error="End date cannot be in the future.")
        
        if datetime.strptime(start_date, "%Y-%m-%d").date() > today:
            return render_template("index.html", error="Start date cannot be in the future.")


        # Fetch and preprocess data
        df = fetch_data(ticker, start_date, end_date)
        df = preprocess_data(df)

        # Detect patterns
        df['Hammer'] = df.apply(is_hammer, axis=1)
        df['Doji'] = df.apply(is_doji, axis=1)
        df['Engulfing'] = df.apply(
            lambda row: is_engulfing(row, df.iloc[df.index.get_loc(row.name) - 1]) if row.name > 0 else False,
            axis=1
        )

        if not df.empty:
            chart = visualize_patterns(df)
            return render_template("index.html", chart=chart.to_html())
        else:
            return render_template("index.html",error="No data available between the given days")

    return render_template("index.html")
