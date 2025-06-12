#Flask supports 3.9 and newer
#Name file "app.py" to skip --app necessity

from flask import Flask, render_template, request, redirect, url_for, session
from matplotlib import pyplot as plt

from Backend_Content.SecureLogin import test_passphrase
from Database.MongoDB_Connection import start_db

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
        "ADP", "AFL", "ALB", "ALL", "AME", "AMP", "APD", "AVB", "BALL", "BBY",
        "QUBT", "BKR", "BR", "BXP", "CAG", "CB", "CDNS", "CE", "CF", "CHD"
    ]

    # Placeholders for visuals and ticker dropdown

    ticker_selection = request.form.get("Ticker")

    # # Generate chart using Matplotlib
    # plt.figure(figsize=(6, 4))
    # plt.plot(dates, close, marker='o')
    # plt.title(f"{ticker_selection} Trend")
    # plt.xlabel("Date")
    # plt.ylabel("Close Price")
    # plt.tight_layout()
    # plt.savefig("static/trend_plot.png")  # Save in /static/
    # plt.close()
    #
    # prediction = "Buy" if predictor.get("Successful") == 1 else "Don't Buy"
    # chart = None

    return render_template("landing.html", tickersList=tickersList, ticker_selection=ticker_selection)


if __name__ == '__main__':
    app.run(debug=True)
