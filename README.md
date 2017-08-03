# PyZIP
(development stopped)
Archive manager using Python3 and wxPython-Phoenix [[German version](README_de.md)]
***
### Features

- compress one or multiple files or folders
- list archive members (+ file information)
- open files directly from within PyZIP
- extract some or all files from archive
- verify archive (CRCs, file headers)
- supported languages: English + German

***
### Supported archive formats

- **ZIP** (*.zip)

  (uncompressed / ZIP compressed / BZIP2 compressed / LZMA compressed)

***
### To do

- support additional archive formats (e.g. *.tar)
- en- / decryption -> password protected archives
- settings window with options to change language, appearance,...

##### etc.

***
### Installation

#### Windows

- double-click ``install.exe`` (ignore SmartScreen warning)

- when having problems with certificate, SmartScreen, etc., open cmd and type

  ``certutil -user -addstore Root "<SPEICHERORT>/CA.cer"``

***
#### Source

##### OS specific dependencies:

- (Windows only!) install Python 3.x (https://www.python.org/downloads/) (>=3.4 was tested)

- (Linux only!, in this case Debian/Ubuntu)

```bash
sudo apt-get install python3.5-dev dpkg-dev build-essential libwebkitgtk-dev libjpeg-dev libtiff-dev libgtk2.0-dev libsdl1.2-dev libgstreamer-plugins-base0.10-dev libnotify-dev freeglut3 freeglut3-dev python3-pip python3-setuptools
```
Adjust Python version in "python3.5-dev" accordingly!


##### All OSs:
```
pip install wxPython
pip install ObjectListView
```
maybe replace ``pip`` with ``pip3``

##### Launch PyZIP:

``python PyZIP.py`` or ``python3 PyZIP.py``

