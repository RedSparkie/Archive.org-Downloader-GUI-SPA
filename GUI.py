#!/usr/bin/python3

import tkinter as tk  # note that module name has changed from Tkinter
                # in Python 2 to tkinter in Python 3\
root = tk.Tk()
root.title("Archive.org-Downloader")
# Code to add widgets will go here...

content = tk.Frame(root)
urlFrame = tk.Frame(content, borderwidth=5, relief="ridge"
    , width=600, height=400)
displayFrame = tk.Frame(content, borderwidth=5, relief="ridge"
    , width=600, height=100)
emailLabel = tk.Label(content, text="Email")
emailEntry = tk.Entry(content)
passwordLabel = tk.Label(content, text="Password")
passwordEntry = tk.Entry(content, show="*")

# placing contents of GUI on grid
content.grid(column=0, row=0)
    # login
emailLabel.grid(column=0, row=0, columnspan=1, sticky=(tk.E))
emailEntry.grid(column=1, row=0, columnspan=1
    , sticky=(tk.N, tk.E, tk.W), padx = 5)
passwordLabel.grid(column=2, row=0, columnspan=1
    , sticky=(tk.N, tk.E, tk.W))
passwordEntry.grid(column=3, row=0, columnspan=1
    , sticky=(tk.N, tk.E, tk.W), padx = 5)
    # url
urlFrame.grid(column=0, row=1, columnspan=3, rowspan=2)
    # display
displayFrame.grid(column=0, row=3, columnspan=3, rowspan=2)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

root.mainloop()
