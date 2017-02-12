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
import threading
import time


class Time(threading.Thread):
    def __init__(self):
        super().__init__()
        self.start_time = time.time()

    def run(self):
        global is_creating
        while is_creating:
            mins, secs = divmod(round(time.time() - self.start_time, 2), 60)
            create_zip_dialog.time_text.SetLabel(strings.elapsed_time + "\n"
                                                 + str(int(mins)) + " min "
                                                 + str(int(secs)) + " s")
            time.sleep(0.05)

    def stop(self):
        global is_creating
        is_creating = False


class ProgressBar(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global is_creating
        with zipfile.ZipFile(create_zip_dialog.zip_destination, "w",
                             compression=create_zip_dialog.zip_compression_method) as zip_file:
            for filename, filepath in create_zip_dialog.files_to_zip.items():
                if is_creating:
                    create_zip_dialog.file_text.SetLabel(strings.file + "\n" + filename)
                    zip_file.write(filepath, filename)
                    wx.CallAfter(create_zip_dialog.update_progess, None)
                else:
                    return
        is_creating = False
        wx.MessageBox(strings.create_success_information, strings.information, wx.OK | wx.ICON_INFORMATION)

    def stop(self):
        global is_creating
        is_creating = False


class Application(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.InitLocale()

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
            wx.MessageBox(strings.archive_open_error + "\n\n" + str(sys.exc_info()[1]),
                          strings.unexpected_error, wx.OK | wx.ICON_ERROR)

    def CloseApp(self, evt):
        if self.archive_contents_olv.ItemCount > 0:
            confirmation = wx.MessageDialog(None, strings.are_you_sure + "\n\n" + strings.really_quit, strings.sure,
                                            style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_EXCLAMATION)
            if confirmation.ShowModal() == wx.ID_NO:
                return
        self.Destroy()

    def CloseDialog(self, evt):
        if isinstance(evt.GetEventObject(), wx.Dialog):
            evt.GetEventObject().Destroy()
        elif isinstance(evt.GetEventObject(), wx.Button):
            evt.GetEventObject().GetParent().Destroy()
        raise SystemExit(0)

    def InitLocale(self):
        global strings
        try:
            with open(os.path.join(os.path.expanduser("~"), ".pyzip_settings.ini"), "r") as settings_file:
                language = settings_file.read().split("=")[-1]
                if language in ("de", "en"):
                    strings = locales.Locale(language)
                else:
                    strings = locales.Locale("de")
                    os.remove(os.path.join(os.path.expanduser("~"), ".pyzip_settings.ini"))
                    with open(os.path.join(os.path.expanduser("~"), ".pyzip_settings.ini"), "w") as settings_file:
                        settings_file.write("language=de")
        except FileNotFoundError:
            # strings = locales.Locale("de")
            # with open(os.path.join(os.path.expanduser("~"), ".pyzip_settings.ini"), "w") as settings_file:
            #     settings_file.write("language=de")
            dlg = wx.Dialog(None, title=locales.Locale.choose_language)
            dlg.SetIcon(images.PyZIP.GetIcon())
            dlg.Bind(wx.EVT_CLOSE, self.CloseDialog)
            vbox = wx.BoxSizer(wx.VERTICAL)
            hbox1 = wx.BoxSizer(wx.HORIZONTAL)
            hbox2 = wx.BoxSizer(wx.HORIZONTAL)
            hbox3 = wx.BoxSizer(wx.HORIZONTAL)
            choose_language_text = wx.StaticText(dlg, label=locales.Locale.choose_language_for_PyZIP)
            hbox1.Add(choose_language_text, 1, wx.EXPAND)
            vbox.Add(hbox1, 1, wx.EXPAND | wx.ALL, 10)
            self.languages_drop_down = wx.Choice(dlg, choices=list(locales.Locale.LANGUAGES.keys()), style=wx.CB_SORT)
            hbox2.Add(self.languages_drop_down, 1, wx.EXPAND)
            vbox.Add(hbox2, 2, wx.EXPAND | wx.ALL, 10)
            ok_button = wx.Button(dlg, label=locales.Locale.okay)
            ok_button.Bind(wx.EVT_BUTTON, self.SetLocale)
            ok_button.SetDefault()
            hbox3.Add(ok_button, 1, wx.EXPAND | wx.RIGHT, 5)
            cancel_button = wx.Button(dlg, label=locales.Locale.cancel)
            cancel_button.Bind(wx.EVT_BUTTON, self.CloseDialog)
            hbox3.Add(cancel_button, 1, wx.EXPAND)
            vbox.Add(hbox3, 2, wx.EXPAND | wx.ALL, 10)
            dlg.SetSizer(vbox)
            dlg.SetMaxSize((260, 170))
            dlg.SetMinSize((260, 170))
            dlg.SetSize((260, 170))
            dlg.Centre()
            dlg.ShowModal()

    def SetLocale(self, evt):
        global strings
        busy_cursor = wx.BusyCursor()
        selection = self.languages_drop_down.GetStringSelection()
        strings = locales.Locale(locales.Locale.LANGUAGES[selection])
        with open(os.path.join(os.path.expanduser("~"), ".pyzip_settings.ini"), "w") as settings_file:
            settings_file.write("language=" + locales.Locale.LANGUAGES[selection])
        evt.GetEventObject().GetParent().Destroy()
        del busy_cursor

    def toolbar(self):
        toolbar = self.CreateToolBar(style=wx.TB_TEXT)
        open_archive_tool = toolbar.AddTool(wx.ID_OPEN, strings.open_tool_label, images.open_archive.GetBitmap(),
                                            strings.open_tool_shortHelp)
        toolbar.AddSeparator()
        extract_archive_tool = toolbar.AddTool(wx.ID_ANY, strings.extract_tool_label, images.extract_archive.GetBitmap(),
                                               strings.extract_tool_shortHelp)
        toolbar.AddSeparator()
        verify_archive_tool = toolbar.AddTool(wx.ID_ANY, strings.verify_tool_label, images.verify_archive.GetBitmap(),
                                              strings.verify_tool_shortHelp)
        toolbar.AddSeparator()
        create_archive_tool = toolbar.AddTool(wx.ID_NEW, strings.create_tool_label, images.new_archive.GetBitmap(),
                                              strings.create_tool_shortHelp)
        toolbar.AddSeparator()
        toolbar.AddStretchableSpace()
        about_info = toolbar.AddTool(wx.ID_ABOUT, strings.about_tool_label, images.about_info.GetBitmap(),
                                     strings.about_tool_shortHelp)
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
            olv.ColumnDefn(strings.filename_column, "right", valueGetter="filename", isSpaceFilling=True),
            olv.ColumnDefn(strings.size_column, "right", 80, "size", isSpaceFilling=False),
            olv.ColumnDefn(strings.changed_column, "right", 140, "changed", isSpaceFilling=False,
                           stringConverter="%d.%m.%Y")])
        # self.archive_contents_olv.AutoSizeColumns()
        self.archive_contents_olv.SetEmptyListMsg(strings.empty_list)
        self.archive_contents_olv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.open_archive_member)
        hbox1.Add(self.archive_contents_olv, 1, wx.EXPAND)
        vbox.Add(hbox1, 10, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        self.archive_member_count_text = wx.StaticText(self, label=strings.archive_member_count_0_files,
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
            wx.MessageBox(strings.unexpected_error + "\n\n" + str(sys.exc_info()[1]), strings.error,
                          wx.OK | wx.ICON_ERROR)

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
            self.archive_member_count_text.SetLabel(str(archive_member_count) + " " + strings.archive_member_count_files)
        except zipfile.BadZipFile:
            wx.MessageBox("\"" + filename_of_zip + "\" " + strings.invalid_archive,
                          strings.error, wx.OK | wx.ICON_EXCLAMATION)

    def open_zip(self, evt):
        file_dialog = wx.FileDialog(self, strings.choose_files_title, "", "", strings.wildcard_archives,
                                    wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
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
            self.archive_member_count_text.SetLabel(str(archive_member_count) + " " + strings.archive_member_count_files)
        except zipfile.BadZipFile:
            wx.MessageBox("\"" + filename_of_zip + "\" " + strings.invalid_archive_1 + " " + file_extension_of_zip
                          + strings.invalid_archive_2, strings.error, wx.OK | wx.ICON_EXCLAMATION)

    def extract_from_zip(self, evt):
        if self.archive_contents_olv.ItemCount == 0:
            pass  # MessageBox: no archive opened (???)
        else:
            file_dialog = wx.DirDialog(self, strings.choose_destination_title, "", wx.DD_DEFAULT_STYLE)
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
                wx.MessageBox(strings.file_not_found_error_1 + " \"" + self.path_to_opened_zip
                              + "\"\n" + strings.file_not_found_error_2 + "\n"
                              + strings.file_not_found_error_3, strings.error, wx.OK | wx.ICON_ERROR)
            except:
                wx.MessageBox(strings.extract_error + "\n" + strings.corrupted_error + "\n\n"
                              + str(sys.exc_info()[1]), strings.unexpected_error, wx.OK | wx.ICON_ERROR)
            else:
                wx.MessageBox(strings.extract_success_information, strings.information, wx.OK | wx.ICON_INFORMATION)

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
                        wx.MessageBox(strings.verify_warning_1 + "\n" + strings.verify_warning_2 + "\n\n"
                                      + "\"" + verification + "\"", strings.result, wx.OK | wx.ICON_EXCLAMATION)
                    else:
                        wx.MessageBox(strings.verify_information_1 + "\n"
                                      + strings.verify_information_2, strings.result, wx.OK | wx.ICON_INFORMATION)
            except FileNotFoundError:
                del busy_cursor
                wx.MessageBox(strings.file_not_found_error_1 + " \"" + self.path_to_opened_zip
                              + "\"\n" + strings.file_not_found_error_2 + "\n"
                              + strings.file_not_found_error_3, strings.error, wx.OK | wx.ICON_ERROR)

            except:
                del busy_cursor
                wx.MessageBox(strings.verify_error + "\n" + strings.corrupted_error + "\n\n"
                              + str(sys.exc_info()[1]), strings.unexpected_error, wx.OK | wx.ICON_ERROR)

    @staticmethod
    def create_zip(evt):
        global create_zip_dialog
        create_zip_dialog = CreateZipDialog(None, title=strings.create_zip_title,
                                            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        create_zip_dialog.ShowModal()

    def about_dialog(self, evt):
        about_info = wx.adv.AboutDialogInfo()
        about_info.SetName("PyZIP")
        about_info.SetVersion("1.0")
        about_info.SetIcon(images.PyZIP.GetIcon())
        about_info.SetDescription(strings.about_dialog_description_1 + "\n" + strings.about_dialog_description_2 + "\n"
                                  + strings.about_dialog_description_3)
        about_info.SetCopyright("(C) 2017 Franz Piontek")
        about_info.SetWebSite("https://github.com/FranzPio/PyZIP", strings.about_dialog_website_description)
        wx.adv.AboutBox(about_info)

    @staticmethod
    def under_development(evt):
        wx.MessageBox(strings.under_development, strings.beta_version, wx.OK | wx.ICON_INFORMATION)


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

    def CloseDialogStopThreads(self, evt):
        busy_cursor = wx.BusyCursor()
        busy_info = wx.BusyInfo(strings.please_wait + "...")
        self.progress_bar_thread.stop()
        self.time_thread.stop()
        self.progress_bar_thread.join()
        self.time_thread.join()
        os.remove(self.zip_destination)
        del busy_info
        del busy_cursor
        self.dlg.Destroy()
        wx.MessageBox(strings.cancelled_by_user, strings.information, wx.OK | wx.ICON_EXCLAMATION)

    def UI(self):
        if os.name != "posix":
            # noinspection PyArgumentList
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        self.SetFocus()
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.StaticBoxSizer(wx.HORIZONTAL, self, strings.create_zip_box_sizer_1)
        hbox2 = wx.StaticBoxSizer(wx.HORIZONTAL, self, strings.create_zip_box_sizer_2)
        hbox3 = wx.StaticBoxSizer(wx.HORIZONTAL, self, strings.create_zip_box_sizer_3)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        choose_files_button = wx.Button(self, label=strings.open_file)
        choose_files_button.Bind(wx.EVT_BUTTON, self.choose_files_dialog)
        choose_folders_button = wx.Button(self, label=strings.open_folder)
        choose_folders_button.Bind(wx.EVT_BUTTON, self.choose_folders_dialog)
        show_chosen_files_button = wx.Button(self, label=strings.show_selection)
        show_chosen_files_button.Bind(wx.EVT_BUTTON, self.show_chosen_files_dialog)
        hbox1.Add(choose_files_button, 1, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 10)
        hbox1.Add((2, -1))
        hbox1.Add(choose_folders_button, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        hbox1.Add((15, -1))
        hbox1.Add(show_chosen_files_button, 2, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 10)
        vbox.Add((-1, 10))
        vbox.Add(hbox1, 2, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        vbox.Add((-1, 10))
        compression_method_zip_stored_button = wx.RadioButton(self, label=strings.compression_method_zip_stored,
                                                              style=wx.RB_GROUP)
        compression_method_zip_stored_button.compression = zipfile.ZIP_STORED
        compression_method_zip_stored_button.Bind(wx.EVT_RADIOBUTTON, self.set_compression_method)
        compression_method_zip_deflated_button = wx.RadioButton(self, label=strings.compression_method_zip_deflated)
        compression_method_zip_deflated_button.compression = zipfile.ZIP_DEFLATED
        compression_method_zip_deflated_button.Bind(wx.EVT_RADIOBUTTON, self.set_compression_method)
        compression_method_zip_bzip2_button = wx.RadioButton(self, label=strings.compression_method_zip_bzip2)
        compression_method_zip_bzip2_button.compression = zipfile.ZIP_BZIP2
        compression_method_zip_bzip2_button.Bind(wx.EVT_RADIOBUTTON, self.set_compression_method)
        compression_method_zip_lzma_button = wx.RadioButton(self, label=strings.compression_method_zip_lzma)
        compression_method_zip_lzma_button.compression = zipfile.ZIP_LZMA
        compression_method_zip_lzma_button.Bind(wx.EVT_RADIOBUTTON, self.set_compression_method)
        hbox2.Add(compression_method_zip_stored_button, 1, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(compression_method_zip_deflated_button, 1, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(compression_method_zip_bzip2_button, 1, wx.EXPAND | wx.ALL, 5)
        hbox2.Add(compression_method_zip_lzma_button, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox2, 2, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        vbox.Add((-1, 10))
        zip_name_text = wx.StaticText(self, label=strings.zip_destination)
        self.zip_destination_textctrl = wx.TextCtrl(self, style=wx.TE_READONLY)
        choose_zip_destination_button = wx.Button(self, label="...", size=(30, -1))
        choose_zip_destination_button.Bind(wx.EVT_BUTTON, self.choose_zip_destination)
        hbox3.Add(zip_name_text, 2, wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, 10)
        hbox3.AddSpacer(20)
        hbox3.Add(self.zip_destination_textctrl, 6, wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM, 10)
        hbox3.Add(choose_zip_destination_button, 1, wx.EXPAND | wx.RIGHT | wx.TOP | wx.BOTTOM, 10)
        vbox.Add(hbox3, 2, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        vbox.Add((-1, 20))
        create_zip_button = wx.Button(self, label=strings.create_archive)
        create_zip_button.Bind(wx.EVT_BUTTON, self.create_zip)
        close_button = wx.Button(self, label=strings.close)
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
        file_dialog = wx.FileDialog(self, strings.choose_files_title, "", "", "",
                                    wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        for index, filename in enumerate(file_dialog.GetFilenames()):
            self.files_to_zip[filename] = file_dialog.GetPaths()[index]
        del busy_cursor

    def choose_folders_dialog(self, evt):
        busy_cursor = wx.BusyCursor()
        folder_dialog = wx.DirDialog(self, strings.choose_folder_title, style=wx.DD_DIR_MUST_EXIST)
        if folder_dialog.ShowModal() == wx.ID_CANCEL:
            return
        for path, folders, files in os.walk(folder_dialog.GetPath()):
            for filename in files:
                self.files_to_zip[os.path.join(path, filename).replace(folder_dialog.GetPath(), "")]\
                    = os.path.join(path, filename)
        del busy_cursor

    def show_chosen_files_dialog(self, evt):
        if self.files_to_zip:
            dlg = wx.Dialog(None, title=strings.selection, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
            dlg.Bind(wx.EVT_CLOSE, self.CloseDialog)
            vbox = wx.BoxSizer(wx.VERTICAL)
            hbox1 = wx.BoxSizer(wx.HORIZONTAL)
            hbox2 = wx.BoxSizer(wx.HORIZONTAL)
            hbox3 = wx.BoxSizer(wx.HORIZONTAL)
            chosen_files_text = wx.StaticText(dlg, label=strings.chosen_files)
            hbox1.Add(chosen_files_text, 2, wx.EXPAND | wx.LEFT, 5)
            vbox.Add(hbox1, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)
            delete_all_button = wx.Button(dlg, label=strings.clear_list)
            delete_all_button.Bind(wx.EVT_BUTTON, self.remove_all_from_zip)
            hbox2.Add(delete_all_button, 1, wx.EXPAND | wx.BOTTOM, 5)
            delete_files_button = wx.Button(dlg, label=strings.remove)
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
        confirmation = wx.MessageDialog(None, strings.are_you_sure + "\n\n" + strings.really_clear_list,
                                        strings.sure, style=wx.YES_NO | wx.ICON_EXCLAMATION)
        if confirmation.ShowModal() == wx.ID_YES:
            self.files_to_zip.clear()
            self.chosen_files_list_box.Clear()

    def choose_zip_destination(self, evt):
        file_extension = ".zip"
        file_dialog = wx.FileDialog(self, strings.choose_destination_title, "", "", strings.wildcard_zip,
                                    wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        path_to_zip = file_dialog.GetPath()
        self.zip_destination = path_to_zip if path_to_zip.endswith(file_extension) else path_to_zip + file_extension
        self.zip_destination_textctrl.SetValue(self.zip_destination)

    def update_progess(self, msg):
        self.count += 1
        if self.count >= PROGRESS_RANGE:
            self.dlg.Destroy()
            return
        self.progress.SetValue(self.count)

    def create_zip(self, evt):
        global PROGRESS_RANGE
        global is_creating
        if self.files_to_zip:
            if self.zip_destination:
                if os.path.isfile(self.zip_destination):
                    os.remove(self.zip_destination)
                # busy_cursor = wx.BusyCursor()
                # busy_info = wx.BusyInfo(strings.please_wait + ",\n" + strings.busy_info)
                try:
                    PROGRESS_RANGE = len(self.files_to_zip.keys())
                    self.dlg = wx.Dialog(None, title=strings.progress)
                    self.dlg.Bind(wx.EVT_CLOSE, self.CloseDialogStopThreads)
                    self.count = 0
                    vbox = wx.BoxSizer(wx.VERTICAL)
                    hbox1 = wx.BoxSizer(wx.HORIZONTAL)
                    hbox2 = wx.StaticBoxSizer(wx.HORIZONTAL, self.dlg, strings.informations)
                    hbox3 = wx.BoxSizer(wx.HORIZONTAL)
                    archive_creation_text = wx.StaticText(self.dlg, label=strings.please_wait + ", "
                                                          + strings.busy_info)
                    hbox1.Add(archive_creation_text, 1, wx.EXPAND | wx.TOP | wx.RIGHT, 5)
                    vbox.Add(hbox1, 1, wx.EXPAND | wx.ALL, 10)
                    self.time_text = wx.StaticText(self.dlg, label=strings.elapsed_time + "\n0 min 0 s")
                    hbox2.Add(self.time_text, 1, wx.EXPAND | wx.RIGHT, 20)
                    self.file_text = wx.StaticText(self.dlg, label=strings.file + "\n", style=wx.ST_ELLIPSIZE_MIDDLE)
                    hbox2.Add(self.file_text, 2, wx.EXPAND)
                    vbox.Add(hbox2, 2, wx.EXPAND | wx.ALL, 10)
                    vbox.Add((-1, 15))
                    self.progress = wx.Gauge(self.dlg, range=PROGRESS_RANGE)
                    hbox3.Add(self.progress, 1, wx.EXPAND | wx.BOTTOM, 10)
                    vbox.Add(hbox3, 2, wx.EXPAND | wx.ALL, 10)
                    self.dlg.SetSizer(vbox)
                    self.dlg.SetSize((350, 225))
                    is_creating = True
                    self.progress_bar_thread = ProgressBar()
                    self.progress_bar_thread.start()
                    self.time_thread = Time()
                    self.time_thread.start()
                    self.dlg.ShowModal()
                except FileNotFoundError:
                    # del busy_info
                    # del busy_cursor
                    wx.MessageBox(strings.file_not_found_error_1_1 + "\n" + strings.file_not_found_error_1_2 + "\n\n"
                                  + str(sys.exc_info()[1]), strings.error, wx.OK | wx.ICON_ERROR)
                    os.remove(self.zip_destination)
                except:
                    # del busy_info
                    # del busy_cursor
                    wx.MessageBox(strings.create_error + "\n" + strings.error_code + "\n\n"
                                  + str(sys.exc_info()[1]), strings.unexpected_error, wx.OK | wx.ICON_ERROR)
                    os.remove(self.zip_destination)
                else:
                    # del busy_info
                    # del busy_cursor
                    pass
            else:
                wx.MessageBox(strings.no_destination_chosen, strings.error, wx.OK | wx.ICON_EXCLAMATION)
        else:
            wx.MessageBox(strings.no_files_to_zip_chosen, strings.error, wx.OK | wx.ICON_EXCLAMATION)


if __name__ == "__main__":
    app = wx.App()
    window = Application(None, title="PyZIP", size=(425, 350))
    app.MainLoop()
