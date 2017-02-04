# PyZIP
Archivmanager in Python mit wxPython
***
### Features

- Kompression von einer / mehreren beliebigen Dateien / Ordnern
- Anzeigen von Inhalten eines Archivs (+ Dateiinformationen)
- Öffnen von Archivmitgliedern direkt aus PyZIP heraus
- Extrahieren einzelner / aller Dateien eines Archivs
- Überprüfen eines Archivs (CRCs, Header)

***
### Unterstützte Archivformate

- ZIP (*.zip)

  (unkomprimiert / ZIP-komprimiert / BZIP2-komprimiert / LZMA-komprimiert)

***
### To do

- Unterstützung weiterer Formate
- Ver- / Entschlüsselung -> passwortgeschützte Archive
- Internationalisierung (u.a. Englisch)
- Entwickler- / Programminformationen aus PyZIP entnehmbar

##### u.v.m.

***
### Anleitung

#### Windows

- ``install.exe`` ausführen (SmartScreen-Warnung ignorieren)

- bei Problemen mit Zertifikat, SmartScreen-Filter etc.

  ``certutil -user -addstore Root "<SPEICHERORT>/CA.cer"``

***
#### Source

##### OS-spezifische Abhängigkeiten:

- (nur Windows!)

Python 3.x installieren (https://www.python.org/downloads/)

- (nur Linux!, hier Debian/Ubuntu)

```bash
sudo apt-get install python3.5-dev dpkg-dev build-essential libwebkitgtk-dev libjpeg-dev libtiff-dev libgtk2.0-dev libsdl1.2-dev libgstreamer-plugins-base0.10-dev libnotify-dev freeglut3 freeglut3-dev python3-pip python3-setuptools
```
Python-Version in "python3.5-dev" entsprechend anpassen!


##### Alle OS:
```
pip install -U --pre -f https://wxpython.org/Phoenix/snapshot-builds/ wxPython_Phoenix
pip install ObjectListView
```
evtl. ``pip`` durch ``pip3`` ersetzen

2.

Ordner ``PyZIP`` in Homeverzeichnis kopieren (/home/NAME oder C:\Users\NAME)

3.

``PyZIP.py`` ausführen

(z.B. ``python PyZIP.py`` bzw. ``python3 PyZIP.py``)
