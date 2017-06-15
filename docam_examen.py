from flask import Flask
from flask import render_template
import os
from DbClass import DbClass
from PIRCamera import PIRCamera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/timeline')
def timeline():
    DB_layer = DbClass()
    list_media = DB_layer.getMediaFromDatabase()
    return render_template('timeline.html', media=list_media)

@app.route('/sound-inside')
def soundinside():
    return render_template('sound-inside.html')

@app.route('/sound-outside')
def soundoutside():
    return render_template('sound-outside.html')

@app.errorhandler(404)
def pagenotfound(error):
    return render_template("error/404.html", error=error)

if __name__ == '__main__':
    picamera = PIRCamera(20, 21, 16, 12)
    picamera.setRingtone("clarinet")
    picamera.cameraSettings(1280, 720, 60, 60)
    port = int(os.environ.get("PORT",8080))
    host = "0.0.0.0"
    app.run(host=host,port=port,debug=False)