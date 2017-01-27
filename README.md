# PyZIP
Archivmanager in Python mit wxPython
***
### Features
(weitere sind in Arbeit)

- Kompression von einer / mehreren beliebigen Dateien
- Anzeigen von Inhalten eines Archivs (+ Dateiinformationen)
- Extrahieren einzelner / aller Dateien eines Archivs
- Überprüfen eines Archivs (CRCs, Header)

***
### Unterstützte Archivformate

- ZIP (unkomprimiert / komprimiert) (*.zip)
- BZIP2 (*.bz2)
- LZMA (*.xz)

***
### Anleitung

- **Windows**

1.

``PyZIP (Windows).zip`` entpacken

2.

``PyZIP.exe`` ausführen

***
- **Linux**

coming (sooner or) later.

***
- **Source**

0,5. (nur Windows!) Python 3.x installieren (https://www.python.org/downloads/)

0,5. (nur Linux!, hier Debian/Ubuntu)

Python-Version in "python3.5-dev" entsprechend anpassen!
```bash
sudo apt-get install python3.5-dev dpkg-dev build-essential libwebkitgtk-dev libjpeg-dev libtiff-dev libgtk2.0-dev libsdl1.2-dev libgstreamer-plugins-base0.10-dev libnotify-dev freeglut3 freeglut3-dev python3-pip python3-setuptools
```


1.

evtl. ``pip`` durch ``pip3`` ersetzen
```
pip install -U --pre -f https://wxpython.org/Phoenix/snapshot-builds/ wxPython_Phoenix
pip install ObjectListView
```

2.

Ordner ``PyZIP`` in Homeverzeichnis kopieren (/home/NAME oder C:\Users\NAME)

3.

``PyZIP.py`` ausführen

(z.B. ``python PyZIP.py`` bzw. ``python3 PyZIP.py``)
