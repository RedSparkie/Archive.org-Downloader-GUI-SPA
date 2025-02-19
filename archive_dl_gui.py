#!/usr/bin/python3

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox
from tkinter import filedialog
import pyperclip as pc
import os
import subprocess, sys
from downloader_functions import *
from concurrent import futures

#---------------------START OF GUI COMMANDS---------------------

# load a text file into the url textbox
def load_file():
    filename = ""
    if sys.platform.startswith('linux'):
        filename = filedialog.askopenfilename(initialdir = "/home", title = "Selecciona un archivo", filetypes = (("Archivos de texto", "*.txt*"), ("Todos los archivos", "*.*")))
    elif sys.platform.startswith('win32'):
        filename = filedialog.askopenfilename(initialdir = "C:", title = "Selecciona un archivo", filetypes = (("Archivos de texto", "*.txt*"), ("Todos los archivos", "*.*")))
    file = open(filename)
    urlText.insert(tk.INSERT, file.read())

# close main window command
def exit_pressed():
    close_window(window, "main_win", 0)

# opens resolution settings window
def resolution_settings_pressed():
    top = tk.Toplevel(window)
    top.geometry("300x150")
    window.withdraw()

    # resolution settings widgets
    resolutionLabel = tk.Label(top, text="Establecer resolución\n(predeterminado: 3)")
    resolutionLabel.pack(pady=10, side=tk.TOP)

    resolutionEntry = tk.Entry(top, width=25)
    resolutionEntry.pack(pady=5, side=tk.TOP)

    resolutionButton = tk.Button(top, text="Ok", command=lambda:close_window(top, "resolución_config", resolutionEntry.get()))
    resolutionButton.pack(pady=5, side=tk.TOP)

    top.protocol("WM_DELETE_WINDOW", on_closing)

# opens thread settings window
def thread_settings_pressed():
    top = tk.Toplevel(window)
    top.geometry("300x150")
    window.withdraw()

    # resolution settings widgets
    threadLabel = tk.Label(top, text="Establecer intentos\n(predeterminados: 50)")
    threadLabel.pack(pady=10, side=tk.TOP)

    threadEntry = tk.Entry(top, width=25)
    threadEntry.pack(pady=5, side=tk.TOP)

    threadButton = tk.Button(top, text="Ok", command=lambda:close_window(top, "intentos_config", threadEntry.get()))
    threadButton.pack(pady=5, side=tk.TOP)

    top.protocol("WM_DELETE_WINDOW", on_closing)

def paste_pressed():
    urlText.insert(tk.INSERT, pc.paste())

def download(session, n_threads, directory, links, scale, book_id):
    print("Descargando páginas...")
    links = [f"{link}&rotate=0&scale={scale}" for link in links]

    tasks = []
    with futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
        for link in links:
            i = links.index(link)
            tasks.append(executor.submit(download_one_image, session=session, link=link, i=i, directory=directory ,book_id=book_id))
        for task in tqdm(futures.as_completed(tasks), total=len(tasks)):
            progressBar.step()
            window.update()

    images = [f"{directory}/{i}.jpg" for i in range(len(links))]
    return images

# downloads books from url(s) given
def start_download():
    # get urls from box, remove last character (newline)
    urls = urlText.get("1.0", tk.END+"-1c")
    if not urls:
        error_msg("Error en URL", "URLs no encontradas")
        return
    urls = parse_urls(urls)

    # Check the urls format
    for url in urls:
        if not url.startswith("https://archive.org/details/"):
            error_msg("Error en URLs", "URLs inválidas. URLs deben empezar con: \nhttps://archive.org/details/")
            return

    # disable window when downloading
    toggle_win_activity()
    window.update()

    # Begin download process
    for url in urls:
        # login to site
        session = login(emailEntry.get(), passwordEntry.get())
        if session == 1:
            error_msg("Error de login", "Credenciales de login inválidas")
            return
        elif session == 2:
            error_msg("Error de login", "Error al conectar")
            return

        # get urls
        book_id = list(filter(None, url.split("/")))[-1]
        print("="*40)
        print(f"Libro actual: {url}")
        session = loan(session, book_id)

        # gather book info
        title, links, progressBar['maximum'] = get_book_infos(session, url)
        if title == 1:
            error_msg("Error en el libro", "Error al obtener las imágenes")
            return

        directory = os.path.join(os.getcwd(), title)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        window.update()

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

    # finished download message
    result = tk.messagebox.askyesno(title="Descarga", message="¡Descarga completada!\n¿Abrir carpeta de descargas?")
    if result:
        open_dl_location()


    # enable window once finished downloading
    toggle_win_activity()

# open file explorer at current download directory
def open_dl_location():
    directory_path = os.getcwd()
    #folder_name = os.path.basename(directory_path)
    if sys.platform.startswith('linux'):
        os.system("xdg-open " + directory_path)
    elif sys.platform.startswith('win32'):
        os.system("explorer.exe " + directory_path)

# displays error messages to user
def error_msg(title, message):
    tk.messagebox.showwarning(title, message)

# close the pop up window
def close_window(win, win_specifier, value):
    # save data inputted by user for settings windows
    if win_specifier == "resolución_config":
        scale.set(value)
    elif win_specifier == "intentos_config":
        n_threads.set(value)

    window.deiconify()
    win.destroy()

# manages jpg toggle button setting
def jpg_toggled():
    if isJPG.get() == True:
        isJPG.set(False)
    elif isJPG.get() == False:
        isJPG.set(True)

# handles case where user exits program at settings windows
def on_closing():
    if messagebox.askokcancel("Salir", "¿Cerrar el programa?"):
        window.destroy()

def toggle_win_activity():
    if urlText['state'] == tk.NORMAL:
        urlText['state'] = tk.DISABLED
        pasteButton['state'] = tk.DISABLED
        openLocationButton['state'] = tk.DISABLED
        emailEntry['state'] = tk.DISABLED
        passwordEntry['state'] = tk.DISABLED
        startButton['state'] = tk.DISABLED
    else:
        urlText['state'] = tk.NORMAL
        pasteButton['state'] = tk.NORMAL
        openLocationButton['state'] = tk.NORMAL
        emailEntry['state'] = tk.NORMAL
        passwordEntry['state'] = tk.NORMAL
        startButton['state'] = tk.NORMAL


#---------------------START OF WINDOW CREATION---------------------

# initial window declaration
window = tk.Tk()
window.title("Archive.org-DL-GUI-español")
window.geometry("600x400")

# download settings variables
n_threads = tk.IntVar(window, value = 50)
scale = tk.IntVar(window, value = 3)
isJPG = tk.BooleanVar(window, False)

# menu declarations
menu = tk.Menu(window)

fileMenuElements = tk.Menu(menu)
fileMenuElements.add_command(label="Cargar archivo", command=load_file)
fileMenuElements.add_separator()
fileMenuElements.add_command(label="Salir", command=exit_pressed)
menu.add_cascade(label="Archivo", menu=fileMenuElements)

optionsMenuElements = tk.Menu(menu)
optionsMenuElements.add_checkbutton(label="Descargar como JPG", command=jpg_toggled)
optionsMenuElements.add_separator()
optionsMenuElements.add_command(label="Configuración de resolución de descarga", command=resolution_settings_pressed)
optionsMenuElements.add_command(label="Configuración de intentos", command=thread_settings_pressed)
menu.add_cascade(label="Opciones", menu=optionsMenuElements)

helpMenuElements = tk.Menu(menu)
helpMenuElements.add_command(label="Sobre el proyecto")
menu.add_cascade(label="Ayuda", menu=helpMenuElements)

window.config(menu=menu)

# frame declarations
loginFrame = tk.LabelFrame(window, text="Login", width=50, height=50)
loginFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, ipady=5)
downloadFrame = tk.Frame(window, width=50, height=50)
downloadFrame.pack(side=tk.BOTTOM, padx=5, pady=5)
urlFrame = tk.LabelFrame(window, text="URLs", padx=5, pady=5, width=50, height=50)
urlFrame.pack(expand=1, side=tk.BOTTOM, fill=tk.BOTH, padx=5, pady=5)

# logins frame widgets
emailLabel = tk.Label(loginFrame, text="Email: ")
emailLabel.pack(side=tk.LEFT)
emailEntry = tk.Entry(loginFrame, width=30)
emailEntry.pack(side=tk.LEFT, fill=tk.X)
passwordLabel = tk.Label(loginFrame, text="  Contraseña: ")
passwordLabel.pack(side=tk.LEFT)
passwordEntry = tk.Entry(loginFrame, width=30, show="*")
passwordEntry.pack(side=tk.LEFT, fill=tk.X)

# urls frame widgets
pasteButton = tk.Button(urlFrame, text="Pegar", command=paste_pressed)
pasteButton.pack(side=tk.LEFT, fill=tk.Y)
urlText = scrolledtext.ScrolledText(urlFrame, width=40, height=30)
urlText.pack(expand=1, side=tk.TOP, fill=tk.BOTH)

# download frame widgets
startButton = tk.Button(downloadFrame, text="Empezar descarga", command=start_download)
startButton.pack(side=tk.LEFT)
openLocationButton = tk.Button(downloadFrame, text="Abrir carpeta de descarga", command=open_dl_location)
openLocationButton.pack(side=tk.LEFT)
progressBar = ttk.Progressbar(downloadFrame, mode='determinate', orient=tk.HORIZONTAL, length=400)
progressBar.pack(side=tk.LEFT, fill=tk.X)


window.mainloop()
