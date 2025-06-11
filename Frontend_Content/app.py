#Flask supports 3.9 and newer
#Name file "app.py" to skip --app necessity

from flask import Flask, render_template, request, redirect, url_for, session
from Backend_Content.SecureLogin import test_passphrase
from Database.MongoDB_Connection import start_db

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def loginPage():
    if request.method == "POST":
        get_passphrase = request.form.get("passphrase")
        if test_passphrase(get_passphrase):
            return redirect(url_for("landingPage"))
        else:
            return "Invalid Passphrase", 403

    return '''
            <form method="POST">
                <label for="passphrase">Enter Passphrase:</label>
                <input type="password" name="passphrase" required>
                <button type="submit">Submit</button>
            </form>
        '''


@app.route("/landingPage", methods=["GET", "POST"])
def landingPage():
    return "This is the landing page"


if __name__ == '__main__':
    app.run(debug=True)
