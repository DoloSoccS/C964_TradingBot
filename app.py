#Flask supports python 3.9 and newer
#Name file "app.py" to skip --app necessity when running

from flask import Flask, render_template, request, redirect, url_for, session
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
from io import BytesIO
import base64
from Backend_Content.SecureLogin import test_passphrase
import yfinance as yf
import talib as ta
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import joblib

from Database.MongoDB_Connection import start_db

# Instantiating Flask instance. __name__ for referencing "main" function
app = Flask(__name__)

# Key used for session handling when entering passphrase to use application
app.secret_key = "secret key"


# URLs for accessing the login page. Conceptual representation on how to get multiple URLs to access the same page.
@app.route("/", methods=["GET", "POST"])
# @app.route("/login", methods=["GET", "POST"])
def loginPage():
    if request.method == "POST":
        get_passphrase = request.form.get(
            "passphrase")  # Visitor will enter passphrase into the text box and that will be saved in this variable
        if test_passphrase(get_passphrase):
            session["logged_in"] = True  # Used to prove access is being provided to authorized user.
            session.permanent = False  # False value to ensure session does not persist browser exit. Once the browser is closed, login will be necessary again.
            return redirect(url_for("landingPage"))  # After successful login, main application page will be loaded
        else:
            return "Invalid Passphrase", 403

    return render_template("login.html")


# URL for accessing the main page of the application
@app.route("/landing", methods=["GET", "POST"])
def landingPage():
    if not session.get("logged_in"):  # Verify session is authorized to access
        return redirect(url_for("loginPage"))

    # These tickers will be available to showcase predictions in a dropdown menu.
    tickersList = [
        "AVB", "AFL", "ALB", "BALL", "BBY", "NET", "CVNA", "ROST", "OMC",
        "QUBT", "BKR", "BR", "BXP", "ORCL", "CAG", "CB", "CDNS", "CE", "CF",
        "CHD", "BTC", "ASIC", "VOYG", "CHYM", "BKIV"
    ]

    # Placeholders for visuals and ticker dropdown selection
    ticker_selection = request.form.get("tickerFromList")
    data1 = None
    data2 = None
    prediction = None
    predScore = None

    if ticker_selection:
        # Ticker data from previous 2 weeks gathered here to keep requests to yfinance API down. This call is only
        # used for the visual chart.
        stock = yf.Ticker(ticker_selection)
        historic_data = stock.history(period="2wk")

        # Plotting values, creating labels, defining trend lines for "Close" and "Volume."
        fig = Figure()
        ax_left = fig.subplots()
        ax_left.plot(historic_data.index.strftime('%d-%b'), historic_data["Close"], color='blue', label="Weekly Close")
        ax_right = ax_left.twinx()
        ax_right.plot(historic_data.index.strftime('%d-%b'), historic_data["Volume"], color='red', label="Weekly Volume", linestyle="dashed")
        ax_left.set_title(f"{stock.ticker} Price/Volume Line Trend")
        ax_left.set_xlabel("Date")
        ax_left.set_ylabel("Price", color='blue')
        ax_right.set_ylabel("Volume", color="red")

        # Saving figure to memory buffer
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data1 = base64.b64encode(buf.getbuffer()).decode("ascii")

        # Creating Candlestick Chart using
        stock_prices = yf.download(ticker_selection, period="3mo", auto_adjust=False)

        stock_prices.columns = stock_prices.columns.droplevel('Ticker')
        print(stock_prices.columns)
        print(isinstance(stock_prices.columns, pd.MultiIndex))

        plt.figure()
        up = stock_prices[stock_prices["Close"] >= stock_prices["Open"]]
        down = stock_prices[stock_prices["Close"] < stock_prices["Open"]]

        col_decrease = "red"
        col_increase = "green"

        width = 0.5
        width2 = 0.1

        plt.bar(up.index, up.Close - up.Open, width, bottom=up.Open, color=col_decrease)
        plt.bar(up.index, up.High - up.Close, width2, bottom=up.Close, color=col_decrease)
        plt.bar(up.index, up.Low - up.Open, width2, bottom=up.Open, color=col_decrease)

        plt.bar(down.index, down.Close - down.Open, width, bottom=down.Open, color=col_increase)
        plt.bar(down.index, down.High - down.Open, width2, bottom=down.Open, color=col_increase)
        plt.bar(down.index, down.Low - down.Close, width2, bottom=down.Close, color=col_increase)

        plt.xticks(rotation=15, ha='right')
        plt.title(f"{stock.ticker} Candlestick Chart")

        buf2 = BytesIO()
        plt.savefig(buf2, format="png")
        data2 = base64.b64encode(buf2.getbuffer()).decode("ascii")

        # Download last 3 months of data. 3 months to ensure enough data is available for all technical indicators
        # can be calculated
        prediction_data = yf.download(ticker_selection, period="3mo", interval="1d", progress=False, auto_adjust=False)
        prediction_data.reset_index(inplace=True)

        # Creating NumPy ndarray for each data point needed for calculation. Flatten to 1-dimensional as required by
        # TA-Lib
        npArrayClose = prediction_data['Close'].to_numpy().astype(float).flatten()
        npArrayHigh = prediction_data['High'].to_numpy().astype(float).flatten()
        npArrayLow = prediction_data['Low'].to_numpy().astype(float).flatten()
        npArrayOpen = prediction_data['Open'].to_numpy().astype(float).flatten()
        npArrayVolume = prediction_data['Volume'].to_numpy().astype(float).flatten()

        print("npArrayClose shape:", npArrayClose.shape)
        print("npArrayClose ndim :", npArrayClose.ndim)

        # Calculating TA-Lib indicators
        SMA_values = ta.SMA(npArrayClose, timeperiod=30)
        EMA_values = ta.EMA(npArrayClose, timeperiod=30)
        RSI_values = ta.RSI(npArrayClose, timeperiod=30)
        MACD_values, MACD_signal, _ = ta.MACD(npArrayClose, fastperiod=10, slowperiod=28, signalperiod=7)
        WILLR_values = ta.WILLR(npArrayHigh, npArrayLow, npArrayClose, timeperiod=14)
        CCI_values = ta.CCI(npArrayHigh, npArrayLow, npArrayClose, timeperiod=14)
        ATR_values = ta.ATR(npArrayHigh, npArrayLow, npArrayClose, timeperiod=14)

        # Download latest news and calculate sentiment analysis score
        try:
            nltk.download('vader_lexicon')
            sia = SentimentIntensityAnalyzer()
            stock = yf.Ticker(ticker_selection)
            news_item = stock.get_news()
            news_article = news_item[0]["content"]["summary"]
            sentiment = sia.polarity_scores(news_article)
            score = sentiment["compound"]
        except:
            score = 0  # Default to neutral in case there are errors finding news articles for specific ticker symbols.

        # Deploying model on selected ticker symbol. -1 index used to get the latest value given for each metric.
        model = joblib.load("Backend_Content/C964_model.joblib")
        predict = [
            npArrayOpen[-1],
            npArrayHigh[-1],
            npArrayLow[-1],
            npArrayVolume[-1],
            score,
            SMA_values[-1],
            EMA_values[-1],
            RSI_values[-1],
            MACD_values[-1],
            WILLR_values[-1],
            CCI_values[-1],
            ATR_values[-1]
        ]
        evaluate = model.predict_proba([predict])  # Utilizing predict.proba() returns the confidence scores for the prediction

        predScore = evaluate[0][1]  # Returns the array value for "positive" prediction or '1.' This value is displayed under each prediction for added context.
        if evaluate[0][1] > 0.75:
            prediction = "Go"
        else:
            prediction = "No Go"

    return render_template("landing.html", tickersList=tickersList, ticker_selection=ticker_selection, data1=data1,
                           data2=data2, prediction=prediction, predScore=predScore)


start_db()

if __name__ == '__main__':
    app.run(debug=True)
