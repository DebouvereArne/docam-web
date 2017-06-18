from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from DbClass import DbClass
from PIRCamera import PIRCamera
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/pi/examen/datacom/Pycharm/static/ringtones'
ALLOWED_EXTENSIONS = set(['wav', 'mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

picamera = PIRCamera(20, 21, 16, 12)

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


@app.route('/mode', methods=['GET','POST'])
def set_mode():
    option = request.form['options-mode']
    print(option)
    # if option == 'image-mode':
    #     picamera.setImageMode()
    # elif option == 'video-mode':
    #     picamera.setVideoMode()
    return settings()

@app.route('/timeline')
def timeline():
    DB_layer = DbClass()
    list_media = DB_layer.getMediaFromDatabase()
    return render_template('timeline.html', media=list_media)


@app.route('/sound')
def sound():
    DB_layer = DbClass()
    list_ringtones = DB_layer.getRingtonesFromDatabase()
    return render_template('sound.html', ringtones=list_ringtones)


# Sources: https://www.tutorialspoint.com/flask/flask_file_uploading.htm
#          http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            name = request.form['nameRingtone']
            DB_layer = DbClass()
            DB_layer.addRingtone(name, filename)
    return sound()


@app.route('/settings')
def settings():
    return render_template('camerasettings.html')


@app.route('/brightness', methods=['GET', 'POST'])
def set_brightness():
    if request.method == 'POST':
        brightness = request.form['amountBrightness']
        picamera.setBrightness(int(brightness))
    return settings()

@app.errorhandler(404)
def pagenotfound(error):
    return render_template("error/404.html", error=error)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    host = "0.0.0.0"
    app.secret_key = os.urandom(12)
    app.run(host=host, port=port, debug=False)
