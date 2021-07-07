from flask import request
import pyautogui
import sys


class KeyboardControl:
    @staticmethod
    def input_keyboard():
        text = request.form.get("text")
        if sys.platform != 'linux':
            if text == 'capslock':
                pyautogui.press(text)
                print("press and release " + text)
            else:
                pyautogui.keyDown(text)
                print("press " + text)
        else:
            pyautogui.press(text)
            print("press " + text)

    @staticmethod
    def input_text():
        # button event
        event = request.form.get('type')
        print(event)
        if event == "text":
            text = request.form.get("text")
            pyautogui.typewrite(text)
        else:
            pyautogui.press(event)
