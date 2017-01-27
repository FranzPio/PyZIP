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

1. ``PyZIP (Windows).zip`` entpacken
2. ``PyZIP.exe`` ausführen

***
- **Linux**

coming (sooner or) later.

***
- **Source**

1.

Python 3.x installieren (https://www.python.org/downloads/)

2.
```
pip install -U --pre -f https://wxpython.org/Phoenix/snapshot-builds/ wxPython_Phoenix
pip install ObjectListView
```

3.

Ordner ``PyZIP`` in Homeverzeichnis kopieren (/home/NAME oder C:\Users\NAME)

4.

``PyZIP.py`` ausführen

(z.B. ``python PyZIP.py`` bzw. ``python3 PyZIP.py``)
