from flask import request
import pyautogui


class MouseControl:
    @staticmethod
    def actions():
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
