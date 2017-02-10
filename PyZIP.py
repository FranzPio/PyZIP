#!/usr/bin/env python3
import wx
import wx.adv
import ObjectListView as olv
import zipfile
import os.path
import sys
import collections.abc
import datetime
import subprocess
import tempfile
import images
import locales


class Application(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SetIcon(images.PyZIP.GetIcon())
        self.SetMinSize((400, 300))

        self.UI()
        self.toolbar()
        self.Centre()
        self.Bind(wx.EVT_CLOSE, self.CloseApp)
        self.Show()
        try:
            self.open_with_PyZIP(sys.argv[1])
        except IndexError:
            pass
        except FileNotFoundError:
            wx.MessageBox(strings.archive_not_existing_error + "\n\n" + str(sys.exc_info()[1]),
                          strings.error, wx.OK | wx.ICON_ERROR)
        except:
            wx.MessageBox("Öffnen des Archivs fehlgeschlagen\n\n" + str(sys.exc_info()[1]),
                          "Unerwarteter Fehler", wx.OK | wx.ICON_ERROR)

    def CloseApp(self, evt):
        if self.archive_contents_olv.ItemCount > 0:
            confirmation = wx.MessageDialog(None, strings.are_you_sure + "\n\n" + strings.really_quit, strings.sure,
                                            style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
            if confirmation.ShowModal() == wx.ID_NO:
                return
        self.Destroy()

    def toolbar(self):
        toolbar = self.CreateToolBar(style=wx.TB_TEXT)
        open_archive_tool = toolbar.AddTool(wx.ID_OPEN, "Öffnen", images.open_archive.GetBitmap(),
                                            "Bestehendes Archiv öffnen")
        toolbar.AddSeparator()
        extract_archive_tool = toolbar.AddTool(wx.ID_ANY, "Extrahieren", images.extract_archive.GetBitmap(),
                                               "Ausgewählte Dateien extrahieren")
        toolbar.AddSeparator()
        verify_archive_tool = toolbar.AddTool(wx.ID_ANY, "Überprüfen", images.verify_archive.GetBitmap(),
                                              "Archiv überprüfen (CRC, Header)")
        toolbar.AddSeparator()
        create_archive_tool = toolbar.AddTool(wx.ID_NEW, "Erstellen", images.new_archive.GetBitmap(),
                                              "Neues Archiv erstellen")
        toolbar.AddSeparator()
        toolbar.AddStretchableSpace()
        about_info = toolbar.AddTool(wx.ID_ABOUT, "Info", images.about_info.GetBitmap(),
                                     "Über PyZIP")
        self.Bind(wx.EVT_TOOL, self.open_zip, open_archive_tool)
        self.Bind(wx.EVT_TOOL, self.extract_from_zip, extract_archive_tool)
        self.Bind(wx.EVT_TOOL, self.verify_zip, verify_archive_tool)
        self.Bind(wx.EVT_TOOL, self.create_zip, create_archive_tool)
        self.Bind(wx.EVT_TOOL, self.about_dialog, about_info)
        toolbar.Realize()

    def UI(self):
        if os.name != "posix":
            # noinspection PyArgumentList
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.archive_contents_olv = olv.FastObjectListView(self, sortable=True, style=wx.LC_REPORT)
        self.archive_contents_olv.SetColumns([
            olv.ColumnDefn("Dateiname", "right", valueGetter="filename", isSpaceFilling=True),
            olv.ColumnDefn("Größe", "right", 80, "size", isSpaceFilling=False),
            olv.ColumnDefn("Änderungsdatum", "right", 140, "changed", isSpaceFilling=False,
                           stringConverter="%d.%m.%Y")])
        # self.archive_contents_olv.AutoSizeColumns()
        self.archive_contents_olv.SetEmptyListMsg("Kein Archiv ausgewählt")
        self.archive_contents_olv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.open_archive_member)
        hbox1.Add(self.archive_contents_olv, 1, wx.EXPAND)
        vbox.Add(hbox1, 10, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        self.archive_member_count_text = wx.StaticText(self, label="0 Dateien",
                                                       style=wx.ST_NO_AUTORESIZE | wx.ALIGN_RIGHT)
        hbox2.Add(self.archive_member_count_text, 1, wx.EXPAND)
        vbox.Add(hbox2, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        vbox.Add((-1, 5))
        self.SetSizer(vbox)

    def open_archive_member(self, evt):
        # yet only opens the directory the zipfile is located in
        # should later silently extract the file and open the right application to play / view /... it!
        try:
            with zipfile.ZipFile(self.path_to_opened_zip, "r") as zip_file:
                filename_of_temp_extracted = self.archive_contents_olv.GetSelectedObject()["filename"]
                path_to_temp_extracted = os.path.join(tempfile.gettempdir(), filename_of_temp_extracted)
                busy_cursor = wx.BusyCursor()
                zip_file.extract(filename_of_temp_extracted, tempfile.gettempdir())
                del busy_cursor
            if os.name == "posix":
                subprocess.call(["xdg-open", path_to_temp_extracted])
            elif os.name == "nt":
                subprocess.call(["start", path_to_temp_extracted], shell=True)
        except:
            wx.MessageBox("Unerwarteter Fehler\n\n" + str(sys.exc_info()[1]), "Error", wx.OK | wx.ICON_ERROR)

    def open_with_PyZIP(self, path_to_zip):
        archive_member_count = 0
        self.path_to_opened_zip = path_to_zip
        filename_of_zip = self.path_to_opened_zip.split(os.sep)[-1]
        try:
            with zipfile.ZipFile(self.path_to_opened_zip, "r") as zip_file:
                for zip_member in zip_file.infolist():
                    self.archive_contents_olv.AddObjects([{
                        "filename": zip_member.filename,
                        "size": str(round(zip_member.compress_size / 1000000, 3)) + " MB",
                        "changed": datetime.datetime(zip_member.date_time[0], zip_member.date_time[1],
                                                     zip_member.date_time[2])}])
                    archive_member_count += 1
            self.archive_member_count_text.SetLabel(str(archive_member_count) + " Dateien")
        except zipfile.BadZipFile:
            wx.MessageBox("\"" + filename_of_zip + "\" ist keine gültige " + "Archivdatei oder sie ist beschädigt!",
                          "Fehler", wx.OK | wx.ICON_EXCLAMATION)

    def open_zip(self, evt):
        wildcard = "Archivdateien|*.zip;*.bz2;*.xz;*.lzma"
        file_dialog = wx.FileDialog(self, "Dateien auswählen", "", "", wildcard, wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        archive_member_count = 0
        self.archive_contents_olv.DeleteAllItems()
        self.path_to_opened_zip = file_dialog.GetPath()
        filename_of_zip = file_dialog.GetFilename()
        file_extension_of_zip = filename_of_zip.split(".")[-1].upper()
        try:
            with zipfile.ZipFile(self.path_to_opened_zip, "r") as zip_file:
                for zip_member in zip_file.infolist():
                    self.archive_contents_olv.AddObjects([{
                        "filename": zip_member.filename,
                        "size": str(round(zip_member.compress_size / 1000000, 3)) + " MB"
                        if zip_member.compress_size > 1000 else str(zip_member.compress_size) + " KB",
                        "changed": datetime.datetime(zip_member.date_time[0], zip_member.date_time[1],
                                                     zip_member.date_time[2])}])
                    archive_member_count += 1
            self.archive_member_count_text.SetLabel(str(archive_member_count) + " Dateien")
        except zipfile.BadZipFile:
            wx.MessageBox("\"" + filename_of_zip + "\" ist keine gültige " + file_extension_of_zip + "-Datei "
                          "oder sie ist beschädigt!",
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
            busy_cursor = wx.BusyCursor()
            try:
                with zipfile.ZipFile(self.path_to_opened_zip, "r") as zip_file:
                    verification = zip_file.testzip()
                    del busy_cursor
                    if verification:
                        wx.MessageBox("Es wurde mindestens ein Fehler im Archiv gefunden!\nErste fehlerhafte Datei:\n\n"
                                      + "\"" + verification + "\"", "Ergebnis", wx.OK | wx.ICON_EXCLAMATION)
                    else:
                        wx.MessageBox("Es wurden keine Fehler im Archiv gefunden!\n"
                                      "CRCs und Header sind einwandfrei.", "Ergebnis", wx.OK | wx.ICON_INFORMATION)
            except FileNotFoundError:
                del busy_cursor
                wx.MessageBox("Das Archiv \"" + self.path_to_opened_zip + "\"\nkonnte nicht gefunden werden.\n"
                              "Es wurde während der Bearbeitung gelöscht, verschoben oder umbenannt.", "Fehler",
                              wx.OK | wx.ICON_ERROR)

            except:
                del busy_cursor
                wx.MessageBox("Überprüfung fehlgeschlagen!\nDas bedeutet meistens, dass das Archiv fehlerhaft ist.\n\n"
                              + str(sys.exc_info()[1]), "Unerwarteter Fehler", wx.OK | wx.ICON_ERROR)

    @staticmethod
    def create_zip(evt):
        create_zip_dialog = CreateZipDialog(None, title="Neues Archiv",
                                            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        create_zip_dialog.ShowModal()

    def about_dialog(self, evt):
        about_info = wx.adv.AboutDialogInfo()
        about_info.SetName("PyZIP")
        about_info.SetVersion("1.0")
        about_info.SetIcon(images.PyZIP.GetIcon())
        about_info.SetDescription("Archivmanager\nfür Windows und Linux\nin Python mit wxPython")
        about_info.SetCopyright("(C) 2017 Franz Piontek")
        about_info.SetWebSite("https://github.com/FranzPio/PyZIP", "\u21E8  Programmwebsite")
        wx.adv.AboutBox(about_info)

    @staticmethod
    def under_development(evt):
        wx.MessageBox("Diese Funktionalität ist noch in Entwicklung!", "Beta-Version", wx.OK | wx.ICON_INFORMATION)


class CreateZipDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.files_to_zip = collections.OrderedDict()
        self.zip_destination = None
        self.zip_compression_method = zipfile.ZIP_STORED

        self.SetIcon(images.PyZIP.GetIcon())

        self.UI()
        self.Centre()
        self.SetMinSize((390, 330))
        self.SetSize((390, 330))
        self.Bind(wx.EVT_CLOSE, self.CloseDialog)
        self.Show()

    @staticmethod
    def CloseDialog(evt):
        if isinstance(evt.GetEventObject(), wx.Dialog):
            evt.GetEventObject().Destroy()
        elif isinstance(evt.GetEventObject(), wx.Button):
            evt.GetEventObject().GetParent().Destroy()

    def UI(self):
        if os.name != "posix":
            # noinspection PyArgumentList
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        self.SetFocus()
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.StaticBoxSizer(wx.HORIZONTAL, self, "1.  Dateien für das Archiv auswählen")
        hbox2 = wx.StaticBoxSizer(wx.HORIZONTAL, self, "2.  Kompressionsmethode wählen")
        hbox3 = wx.StaticBoxSizer(wx.HORIZONTAL, self, "3.  Speicherort wählen")
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        choose_files_button = wx.Button(self, label="Datei öffnen...")
        choose_files_button.Bind(wx.EVT_BUTTON, self.choose_files_dialog)
        choose_folders_button = wx.Button(self, label="Ordner öffnen...")
        choose_folders_button.Bind(wx.EVT_BUTTON, self.choose_folders_dialog)
        show_chosen_files_button = wx.Button(self, label="Auswahl anzeigen")
        show_chosen_files_button.Bind(wx.EVT_BUTTON, self.show_chosen_files_dialog)
        hbox1.Add(choose_files_button, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 10)
        hbox1.Add((2, -1))
        hbox1.Add(choose_folders_button, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        hbox1.Add((15, -1))
        hbox1.Add(show_chosen_files_button, 2, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 10)
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
        busy_cursor = wx.BusyCursor()
        file_dialog = wx.FileDialog(self, "Dateien auswählen", "", "", "",
                                    wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        for index, filename in enumerate(file_dialog.GetFilenames()):
            self.files_to_zip[filename] = file_dialog.GetPaths()[index]
        del busy_cursor

    def choose_folders_dialog(self, evt):
        busy_cursor = wx.BusyCursor()
        folder_dialog = wx.DirDialog(self, "Ordner auswählen", style=wx.DD_DIR_MUST_EXIST)
        if folder_dialog.ShowModal() == wx.ID_CANCEL:
            return
        for path, folders, files in os.walk(folder_dialog.GetPath()):
            for filename in files:
                self.files_to_zip[os.path.join(path, filename).replace(folder_dialog.GetPath(), "")]\
                    = os.path.join(path, filename)
        del busy_cursor

    def show_chosen_files_dialog(self, evt):
        if self.files_to_zip:
            dlg = wx.Dialog(None, title="Auswahl", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
            dlg.Bind(wx.EVT_CLOSE, self.CloseDialog)
            vbox = wx.BoxSizer(wx.VERTICAL)
            hbox1 = wx.BoxSizer(wx.HORIZONTAL)
            hbox2 = wx.BoxSizer(wx.HORIZONTAL)
            hbox3 = wx.BoxSizer(wx.HORIZONTAL)
            chosen_files_text = wx.StaticText(dlg, label="Ausgewählte Dateien und Ordner")
            hbox1.Add(chosen_files_text, 2, wx.EXPAND | wx.LEFT, 5)
            vbox.Add(hbox1, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)
            delete_all_button = wx.Button(dlg, label="Liste leeren")
            delete_all_button.Bind(wx.EVT_BUTTON, self.remove_all_from_zip)
            hbox2.Add(delete_all_button, 1, wx.EXPAND | wx.BOTTOM, 5)
            delete_files_button = wx.Button(dlg, label="Entfernen")
            delete_files_button.Bind(wx.EVT_BUTTON, self.remove_from_zip)
            hbox2.Add(delete_files_button, 1, wx.EXPAND | wx.BOTTOM | wx.LEFT, 5)
            vbox.Add(hbox2, 1, wx.EXPAND | wx.ALL, 10)
            self.chosen_files_list_box = wx.CheckListBox(dlg)
            busy_cursor = wx.BusyCursor()
            for file in self.files_to_zip.keys():
                self.chosen_files_list_box.Append(file)
            hbox3.Add(self.chosen_files_list_box, 1, wx.EXPAND)
            vbox.Add(hbox3, 3, wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, 10)
            self.chosen_files_list_box.SetFocus()
            dlg.SetSizer(vbox)
            dlg.SetMinSize((380, 270))
            dlg.SetSize((380, 270))
            del busy_cursor
            dlg.ShowModal()

    def remove_from_zip(self, evt):
        try:
            for checked_string in self.chosen_files_list_box.GetCheckedStrings():
                del self.files_to_zip[checked_string]
            while self.chosen_files_list_box.GetCheckedItems():
                self.chosen_files_list_box.Delete(self.chosen_files_list_box.GetCheckedItems()[0])
        except KeyError:
            pass

    def remove_all_from_zip(self, evt):
        confirmation = wx.MessageDialog(None, "Sind Sie sicher?\n\nListe wirklich löschen?",
                                        "Sicher?", style=wx.YES_NO | wx.ICON_EXCLAMATION)
        if confirmation.ShowModal() == wx.ID_YES:
            self.files_to_zip.clear()
            self.chosen_files_list_box.Clear()

    def choose_zip_destination(self, evt):
        file_extension = ".zip"
        wildcard = "ZIP-Archiv (*.zip) |*.zip"
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
                if os.path.isfile(self.zip_destination):
                    os.remove(self.zip_destination)
                busy_cursor = wx.BusyCursor()
                busy_info = wx.BusyInfo("Bitte warten,\nArchiv wird erstellt...")
                try:
                    with zipfile.ZipFile(self.zip_destination, "w", compression=self.zip_compression_method) as zip_file:
                        for filename, filepath in self.files_to_zip.items():
                            zip_file.write(filepath, filename)
                except FileNotFoundError:
                    del busy_info
                    del busy_cursor
                    wx.MessageBox("Mindestens eine Datei wurde während des Erstellens\n"
                                  "gelöscht, verschoben oder umbenannt.\n\n" + str(sys.exc_info()[1]), "Fehler",
                                  wx.OK | wx.ICON_ERROR)
                    os.remove(self.zip_destination)
                except:
                    del busy_info
                    del busy_cursor
                    wx.MessageBox("Erstellen des Archivs fehlgeschlagen!\n"
                                  "Eventuell gibt der Fehlercode weitere Informationen.\n\n"
                                  + str(sys.exc_info()[1]), "Unerwarteter Fehler", wx.OK | wx.ICON_ERROR)
                    os.remove(self.zip_destination)
                else:
                    del busy_info
                    del busy_cursor
                    wx.MessageBox("Archiv erfolgreich erstellt!", "Info", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("Kein Speicherort ausgewählt!", "Fehler", wx.OK | wx.ICON_EXCLAMATION)
        else:
            wx.MessageBox("Keine Dateien ausgewählt!", "Fehler", wx.OK | wx.ICON_EXCLAMATION)


strings = locales.Locale("de")

app = wx.App()
window = Application(None, title="PyZIP", size=(425, 350))
app.MainLoop()

