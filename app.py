import os
import sys
import pyautogui
from werkzeug.utils import secure_filename

import file

if sys.platform == 'linux':
    import Xlib.threaded
from flask import Flask, render_template, Response, request, redirect, send_file, session, url_for, g
from camera_desktop import Camera

app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/Storage/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make user list that can login
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'
users = []
users.append(User(id=1, username='user1', password='123456'))
users.append(User(id=2, username='user2', password='secret'))
users.append(User(id=3, username='user3', password='password'))
app.secret_key = 'youmustknowthesecretkeytoaccess'
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        for x in users:
            if x.username == username:
                if x.password == password:
                    session['user_id'] = x.id
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('login'))


        # user = [x for x in users if x.username == username][0]

        # if user and user.password == password:
        #    session['user_id'] = user.id
        #    return redirect(url_for('profile'))
        # else:
        #    return redirect(url_for('login'))

    return render_template('login.html')
@app.route('/sign_out')
def sign_out():
    session.pop('user_id', None)
    return redirect('/')


@app.route('/index')
def index():
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/mouse', methods=['POST'])
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


@app.route('/keyboard', methods=['POST'])
def keyboard_event():
    text = request.form.get("text")
    #    if text == 'ctrl' or 'shift' or 'alt'
    pyautogui.keyDown(text)
    return Response("success")


@app.route('/button', methods=['POST'])
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
    app.run(host='192.168.0.126', port=5000, threaded=True, ssl_context=('cert.pem', 'key.pem'))#,ssl_context='adhoc', ssl_context=('cert.pem', 'key.pem')
    #app.run(host='192.168.0.126', port=5000, threaded=True)