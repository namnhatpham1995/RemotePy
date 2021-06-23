# Import from python
import os
import sys
import uuid

# Import from libraries
import pyautogui
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

if sys.platform == 'linux':
    import Xlib.threaded
from flask import Flask, render_template, Response, request, redirect, send_file, session, url_for, g, flash

# Import from other files
import file
from camera_desktop import Camera

############################################################################################
# Setting ##################################################################################
############################################################################################
app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/Storage/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.sqlite3'
app.config['SECRET_KEY'] = "dcmyasuoganhteam123"
db = SQLAlchemy(app)


############################################################################################
# Log in and check user identity ###########################################################
############################################################################################
class Users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    token = db.Column(db.String(200))


# Make user list that can login
def __init__(self, username, password, token):
    self.username = username
    self.password = password
    self.token = token


@app.before_request
def before_request():
    g.user = None
    if 'user_token' and 'username' in session:  # if session is available (logged in before)
        # check database about the current user
        current_user = Users.query.filter_by(username=session['username']).first()
        print(current_user.username + ' is in session')
        # check token to ensure no one else log in in this account
        if current_user.token == session['user_token']:
            print('Right token, get in!')
            g.user = current_user.username
        else:
            session.pop('user_token', None)
            session.pop('username', None)
            print('Wrong token, logout')
            return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('user_token', None)  # remove all session when stay in log in page
    session.pop('username', None)

    if request.method == 'POST':
        if not request.form['username'] and not request.form['password']:  # Check if the log in form is not filled
            flash('Please enter username and password!', 'error')
        else:
            username = request.form['username']  # take user's identity from input
            password = request.form['password']
            user = Users.query.filter_by(username=username).first()  # check if database has the input user
            # by username
            if user is not None:  # check if user's identity is available
                if check_password_hash(user.password, password):
                    print(user.token)
                    new_session_token = str(uuid.uuid4())  # Generate new token for each log in time
                    user.token = new_session_token  # Add new token to user database
                    db.session.commit()
                    session['user_token'] = user.token  # Log session token and username
                    session['username'] = user.username
                    print(session['user_token'])
                    return redirect(url_for('index'))  # redirect to main page index
                else:
                    flash('Wrong Password, please try again!', 'error')  # Wrong password message
                    return redirect(url_for('login'))  # reload login page
            else:
                flash('This username is not exist!', 'error')  # Username isn't available message

    return render_template('login.html')


@app.route('/sign_out')
def sign_out():
    session.pop('user_token', None)
    session.pop('username', None)
    return redirect('/')


############################################################################################
# Pages to create new account and check database (Hidden)###################################
############################################################################################

# @app.route('/')
@app.route('/check_user')
def show_all():
    return render_template('show_all.html', Users=Users.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:  # Check if the create form is not filled
            flash('Please enter all the fields', 'error')
        else:
            new_user = Users(username=request.form['username'],
                             password=generate_password_hash(request.form['password']),
                             token=str(uuid.uuid4()))

            db.session.add(new_user)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


############################################################################################
# Remote control functions #################################################################
############################################################################################


@app.route('/')  # Decide which page is load from the beginning
@app.route('/index')  # Main page
def index():
    if not g.user:  # Check if user logged in before
        return redirect(url_for('login'))  # If not, to log in page
    else:
        return render_template('index.html')  # If yes, to main page


def gen(camera):  # get video frame of the remote desktop screen
    while True:
        frame = camera.get_frame()
        yield b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'


@app.route('/video_feed')  # Feed video to web page
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/mouse', methods=['POST'])  # control mouse
def mouse_event():
    # co-ordinates of browser image event
    ex, ey = float(request.form.get('x')), float(request.form.get('y'))
    # size of browser image
    imx, imy = float(request.form.get('X')), float(request.form.get('Y'))
    # size of desktop
    dx, dy = pyautogui.size()
    # co-ordinates of desktop event
    x, y = dx * (ex / imx), dy * (ey / imy)
    # mouse event
    event = request.form.get('type')

    if event == 'rightclick':
        pyautogui.click(x, y, button='right')
    elif event == 'click':
        pyautogui.click(x, y, button='left')
    elif event == 'mousewheelup':
        pyautogui.scroll(100)
    elif event == 'mousewheeldown':
        pyautogui.scroll(-100)
    elif event == 'mousepress':
        pyautogui.mouseDown(x, y)
    elif event == 'mouserelease':
        pyautogui.mouseUp(x, y)
    elif event == 'mousemove':
        if y == ey:
            pyautogui.moveTo(x, ey + 2)  # in case to show hidden taskbar
        elif x == ex:
            pyautogui.moveTo(ex + 2, y)
        elif y == 0:
            pyautogui.moveTo(x, -2)
        elif x == 0:
            pyautogui.moveTo(-2, y)
        else:
            pyautogui.moveTo(x, y)
    return Response("success")


@app.route('/keyboard', methods=['POST'])  # input keyboard on remote desktop
def keyboard_event():
    text = request.form.get("text")
    #    if text == 'ctrl' or 'shift' or 'alt'
    pyautogui.keyDown(text)
    return Response("success")


@app.route('/button', methods=['POST'])  # receive text from front end and paste to the field on remote desktop
def button_event():
    # button event
    event = request.form.get('type')
    print(event)
    if event == "text":
        text = request.form.get("text")
        pyautogui.typewrite(text)
    else:
        pyautogui.press(event)
    return Response("success")


'''
@app.route('/sendtext', methods=['POST'])
def send_text_event():
    # keyoard event
    event = request.form.get('type')
    print(event)
    if event == "text":
        text = request.form.get("text")
        pyautogui.typewrite(text)
    else:
        pyautogui.press(event)
    return Response("success")
'''


# Upload API
@app.route('/upload_file/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("saved file successfully")
    return render_template('index.html')


# Download API
@app.route("/downloadfile/")
def choose_file_download():
    file_path = file.chooseFile(UPLOAD_FOLDER)
    if file_path == "":
        return redirect('/')
    else:
        return redirect('/return-files/' + file_path)


@app.route('/return-files/<filename>')
def download_file(filename):
    # file_path = UPLOAD_FOLDER + filename
    file_path = filename.replace('*', '/')
    print(file_path)
    file_name = file.file_name_from_path(file_path)
    print(file_name)
    redirect('/')
    return send_file(file_path, as_attachment=True, attachment_filename=file_name)


if __name__ == "__main__":
    app.run(host='192.168.0.126', port=5000, threaded=True,
            ssl_context=('cert.pem', 'key.pem'))  # ,ssl_context='adhoc', ssl_context=('cert.pem', 'key.pem')
    # app.run(host='192.168.0.126', port=5000, threaded=True)
