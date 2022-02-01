#!/usr/bin/python3

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import Menu
from downloaderFunctions import *
from tkinter import messagebox

# gui commands
def load_file():
    print("test")

def exit_pressed():
    print("test")

def resolution_settings_pressed():
    print("test")

def thread_settings_pressed():
    print("test")

def paste_pressed():
    print("test")

# downloads books from url(s) given
def start_download():
    #tmp
    n_threads = 50
    scale = 3
    isJPG = False
    # get urls from box, remove last character (newline)
    urls = urlText.get("1.0", tk.END+"-1c")

    # login to site
    session = login(emailEntry.get(), passwordEntry.get())
    # get urls
    book_id = list(filter(None, urls.split("/")))[-1]
    print("="*40)
    print(f"Current book: {urls}")
    session = loan(session, book_id)
    title, links = get_book_infos(session, urls)

    directory = os.path.join(os.getcwd(), title)
    if not os.path.isdir(directory):
        os.makedirs(directory)

    # download book as jpgs
    images = download(session, n_threads, directory, links, scale, book_id)

    # converts book images to pdf
    if isJPG == False:
        pdf = img2pdf.convert(images)
        make_pdf(pdf, title)
        try:
            shutil.rmtree(directory)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))

    # return loan for the downloaded book
    return_loan(session, book_id)


def open_dl_location():
    print("test")
    error_msg("ERROR", "test")

# displays error messages to user
def error_msg(title, message):
    tk.messagebox.showwarning(title, message)

#---------------------START OF WINDOW CREATION---------------------

# initial window declaration
window = tk.Tk()
window.title("Archive.org-DLG")
window.geometry("600x400")

# menu declaration
menu = tk.Menu(window)

fileMenuElements = tk.Menu(menu)
fileMenuElements.add_command(label="Load File", command=load_file)
fileMenuElements.add_separator()
fileMenuElements.add_command(label="Exit", command=exit_pressed)
menu.add_cascade(label="File", menu=fileMenuElements)

optionsMenuElements = tk.Menu(menu)
optionsMenuElements.add_checkbutton(label="Toggle JPG Download")
optionsMenuElements.add_separator()
optionsMenuElements.add_command(label="Download Resolution Settings", command=resolution_settings_pressed)
optionsMenuElements.add_command(label="Thread Settings", command=thread_settings_pressed)
menu.add_cascade(label="Options", menu=optionsMenuElements)

helpMenuElements = tk.Menu(menu)
helpMenuElements.add_command(label="About..")
menu.add_cascade(label="Help", menu=helpMenuElements)

window.config(menu=menu)

# frame declarations
loginFrame = tk.LabelFrame(window, text="Login", width=50, height=50)
loginFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, ipady=5)
downloadFrame = tk.Frame(window, width=50, height=50)
downloadFrame.pack(side=tk.BOTTOM, padx=5, pady=5)
urlFrame = tk.LabelFrame(window, text="URL(s)", padx=5, pady=5, width=50, height=50)
urlFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=5, pady=5)

# logins frame widgets
emailLabel = tk.Label(loginFrame, text="Email: ")
emailLabel.pack(side=tk.LEFT)
emailEntry = tk.Entry(loginFrame, width=30)
emailEntry.pack(side=tk.LEFT, fill=tk.X)
passwordLabel = tk.Label(loginFrame, text="  Password: ")
passwordLabel.pack(side=tk.LEFT)
passwordEntry = tk.Entry(loginFrame, width=30, show="*")
passwordEntry.pack(side=tk.LEFT, fill=tk.X)

# urls frame widgets
pasteButton = tk.Button(urlFrame, text="Paste", command=paste_pressed)
pasteButton.pack(side=tk.LEFT, fill=tk.Y)
urlText = scrolledtext.ScrolledText(urlFrame, width=40, height=30)
urlText.pack(side=tk.TOP, fill=tk.BOTH)

# download frame widgets
startButton = tk.Button(downloadFrame, text="Start Download", command=start_download)
startButton.pack(side=tk.LEFT)
openLocationButton = tk.Button(downloadFrame, text="Open Download Location", command=open_dl_location)
openLocationButton.pack(side=tk.LEFT)
progressBar = ttk.Progressbar(downloadFrame, orient=tk.HORIZONTAL, length=400)
progressBar.pack(side=tk.LEFT, fill=tk.X)

window.mainloop()
