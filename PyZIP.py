#!/usr/bin/env python
import wx
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
        self.Show()

    def toolbar(self):
        toolbar = self.CreateToolBar(style=wx.TB_TEXT)
        open_archive_tool = toolbar.AddTool(wx.ID_OPEN, "Öffnen", wx.Bitmap(res_dir + "/open_archive.png"),
                                            "Bestehendes Archiv öffnen")
        toolbar.AddSeparator()
        create_archive_tool = toolbar.AddTool(wx.ID_NEW, "Erstellen", wx.Bitmap(res_dir + "/new_archive.png"),
                                              "Neues Archiv erstellen")
        self.Bind(wx.EVT_TOOL, self.under_development, open_archive_tool)
        self.Bind(wx.EVT_TOOL, self.create_zip_dialog, create_archive_tool)
        toolbar.Realize()

    def UI(self):
        pass
        # noinspection PyArgumentList
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.archive_contents_listctrl = wx.ListCtrl(self)
        hbox1.Add(self.archive_contents_listctrl, 1, wx.EXPAND)
        vbox.Add(hbox1, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        vbox.Add((-1, 10))
        self.SetSizer(vbox)

    @staticmethod
    def under_development(evt):
        wx.MessageBox("Diese Funktionalität ist noch in Entwicklung!", "Beta-Version", wx.OK | wx.ICON_INFORMATION)

    @staticmethod
    def create_zip_dialog(evt):
        create_zip_dialog = CreateZipDialog(None, title="Neues Archiv",
                                            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        create_zip_dialog.ShowModal()


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
        hbox1 = wx.StaticBoxSizer(wx.HORIZONTAL, self, " 1.  Dateien für das ZIP-Archiv auswählen")
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
        create_zip_button = wx.Button(self, label="ZIP-Archiv erstellen")
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
        if self.zip_compression_method == zipfile.ZIP_STORED:
            file_extension = ".zip"
            wildcard = "ZIP-Archiv (*.zip) | *.zip"
        elif self.zip_compression_method == zipfile.ZIP_DEFLATED:
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
                with zipfile.ZipFile(self.zip_destination, "w", compression=self.zip_compression_method) as zip_file:
                    for filename, filepath in self.files_to_zip.items():
                        zip_file.write(filepath, filename)
                wx.MessageBox("Archiv erfolgreich erstellt!", "Info", wx.OK | wx.ICON_INFORMATION)
                self.CloseDialog(wx.EVT_CLOSE)
            else:
                wx.MessageBox("Kein Speicherort ausgewählt!", "Fehler", wx.OK | wx.ICON_EXCLAMATION)
        else:
            wx.MessageBox("Keine Dateien ausgewählt!", "Fehler", wx.OK | wx.ICON_EXCLAMATION)


res_dir = "res" if hasattr(sys, "frozen") else os.path.expanduser("~") + "/PyZIP"

app = wx.App()
window = Application(None, title="PyZIP", size=(360, 250))
app.MainLoop()
