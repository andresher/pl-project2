from tkinter import *
from tkinter import font
from tkinter import filedialog
from PIL import ImageTk, Image


def raise_frame(frame):
    frame.tkraise()


def upload_image():
    popup = Tk()
    popup.withdraw()
    options = {'filetypes': [('JPEG Files', '.jpg'), ('GIF Files', '.gif')]}
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
    print("Wiener Filter")
    raise_frame(results_page)


def alg2():
    print("Marr-Hildreth Edge Detector")
    raise_frame(results_page)


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

# RESULTS PAGE

# TODO Show Processed Image
Button(results_page, text='Process a new image', command=lambda:raise_frame(upload_page)).pack(side='left')
Button(results_page, text='Exit Program', command=results_page.quit).pack(side='left')

raise_frame(upload_page)
root.mainloop()
