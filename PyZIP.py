#!/usr/bin/env python3
import wx
import ObjectListView as olv
import zipfile
import os.path
import sys


class Application(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SetIcon(wx.Icon(res_dir + "/PyZIP.ico"))

        self.UI()
        self.toolbar()
        self.Centre()
        self.Bind(wx.EVT_CLOSE, self.CloseApp)
        self.Show()

    def CloseApp(self, evt):
        if self.archive_contents_olv.ItemCount > 0:
            confirmation = wx.MessageDialog(None, "Sind Sie sicher?\n\nPyZIP wirklich schließen?", "Sicher?",
                                            style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
            if confirmation.ShowModal() == wx.ID_NO:
                return
        self.Destroy()

    def toolbar(self):
        toolbar = self.CreateToolBar(style=wx.TB_TEXT)
        open_archive_tool = toolbar.AddTool(wx.ID_OPEN, "Öffnen", wx.Bitmap(res_dir + "/open_archive.png"),
                                            "Bestehendes Archiv öffnen")
        toolbar.AddSeparator()
        extract_archive_tool = toolbar.AddTool(wx.ID_ANY, "Extrahieren", wx.Bitmap(res_dir + "/extract_archive.png"),
                                               "Ausgewählte Dateien extrahieren")
        toolbar.AddSeparator()
        verify_archive_tool = toolbar.AddTool(wx.ID_ANY, "Überprüfen", wx.Bitmap(res_dir + "/verify_archive.png"),
                                              "Archiv überprüfen (CRC, Header)")
        toolbar.AddSeparator()
        create_archive_tool = toolbar.AddTool(wx.ID_NEW, "Erstellen", wx.Bitmap(res_dir + "/new_archive.png"),
                                              "Neues Archiv erstellen")
        self.Bind(wx.EVT_TOOL, self.open_zip, open_archive_tool)
        self.Bind(wx.EVT_TOOL, self.extract_from_zip, extract_archive_tool)
        self.Bind(wx.EVT_TOOL, self.verify_zip, verify_archive_tool)
        self.Bind(wx.EVT_TOOL, self.create_zip, create_archive_tool)
        toolbar.Realize()

    def UI(self):
        # noinspection PyArgumentList
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.archive_contents_olv = olv.ObjectListView(self, style=wx.LC_REPORT)
        self.archive_contents_olv.SetColumns([
            olv.ColumnDefn("Dateiname", "right", valueGetter="filename", isSpaceFilling=True),
            olv.ColumnDefn("Größe", "right", 80, "size", isSpaceFilling=False),
            olv.ColumnDefn("Änderungsdatum", "right", 140, valueGetter="changed", isSpaceFilling=False)])
        self.archive_contents_olv.AutoSizeColumns()
        self.archive_contents_olv.SetEmptyListMsg("Kein Archiv ausgewählt")
        hbox1.Add(self.archive_contents_olv, 1, wx.EXPAND)
        vbox.Add(hbox1, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        vbox.Add((-1, 10))
        self.SetSizer(vbox)

    def open_zip(self, evt):
        wildcard = "Archivdateien| *.zip;*.bz2;*.xz;*.lzma"
        file_dialog = wx.FileDialog(self, "Dateien auswählen", "", "", wildcard, wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self.path_to_opened_zip = file_dialog.GetPath()
        filename_of_zip = file_dialog.GetFilename()
        file_extension_of_zip = filename_of_zip.split(".")[-1]
        try:
            with zipfile.ZipFile(self.path_to_opened_zip, "r") as zip_file:
                for zip_member in zip_file.infolist():
                    self.archive_contents_olv.AddObjects([{
                        "filename": zip_member.filename,
                        "size": str(round(zip_member.compress_size / 1000000, 3)) + " MB",
                        "changed": str(zip_member.date_time[2]) + "." + str(zip_member.date_time[1]) + "." +
                        str(zip_member.date_time[0])}])
        except zipfile.BadZipFile:
            wx.MessageBox("\"" + filename_of_zip + "\" ist keine gültige " + file_extension_of_zip.upper() + "-Datei!",
                          "Fehler", wx.OK | wx.ICON_EXCLAMATION)

    def extract_from_zip(self, evt):
        if self.archive_contents_olv.ItemCount == 0:
            pass  # MessageBox: no archive opened (???)
        else:
            file_dialog = wx.DirDialog(self, "Speicherort auswählen", "", wx.DD_DEFAULT_STYLE)
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            path_to_zip = file_dialog.GetPath()
            try:
                if self.archive_contents_olv.GetSelectedObjects():
                        with zipfile.ZipFile(self.path_to_opened_zip, "r") as zip_file:
                            for selection in self.archive_contents_olv.GetSelectedObjects():
                                zip_file.extract(selection["filename"], path_to_zip)

                else:
                    with zipfile.ZipFile(self.path_to_opened_zip, "r") as zip_file:
                        zip_file.extractall(path_to_zip)
            except FileNotFoundError:
                wx.MessageBox("Das Archiv \"" + self.path_to_opened_zip + "\"\nkonnte nicht gefunden werden.\n"
                              "Es wurde während der Bearbeitung gelöscht, verschoben oder umbenannt.", "Fehler",
                              wx.OK | wx.ICON_ERROR)
            except:
                wx.MessageBox("Extrahieren fehlgeschlagen!\nDas bedeutet meistens, dass das Archiv fehlerhaft ist.\n\n"
                              + str(sys.exc_info()[1]), "Unerwarteter Fehler", wx.OK | wx.ICON_ERROR)
            else:
                wx.MessageBox("Dateien erfolgreich extrahiert!", "Info", wx.OK | wx.ICON_INFORMATION)

    def verify_zip(self, evt):
        if self.archive_contents_olv.ItemCount == 0:
            pass  # MessageBox: no archive opened (???)
        else:
            try:
                with zipfile.ZipFile(self.path_to_opened_zip, "r") as zip_file:
                    verification = zip_file.testzip()
                    if verification:
                        wx.MessageBox("Es wurde mindestens ein Fehler im Archiv gefunden!\nErste fehlerhafte Datei:\n\n"
                                      + "\"" + verification + "\"", "Ergebnis", wx.OK | wx.ICON_EXCLAMATION)
                    else:
                        wx.MessageBox("Es wurden keine Fehler im Archiv gefunden!\n"
                                      "CRCs und Header sind einwandfrei.", "Ergebnis", wx.OK | wx.ICON_INFORMATION)
            except FileNotFoundError:
                wx.MessageBox("Das Archiv \"" + self.path_to_opened_zip + "\"\nkonnte nicht gefunden werden.\n"
                              "Es wurde während der Bearbeitung gelöscht, verschoben oder umbenannt.", "Fehler",
                              wx.OK | wx.ICON_ERROR)

            except:
                wx.MessageBox("Überprüfung fehlgeschlagen!\nDas bedeutet meistens, dass das Archiv fehlerhaft ist.\n\n"
                              + str(sys.exc_info()[1]), "Unerwarteter Fehler", wx.OK | wx.ICON_ERROR)

    @staticmethod
    def create_zip(evt):
        create_zip_dialog = CreateZipDialog(None, title="Neues Archiv",
                                            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        create_zip_dialog.ShowModal()

    @staticmethod
    def under_development(evt):
        wx.MessageBox("Diese Funktionalität ist noch in Entwicklung!", "Beta-Version", wx.OK | wx.ICON_INFORMATION)


class CreateZipDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.files_to_zip = None
        self.zip_destination = None
        self.zip_compression_method = zipfile.ZIP_STORED

        self.UI()
        self.Centre()
        self.SetMinSize((380, 330))
        self.SetSize((380, 330))
        self.Bind(wx.EVT_CLOSE, self.CloseDialog)
        self.Show()

    def CloseDialog(self, evt):
        self.Destroy()

    def UI(self):
        # noinspection PyArgumentList
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.StaticBoxSizer(wx.HORIZONTAL, self, " 1.  Dateien für das Archiv auswählen")
        hbox2 = wx.StaticBoxSizer(wx.HORIZONTAL, self, "2.  Kompressionsmethode wählen")
        hbox3 = wx.StaticBoxSizer(wx.HORIZONTAL, self, "3.  Speicherort wählen")
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        choose_files_button = wx.Button(self, label="Öffnen...")
        choose_files_button.Bind(wx.EVT_BUTTON, self.choose_files_dialog)
        hbox1.Add(choose_files_button, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add((-1, 10))
        vbox.Add(hbox1, 2, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        vbox.Add((-1, 10))
        compression_method_zip_stored_button = wx.RadioButton(self, label="ZIP", style=wx.RB_GROUP)
        compression_method_zip_stored_button.compression = zipfile.ZIP_STORED
        compression_method_zip_stored_button.Bind(wx.EVT_RADIOBUTTON, self.set_compression_method)
        compression_method_zip_deflated_button = wx.RadioButton(self, label="ZIP (komprimiert)")
        compression_method_zip_deflated_button.compression = zipfile.ZIP_DEFLATED
        compression_method_zip_deflated_button.Bind(wx.EVT_RADIOBUTTON, self.set_compression_method)
        compression_method_zip_bzip2_button = wx.RadioButton(self, label="BZIP2")
        compression_method_zip_bzip2_button.compression = zipfile.ZIP_BZIP2
        compression_method_zip_bzip2_button.Bind(wx.EVT_RADIOBUTTON, self.set_compression_method)
        compression_method_zip_lzma_button = wx.RadioButton(self, label="LZMA")
        compression_method_zip_lzma_button.compression = zipfile.ZIP_LZMA
        compression_method_zip_lzma_button.Bind(wx.EVT_RADIOBUTTON, self.set_compression_method)
        hbox2.Add(compression_method_zip_stored_button, 1, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(compression_method_zip_deflated_button, 1, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(compression_method_zip_bzip2_button, 1, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(compression_method_zip_lzma_button, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox2, 2, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        vbox.Add((-1, 10))
        zip_name_text = wx.StaticText(self, label="Speicherort:")
        self.zip_destination_textctrl = wx.TextCtrl(self, style=wx.TE_READONLY)
        choose_zip_destination_button = wx.Button(self, label="...", size=(30, -1))
        choose_zip_destination_button.Bind(wx.EVT_BUTTON, self.choose_zip_destination)
        hbox3.Add(zip_name_text, 2, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 10)
        hbox3.AddSpacer(20)
        hbox3.Add(self.zip_destination_textctrl, 6, wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM, 10)
        hbox3.Add(choose_zip_destination_button, 1, wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM, 10)
        vbox.Add(hbox3, 2, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        vbox.Add((-1, 20))
        create_zip_button = wx.Button(self, label="Archiv erstellen")
        create_zip_button.Bind(wx.EVT_BUTTON, self.create_zip)
        close_button = wx.Button(self, label="Schließen")
        close_button.Bind(wx.EVT_BUTTON, self.CloseDialog)
        hbox4.Add(create_zip_button, 1, wx.EXPAND | wx.LEFT, 20)
        hbox4.AddSpacer(20)
        hbox4.Add(close_button, 1, wx.EXPAND | wx.RIGHT, 20)
        vbox.Add(hbox4, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        vbox.Add((-1, 10))
        self.SetSizer(vbox)

    def set_compression_method(self, evt):
        self.zip_compression_method = evt.GetEventObject().compression
        self.zip_destination = None
        self.zip_destination_textctrl.SetValue("")

    def choose_files_dialog(self, evt):
        self.files_to_zip = {}
        file_dialog = wx.FileDialog(self, "Dateien auswählen", "", "", "",
                                    wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        for index, filename in enumerate(file_dialog.GetFilenames()):
            self.files_to_zip[filename] = file_dialog.GetPaths()[index]

    def choose_zip_destination(self, evt):
        if self.zip_compression_method == zipfile.ZIP_STORED or self.zip_compression_method == zipfile.ZIP_DEFLATED:
            file_extension = ".zip"
            wildcard = "ZIP-Archiv (*.zip) | *.zip"
        elif self.zip_compression_method == zipfile.ZIP_BZIP2:
            file_extension = ".bz2"
            wildcard = "BZIP2-Archiv (*.bz2) | *.bz2"
        elif self.zip_compression_method == zipfile.ZIP_LZMA:
            file_extension = ".xz"
            wildcard = "LZMA-Archiv (*.xz) | *.xz"
        else:
            file_extension = ""
            wildcard = ""
        file_dialog = wx.FileDialog(self, "Speicherort auswählen", "", "", wildcard,
                                    wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        path_to_zip = file_dialog.GetPath()
        self.zip_destination = path_to_zip if path_to_zip.endswith(file_extension) else path_to_zip + file_extension
        self.zip_destination_textctrl.SetValue(self.zip_destination)

    def create_zip(self, evt):
        if self.files_to_zip:
            if self.zip_destination:
                try:
                    with zipfile.ZipFile(self.zip_destination, "w", compression=self.zip_compression_method) as zip_file:
                        for filename, filepath in self.files_to_zip.items():
                            zip_file.write(filepath, filename)
                except FileNotFoundError:
                    wx.MessageBox("Mindestens eine Datei wurde während des Erstellens\n"
                                  "gelöscht, verschoben oder umbenannt.\n\n" + str(sys.exc_info()[1]), "Fehler",
                                  wx.OK | wx.ICON_ERROR)
                    os.remove(self.zip_destination)
                except:
                    wx.MessageBox("Erstellen des Archivs fehlgeschlagen!\n"
                                  "Eventuell gibt der Fehlercode weitere Informationen.\n\n"
                                  + str(sys.exc_info()[1]), "Unerwarteter Fehler", wx.OK | wx.ICON_ERROR)
                    os.remove(self.zip_destination)
                else:
                    wx.MessageBox("Archiv erfolgreich erstellt!", "Info", wx.OK | wx.ICON_INFORMATION)
                    self.CloseDialog(wx.EVT_CLOSE)
            else:
                wx.MessageBox("Kein Speicherort ausgewählt!", "Fehler", wx.OK | wx.ICON_EXCLAMATION)
        else:
            wx.MessageBox("Keine Dateien ausgewählt!", "Fehler", wx.OK | wx.ICON_EXCLAMATION)


res_dir = "res" if hasattr(sys, "frozen") else os.path.expanduser("~") + "/PyZIP"

app = wx.App()
window = Application(None, title="PyZIP", size=(400, 300))
app.MainLoop()
