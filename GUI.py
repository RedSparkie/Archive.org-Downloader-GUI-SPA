#!/usr/bin/python3

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import Menu
from downloaderFunctions import *
from tkinter import messagebox
import pyperclip as pc

# gui commands
def load_file():
    print("test")

def exit_pressed():
    close_window(window, "main_win", 0)

def resolution_settings_pressed():
    top = tk.Toplevel(window)
    top.geometry("300x150")
    window.withdraw()

    # resolution settings widgets
    resolutionLabel = tk.Label(top, text="Set resolution settings\n(default: 3)")
    resolutionLabel.pack(pady=10, side=tk.TOP)

    resolutionEntry = tk.Entry(top, width=25)
    resolutionEntry.pack(pady=5, side=tk.TOP)

    resolutionButton = tk.Button(top, text="Ok", command=lambda:close_window(top, "res_settings", resolutionEntry.get()))
    resolutionButton.pack(pady=5, side=tk.TOP)

def thread_settings_pressed():
    top = tk.Toplevel(window)
    top.geometry("300x150")
    window.withdraw()

    # resolution settings widgets
    threadLabel = tk.Label(top, text="Set thread settings\n(default: 50)")
    threadLabel.pack(pady=10, side=tk.TOP)

    threadEntry = tk.Entry(top, width=25)
    threadEntry.pack(pady=5, side=tk.TOP)

    threadButton = tk.Button(top, text="Ok", command=lambda:close_window(top, "thread_settings", threadEntry.get()))
    threadButton.pack(pady=5, side=tk.TOP)

def paste_pressed():
    urlText.insert(tk.INSERT, pc.paste())

# downloads books from url(s) given
def start_download():
    # get urls from box, remove last character (newline)
    urls = urlText.get("1.0", tk.END+"-1c")
    if not urls:
        error_msg("URL Error", "No URLs present")
    urls = parse_urls(urls)

    # Check the urls format
    for url in urls:
        if not url.startswith("https://archive.org/details/"):
            error_msg("URL(s) Error", "Invalid URL(s). URL(s) must starts with: \nhttps://archive.org/details/")
            return

    # Begin download process
    for url in urls:
        # login to site
        session = login(emailEntry.get(), passwordEntry.get())
        if session == 1:
            error_msg("Login Error", "Invalid login credentials")
            return
        elif session == 2:
            error_msg("Login Error", "Error with login")
            return

        # get urls
        book_id = list(filter(None, url.split("/")))[-1]
        print("="*40)
        print(f"Current book: {url}")
        session = loan(session, book_id)

        # gather book info
        title, links = get_book_infos(session, url)
        if title == 1:
            error_msg("Book Error", "Error while getting image links")
            return

        directory = os.path.join(os.getcwd(), title)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        # download book as jpgs
        images = download(session, n_threads.get(), directory, links, scale.get(), book_id)

        # converts book images to pdf
        if isJPG.get() == False:
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

# close the pop up window
def close_window(win, win_specifier, value):
    # save data inputted by user for settings windows
    if win_specifier == "res_settings":
        scale.set(value)
    elif win_specifier == "thread_settings":
        n_threads.set(value)

    window.deiconify()
    win.destroy()

# manages jpg toggle button setting
def jpg_toggled():
    if isJPG.get() == True:
        isJPG.set(False)
    elif isJPG.get() == False:
        isJPG.set(True)

#---------------------START OF WINDOW CREATION---------------------

# initial window declaration
window = tk.Tk()
window.title("Archive.org-DLG")
window.geometry("600x400")

# download settings variables
n_threads = tk.IntVar(window, value = 50)
scale = tk.IntVar(window, value = 3)
isJPG = tk.BooleanVar(window, False)

# menu declarations
menu = tk.Menu(window)

fileMenuElements = tk.Menu(menu)
fileMenuElements.add_command(label="Load File", command=load_file)
fileMenuElements.add_separator()
fileMenuElements.add_command(label="Exit", command=exit_pressed)
menu.add_cascade(label="File", menu=fileMenuElements)

optionsMenuElements = tk.Menu(menu)
optionsMenuElements.add_checkbutton(label="Toggle JPG Download", command=jpg_toggled)
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
