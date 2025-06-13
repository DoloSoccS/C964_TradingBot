#Flask supports 3.9 and newer
#Name file "app.py" to skip --app necessity

from flask import Flask, render_template, request, redirect, url_for, session
from matplotlib.figure import Figure
from io import BytesIO
import base64
from Backend_Content.SecureLogin import test_passphrase
from Database.MongoDB_Connection import start_db
import yfinance as yf
import talib as ta
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import joblib

start_db()
app = Flask(__name__)
app.secret_key = "secret key"


# Needed for session handling features. Should be much more secure than this but suitable for conceptual use.


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def loginPage():
    if request.method == "POST":
        get_passphrase = request.form.get("passphrase")
        if test_passphrase(get_passphrase):
            session["logged_in"] = True
            session.permanent = False
            return redirect(url_for("landingPage"))
        else:
            return "Invalid Passphrase", 403

    return render_template("login.html")


@app.route("/landing", methods=["GET", "POST"])
def landingPage():
    if not session.get("logged_in"):
        return redirect(url_for("loginPage"))

    # These tickers will be available to showcase predictions
    tickersList = [
        "AVB", "AFL", "ALB", "BALL", "BBY", "NET", "CVNA", "ROST", "OMC",
        "QUBT", "BKR", "BR", "BXP", "ORCL", "CAG", "CB", "CDNS", "CE", "CF",
        "CHD", "BTC", "ASIC", "VOYG", "CHYM", "BKIV"
    ]

    # Placeholders for visuals and ticker dropdown

    ticker_selection = request.form.get("tickerFromList")
    data = None
    prediction = None
    predScore = None

    if ticker_selection:
        # Ticker data gathered here to keep requests to yfinance API down. This request is only for the visual chart.
        stock = yf.Ticker(ticker_selection)
        historic_data = stock.history(period="2wk")

        fig = Figure()
        ax_left = fig.subplots()
        ax_left.plot(historic_data.index.strftime('%d-%b'), historic_data["Close"], color='blue', label="Weekly Close")
        ax_right = ax_left.twinx()
        ax_right.plot(historic_data.index.strftime('%d-%b'), historic_data["Volume"], color='red',
                      label="Weekly Volume", linestyle="dashed")
        ax_left.set_title(f"Trend Chart for {stock.ticker}")
        ax_left.set_xlabel("Date")
        ax_left.set_ylabel("Price", color='blue')
        ax_right.set_ylabel("Volume", color="red")

        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        # Download last 3 months of data
        prediction_data = yf.download(ticker_selection, period="3mo", interval="1d", progress=False, auto_adjust=False)
        prediction_data.reset_index(inplace=True)

        # Convert to numpy arrays (1D flattened)

        npArrayClose = prediction_data['Close'].to_numpy().astype(float).flatten()
        npArrayHigh = prediction_data['High'].to_numpy().astype(float).flatten()
        npArrayLow = prediction_data['Low'].to_numpy().astype(float).flatten()
        npArrayOpen = prediction_data['Open'].to_numpy().astype(float).flatten()
        npArrayVolume = prediction_data['Volume'].to_numpy().astype(float).flatten()

        print("npArrayClose shape:", npArrayClose.shape)
        print("npArrayClose ndim :", npArrayClose.ndim)

        # Download latest news and calculate sentiment
        nltk.download('vader_lexicon')
        sia = SentimentIntensityAnalyzer()
        stock = yf.Ticker(ticker_selection)
        news_item = stock.get_news(count=1)
        news_article = news_item[0]["content"]["summary"]
        sentiment = sia.polarity_scores(news_article)
        score = sentiment["compound"]

        # Calculate TA-Lib indicators
        SMA_values = ta.SMA(npArrayClose, timeperiod=30)
        EMA_values = ta.EMA(npArrayClose, timeperiod=30)
        RSI_values = ta.RSI(npArrayClose, timeperiod=30)
        MACD_values, MACD_signal, _ = ta.MACD(npArrayClose, fastperiod=10, slowperiod=28, signalperiod=7)
        WILLR_values = ta.WILLR(npArrayHigh, npArrayLow, npArrayClose, timeperiod=14)
        CCI_values = ta.CCI(npArrayHigh, npArrayLow, npArrayClose, timeperiod=14)
        ATR_values = ta.ATR(npArrayHigh, npArrayLow, npArrayClose, timeperiod=14)

        model = joblib.load("Backend_Content/C964_model.joblib")
        predict = [
            npArrayOpen[-1],  # Latest 'Open'
            npArrayHigh[-1],  # Latest 'High'
            npArrayLow[-1],  # Latest 'Low'
            npArrayVolume[-1],  # Latest 'Volume'
            score,  # Latest sentiment score
            SMA_values[-1],  # Latest SMA
            EMA_values[-1],  # Latest EMA
            RSI_values[-1],  # Latest RSI
            MACD_values[-1],  # Latest MACD
            WILLR_values[-1],  # Latest Williams %R
            CCI_values[-1],  # Latest CCI
            ATR_values[-1]  # Latest ATR
        ]
        evaluate = model.predict_proba([predict])
        predScore = evaluate[0][1]
        if evaluate[0][1] > 0.75:
            prediction = "BUY"
        else:
            prediction = "SELL"

    return render_template("landing.html", tickersList=tickersList, ticker_selection=ticker_selection, data=data,
                           prediction=prediction, predScore=predScore)


if __name__ == '__main__':
    app.run(debug=True)
