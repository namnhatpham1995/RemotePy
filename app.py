import sys
import pyautogui

if sys.platform == 'linux':
    import Xlib.threaded
from flask import Flask, render_template, Response, request
from camera_desktop import Camera

app = Flask(__name__)


@app.route('/')
def index():
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
    if text == 'ctrl' or 'shift' or 'alt'
    pyautogui.press(text)
    return Response("success")


if __name__ == "__main__":
    app.run(host='192.168.0.101', port=5000, threaded=True)
