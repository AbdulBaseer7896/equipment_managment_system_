from flask import Flask , render_template , request

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/")
def hello_world():
    return render_template('index.html')

from controller import *


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)