from flask import request
import pyautogui


class KeyboardControl:
    @staticmethod
    def input_keyboard():
        text = request.form.get("text")
        #    if text == 'ctrl' or 'shift' or 'alt'
        pyautogui.keyDown(text)

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
