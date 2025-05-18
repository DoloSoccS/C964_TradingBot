#Flask supports 3.9 and newer
#Name file "app.py" to skip --app necessity

from flask import Flask

app = Flask(__name__)

@app.route("/")
# def landingPage():
#     return "<p>We need to make this function robust for inserting the required text, graphs and functions on the page.</p>"

def loginPage():
    return "Enter the student's ID to retrieve the passphrase. Then enter the passphrase below."

if __name__ == '__main__':
    app.run(debug=True)