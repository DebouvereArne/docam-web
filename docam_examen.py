from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from DbClass import DbClass
from PIRCamera import PIRCamera
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/pi/examen/datacom/Pycharm/static/ringtones'
ALLOWED_EXTENSIONS = set(['wav', 'mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')


# Source: https://pythonspot.com/en/login-authentication-with-flask/
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('Verkeerde wachtwoord.')
    return index()


@app.route('/timeline')
def timeline():
    DB_layer = DbClass()
    list_media = DB_layer.getMediaFromDatabase()
    return render_template('timeline.html', media=list_media)


@app.route('/sound')
def sound():
    return render_template('sound.html')


# Source: https://www.tutorialspoint.com/flask/flask_file_uploading.htm
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
    return sound()


@app.route('/settings')
def settings():
    return render_template('camerasettings.html')


@app.errorhandler(404)
def pagenotfound(error):
    return render_template("error/404.html", error=error)


if __name__ == '__main__':
    picamera = PIRCamera(20, 21, 16, 12)
    picamera.setRingtone("clarinet")
    picamera.cameraSettings(1280, 720, 60, 60)
    port = int(os.environ.get("PORT", 8080))
    host = "0.0.0.0"
    app.secret_key = os.urandom(12)
    app.run(host=host, port=port, debug=False)
