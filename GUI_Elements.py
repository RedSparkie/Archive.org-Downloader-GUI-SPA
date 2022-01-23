#!/usr/bin/python3

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import Menu
from GUI_Functions import *

# Class handles the creation of the window
class Window:
    def __init__(self):
        # initial window declaration
        self.window = tk.Tk()
        self.window.title("Archive.org-DLG")
        self.window.geometry("600x400")

        # menu declaration
        self.menu = tk.Menu(self.window)

        self.fileMenuElements = tk.Menu(self.menu)
        self.fileMenuElements.add_command(label="Load File")
        self.fileMenuElements.add_separator()
        self.fileMenuElements.add_command(label="Exit")
        self.menu.add_cascade(label="File", menu=self.fileMenuElements)

        self.optionsMenuElements = tk.Menu(self.menu)
        self.optionsMenuElements.add_checkbutton(label="Toggle JPG Download")
        self.optionsMenuElements.add_command(label="Download Resolution Settings")
        self.optionsMenuElements.add_command(label="Thread Settings")
        self.menu.add_cascade(label="Options", menu=self.optionsMenuElements)

        self.helpMenuElements = tk.Menu(self.menu)
        self.helpMenuElements.add_command(label="About..")
        self.menu.add_cascade(label="Help", menu=self.helpMenuElements)

        self.window.config(menu=self.menu)

        # frame declarations
        self.loginFrame = tk.LabelFrame(self.window, text="Login", width=50, height=50)
        self.loginFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, ipady=5)
        self.downloadFrame = tk.Frame(self.window, width=50, height=50)
        self.downloadFrame.pack(side=tk.BOTTOM, padx=5, pady=5)
        self.urlFrame = tk.LabelFrame(self.window, text="URL(s)", padx=5, pady=5, width=50, height=50)
        self.urlFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=5, pady=5)

        # logins frame widgets
        self.emailLabel = tk.Label(self.loginFrame, text="Email: ")
        self.emailLabel.pack(side=tk.LEFT)
        self.emailEntry = tk.Entry(self.loginFrame, width=30)
        self.emailEntry.pack(side=tk.LEFT, fill=tk.X)
        self.passwordLabel = tk.Label(self.loginFrame, text="  Password: ")
        self.passwordLabel.pack(side=tk.LEFT)
        self.passwordEntry = tk.Entry(self.loginFrame, width=30, show="*")
        self.passwordEntry.pack(side=tk.LEFT, fill=tk.X)

        # urls frame widgets
        self.pasteButton = tk.Button(self.urlFrame, text="Paste")
        self.pasteButton.pack(side=tk.LEFT, fill=tk.Y)
        self.urlText = scrolledtext.ScrolledText(self.urlFrame, width=40, height=30)
        self.urlText.pack(side=tk.TOP, fill=tk.BOTH)

        # download frame widgets
        self.startButton = tk.Button(self.downloadFrame, text="Start Download", command=startDownload)
        self.startButton.pack(side=tk.LEFT)
        self.openLocationButton = tk.Button(self.downloadFrame, text="Open Download Location")
        self.openLocationButton.pack(side=tk.LEFT)
        self.progressBar = ttk.Progressbar(self.downloadFrame, orient=tk.HORIZONTAL, length=400)
        self.progressBar.pack(side=tk.LEFT, fill=tk.X)


    def start(self):
        self.window.mainloop()
