import tkinter as tk
import threading
from flask import *

def userInterface():
    window = tk.Tk()
    window.title("File transfer")
    window.geometry('250x100')

    for i in range(2):
        window.columnconfigure(i, weight=1, minsize=75)
        window.rowconfigure(i, weight=1, minsize=50)
        if i == 1:
            for j in range(0, 2):
                frame = tk.Frame(
                    master=window,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.grid(row=i, column=j, padx=5, pady=5)
                if j == 0:
                    label = tk.Button(master=frame, text="Download")
                    label.pack()
                else:
                    label = tk.Button(master=frame, text="Upload")
                    label.pack()
        elif i == 0:
            frame = tk.Frame(master=window, relief=tk.FLAT, borderwidth=1, padx=5, pady=5)
            frame.grid(row=i, columnspan=2, padx=5, pady=5)
            lbl = tk.Label(frame, text="Exchange file with oneye")
            lbl.pack()

    window.mainloop()


def upload():
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


def download():
    send_file(app.config['DOWNLOAD_FOLDER'],  as_attachment=True)


threading.Thread(target=userInterface).start()
