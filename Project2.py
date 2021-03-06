from tkinter import *
from tkinter import font
from tkinter import filedialog
from PIL import ImageTk, Image
import subprocess as sp


def raise_frame(frame):
    frame.tkraise()


def upload_image():
    popup = Tk()
    popup.withdraw()
    options = {'filetypes': [('JPEG Files', '.jpg'), ('GIF Files', '.gif')]}
    global file_path
    file_path = filedialog.askopenfilename(**options)

    image = Image.open(file_path)
    photo = ImageTk.PhotoImage(image)
    label = Label(options_page, image=photo)
    label.image = photo
    label.pack()

    Button(options_page, text='Wiener Filter', command=alg1).pack()
    Button(options_page, text='Marr-Hildreth Edge Detector', command=alg2).pack()

    raise_frame(options_page)


def alg1():
    if sp.call(["./WienerFilterOMP/build/WienerFilter", file_path]) == 0:
        print("Wiener Filter")
        image = Image.open("WienerFiltered.png")
        photo = ImageTk.PhotoImage(image)
        label = Label(results_page, image=photo)
        label.image = photo
        label.pack()
        Button(results_page, text='Exit Program', command=results_page.quit).pack(side='left')
        raise_frame(results_page)
    else:
        print("Error")
        raise_frame(upload_page)


def alg2():
    if sp.call(["./MarrHildrethEdgeDetOMP/build/MarrHildreth", file_path]) == 0:
        print("Marr Hildreth Edge Detector")
        image = Image.open("MarrHildreth.png")
        photo = ImageTk.PhotoImage(image)
        label = Label(results_page, image=photo)
        label.image = photo
        label.pack()
        Button(results_page, text='Exit Program', command=results_page.quit).pack(side='left')
        raise_frame(results_page)
    else:
        print("Error")
        raise_frame(upload_page)

root = Tk()
upload_page = Frame(root)
options_page = Frame(root)
results_page = Frame(root)

for frame in (upload_page, options_page, results_page):
    frame.grid(row=0, column=0, sticky='news')
    title_font = font.Font(family='Helvetica', size=18, weight="bold")
    title = Label(frame, text="Parallel Image Processor", font=title_font).pack(fill=X, pady=20, padx=20)

# UPLOAD PAGE

upload_button = Button(upload_page, text='Upload Image', command=upload_image)
upload_button.pack()

raise_frame(upload_page)
root.mainloop()
