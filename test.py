from tkinter import *

window = Tk()

window.title("File transfer")

window.geometry('200x100')

lbl = Label(window, text="Exchange file with oneye")

lbl.pack()

btn = Button(window, text="Download")

btn.pack()

btn = Button(window, text="Upload")

btn.pack()

window.mainloop()



