from flask import Flask
from flask import render_template
from DbClass import DbClass
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def pagenotfound(error):
    return render_template("error/404.html", error=error)

if __name__ == '__main__':
    port = int(os.environ.get("PORT",8080))
    host = "0.0.0.0"
    app.run(host=host,port=port,debug=True)
