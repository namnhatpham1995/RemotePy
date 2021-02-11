import tkinter
from tkinter import filedialog


def chooseFile(UPLOAD_FOLDER):
    window = tkinter.Tk()
    file_path = filedialog.askopenfilename(initialdir=UPLOAD_FOLDER, title='Choose a file')  # check file address (name)
    if file_path != "":  # Full address of the file, ex: F:/data/uploads/oppo123.jpg
        print("%s is chosen" % file_path)
        file_path_new = file_path.replace('/', '*')  # Change / to * for the string on address bar
        window.after(1000, lambda: window.destroy())  # Destroy the widget (tk window) after 1 seconds to run next line
        window.mainloop()
        return file_path_new

    else:  # No file is chosen
        print("No file is chosen")
        window.after(1000, lambda: window.destroy())  # Destroy the widget after 1 seconds
        window.mainloop()
        return file_path  # Return empty string as name


def file_name_from_path(file_path):
    path_list = file_path.split('/')  # Split full address into list, ex: ["F:", "data", "uploads" ,"oppo123.jpg"]
    file_name = path_list[len(path_list) - 1]  # File name in last position of the list
    print("File's name is: %s", file_name)
    return file_name

