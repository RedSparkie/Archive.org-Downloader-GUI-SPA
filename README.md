
![made-with-python](https://img.shields.io/badge/Made%20with-Python3-brightgreen)
<!-- LOGO -->
<br />
<p align="left">
  <h1 align="center">Archive.org Downloader GUI</h1>
</p>

## About This Project

The site https://archive.org/ offers a selection of free books to view and some to download. However due to the current makeup of said site, some books can only be "borrowed" for a two week span at maximum. Others still are not available for download which limits offline reading. This program, which was forked from https://github.com/MiniGlome/Archive.org-Downloader that offered up the initial download script, offers a GUI experience to easily download books into PDF format.

### Screenshot

![Archive org_DL_GUI](https://user-images.githubusercontent.com/71157556/195441576-e8eb9745-a713-4068-80d1-52f29058dc43.png)
## Installation - Linux OS

Python3 is required for this program to work: https://www.python.org/downloads/
Or a command can be used to install on Debian: 
```sh
sudo apt install python3
```
Also install git with: 
```sh
sudo apt install git
```

### Clone Repository to Directory
Then you can run the following commands to get the scripts on your computer:
```sh
git clone https://github.com/alobeep/Archive.org-Downloader-GUI
cd Archive.org-Downloader-GUI
```
The program requires following python modules `requests`, `tqdm`, `img2pdf`, `tkinter`, and `pyperclip`. Install them all with pip:
```sh
pip install -r requirements.txt
```

### Running the Program
Now that everything is installed, to run the program you do the following command:
```
python3 archive_dl_gui.py 
```
You should see a program pop up like the screenshot shown above. Now just input your email and password, as well as the URLs of the books to be downloaded, from your archive.org account and begin downloading.

## Options

The program comes with a couple of options taken from the original script. 
![Archive org_DL_GUI_options](https://user-images.githubusercontent.com/71157556/195453465-468005be-bb96-472d-bb40-d0e9dd66847f.png)

These options are JPG download which makes the book download as a set of images, the download resolution of the book, and the amount of threads for downloading. Additionally, under `File` a text file with URLs can be loaded into the program.

## Creating an Executable
In order to avoid having to run the command every time you would want to use the program, instead you could make an executable. This can be done with the use of pyinstaller. First, install pyinstaller with:
```
pip install pyinstaller
```
Then, run the command: 
```
pyinstaller --onefile archive_dl_gui.py
```
The executable should then be within the `dist` folder in the same directory.

## Potential Issues
- If the paste button does not work, you need to install xclip and xsel:
	```
	sudo apt install xclip xsel
	```
- If nothing is downloading, could be that the site is experiencing maintenance.	
