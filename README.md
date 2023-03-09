 ![made-with-python](https://img.shields.io/badge/Made%20with-Python3-brightgreen)  
<!-- LOGO -->  
<br />  
<p align="left">  
  <h1 align="center">Archive.org Downloader GUI - Versión española</h1>  
</p>

## Sobre este proyecto  
Este proyecto está basado en el código de [alobeep](https://github.com/alobeep/Archive.org-Downloader-GUI), y este, a su vez, en el de [Minignome](https://github.com/MiniGlome/Archive.org-Downloader).

De aquí en adelante se ofrece una traducción de todo lo necesario para ejecutar el código en python o gracias al autoejecutable.

La página web https://archive.org/ ofrece una selección de libros gratuitos para su lectura y su descarga. Sin embargo, algunos libros solo pueden ser "tomados prestados" durante dos semanas. Algunos ni siquiera pueden ser descargados, lo que limita la lectura fuera de línea.

Este programa es una versión traducida y compilada para hispanohablantes.
  
### Captura de pantalla de la interfaz gráfica
![Archive org_DL_GUI](https://user-images.githubusercontent.com/71157556/195441576-e8eb9745-a713-4068-80d1-52f29058dc43.png)  
## Instalación - SO Linux 
  
Es necesario [Python3](https://www.python.org/downloads/) para ejecutar este programa.

También puedes instalarlo con este comando en Debian:
```sh  
sudo apt install python3
```

Instala también `git` con:   
```sh  
sudo apt install git
```  

  
### Clonar repositorio a directorio 
Entonces ejecuta el siguiente comando para descargar los archivos:  
```sh  
git clone https://github.com/RedSparkie/Archive.org-Downloader-GUI-SPAcd Archive.org-Downloader-GUI
```  
Este programa requiere los módulos `requests`, `tqdm`, `img2pdf`, `tkinter`, y `pyperclip`. 

Instálalos con pip:  
```sh  
pip install -r requirements.txt
```

### Ejecutar el programa 
Una vez que todo esté instalado, puedes ejecutarlo con el siguiente comando:  
```  
python3 archive_dl_gui.py
``` 
Deberías ver cómo aparece una ventana similar a la de abajo. Entonces, ingresa tu correo electrónico y tu contraseña, así como las URLs de los libros que quieras descargar de archive.org y comienza a descargar.
  
## Opciones
El programa viene con unas cuantas opciones tomadas del repositorio original.
![Archive org_DL_GUI_options](https://user-images.githubusercontent.com/71157556/195453465-468005be-bb96-472d-bb40-d0e9dd66847f.png)  
  
Estas opciones son:

 - descargar el libro como imágenes JPG.
 - establecer la resolución del libro.
 - la cantidad de intentos de descarga.

De forma adicional, presionando `Archivo` podremos cargar un archivo `.txt` en el que habremos escrito las URLs de los libros, una en cada línea, como muestra la imagen de abajo.
TODO: Imagen por poner.
  
## Creando el ejecutable
Exclusivo: Este *fork* dispone de un ejecutable ya compilado para Windows de este código a fecha de 09/03/2023. Lo puedes encontrar en [este enlace](https://github.com/RedSparkie/Archive.org-Downloader-GUI-SPA/releases/download/v0.1.0/downloader.exe).

Para evitar tener que ejecutar el comando cada vez, puedes crear un ejecutable gracias a la librería pyinstaller, que instalaremos con:
```  
pip install pyinstaller  
```  
Entonces, ejecuta el comando:
```  
pyinstaller --onefile archive_dl_gui.py  
```  
El ejecutable se guardará en la carpeta `dist` del directorio del proyecto.
Se hace necesario mencionar que para compilarlo, se deben tener descargados todos los requerimientos.
  
## Problemas potenciales
El autor de este fork no ha tenido problema alguno, pero reproduce aquí esta advertencia de la versión inglesa.
- Si no podéis pegar los distintos links, es porque es necesario instalar `xclip` y `xsel` en vuestro ordenador, lo cual podéis hacer con:  
```
  sudo apt install xclip xsel  
```

 - Si nada se descarga, puede ser porque la página esté bajo algún tipo de mantenimiento.
