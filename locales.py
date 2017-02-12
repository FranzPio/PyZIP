# 'locales.py'
#  contains language-specific strings for all the texts, labels, messages etc. in PyZIP


class Locale:

    LANGUAGES = {"Deutsch": "de", "English": "en"}
    choose_language = "Sprache auswählen"
    choose_language_for_PyZIP = "Bitte wählen Sie eine Sprache für PyZIP aus:"
    okay = "OK"
    cancel = "Abbrechen"

    def __init__(self, language):
        if language == "de":
            # errors
            self.error = "Fehler"
            self.unexpected_error = "Unerwarteter Fehler"
            self.archive_not_existing_error = "Archiv existiert nicht"
            self.archive_open_error = "Öffnen des Archivs fehlgeschlagen"
            self.invalid_archive = "ist keine gültige Archivdatei oder sie ist beschädigt!"
            self.invalid_archive_1 = "ist keine gültige"
            self.invalid_archive_2 = "-Datei oder sie ist beschädigt!"
            self.file_not_found_error_1 = "Das Archiv"
            self.file_not_found_error_2 = "konnte nicht gefunden werden."
            self.file_not_found_error_3 = "Es wurde während der Bearbeitung gelöscht, verschoben oder umbenannt."
            self.file_not_found_error_1_1 = "Mindestens eine Datei wurde während des Erstellens"
            self.file_not_found_error_1_2 = "gelöscht, verschoben oder umbenannt."
            self.extract_error = "Extrahieren fehlgeschlagen!"
            self.verify_error = "Überprüfung fehlgeschlagen!"
            self.corrupted_error = "Das bedeutet meistens, dass das Archiv fehlerhaft ist."
            self.create_error = "Erstellen des Archivs fehlgeschlagen!"
            self.error_code = "Eventuell gibt der Fehlercode weitere Informationen."
            self.verify_warning_1 = "Es wurde mindestens ein Fehler im Archiv gefunden!"
            self.verify_warning_2 = "Erste fehlerhafte Datei"
            self.no_destination_chosen = "Kein Speicherort ausgewählt!"
            self.no_files_to_zip_chosen = "Keine Dateien ausgewählt!"
            self.cancelled_by_user = "Aktion durch Benutzer abgebrochen!"

            # information
            self.information = "Info"
            self.extract_success_information = "Dateien erfolgreich extrahiert!"
            self.create_success_information = "Archiv erfolgreich erstellt!"
            self.verify_information_1 = "Es wurden keine Fehler im Archiv gefunden!"
            self.verify_information_2 = "CRCs und Header sind einwandfrei."

            # phrases
            self.sure = "Sicher?"
            self.are_you_sure = "Sind Sie sicher?"
            self.really_quit = "PyZIP wirklich beenden?"
            self.really_clear_list = "Liste wirklich löschen?"
            self.please_wait = "Bitte warten"
            self.busy_info = "Archiv wird erstellt..."
            self.close = "Schließen"
            self.result = "Ergebnis"

            # toolbar
            self.open_tool_label = "Öffnen"
            self.open_tool_shortHelp = "Bestehendes Archiv öffnen"
            self.extract_tool_label = "Extrahieren"
            self.extract_tool_shortHelp = "Ausgewählte Dateien extrahieren"
            self.verify_tool_label = "Überprüfen"
            self.verify_tool_shortHelp = "Archiv überprüfen (CRC, Header)"
            self.create_tool_label = "Erstellen"
            self.create_tool_shortHelp = "Neues Archiv erstellen"
            self.about_tool_label = "Info"
            self.about_tool_shortHelp = "Über PyZIP"

            # ListCtrl
            self.filename_column = "Dateiname"
            self.size_column = "Größe"
            self.changed_column = "Änderungsdatum"
            self.empty_list = "Kein Archiv ausgewählt"
            
            self.archive_member_count_0_files = "0 Dateien"
            self.archive_member_count_files = "Dateien"

            # file dialogs
            self.wildcard_archives = "Archivdateien|*.zip;*.bz2;*.xz;*.lzma"
            self.wildcard_zip = "ZIP-Archiv (*.zip) |*.zip"
            self.choose_files_title = "Dateien auswählen"
            self.choose_folder_title = "Ordner auswählen"
            self.choose_destination_title = "Speicherort auswählen"

            # about dialog
            self.about_dialog_description_1 = "Archivmanager"
            self.about_dialog_description_2 = "für Windows und Linux"
            self.about_dialog_description_3 = "in Python mit wxPython"
            self.about_dialog_website_description = "\u21E8  Programmwebsite"

            # under development dialog
            self.under_development = "Diese Funktionalität ist noch in Entwicklung!"
            self.beta_version = "Beta-Version"

            # create archive dialog
            self.create_zip_title = "Neues Archiv"
            self.create_zip_box_sizer_1 = "1.  Dateien für das Archiv auswählen"
            self.create_zip_box_sizer_2 = "2.  Kompressionsmethode wählen"
            self.create_zip_box_sizer_3 = "3.  Speicherort wählen"
            self.open_file = "Datei öffnen..."
            self.open_folder = "Ordner öffnen..."
            self.selection = "Auswahl"
            self.show_selection = "Auswahl anzeigen"
            self.chosen_files = "Ausgewählte Dateien und Ordner"
            self.clear_list = "Liste leeren"
            self.remove = "Entfernen"
            self.compression_method_zip_stored = "ZIP"
            self.compression_method_zip_deflated = "ZIP (komprimiert)"
            self.compression_method_zip_bzip2 = "BZIP2"
            self.compression_method_zip_lzma = "LZMA"
            self.zip_destination = "Speicherort:"
            self.create_archive = "Archiv erstellen"

            self.progress = "Fortschritt"
            self.informations = "Informationen"
            self.elapsed_time = "Verstrichene Zeit:"
            self.file = "Datei:"

        elif language == "en":
            # errors
            self.error = "Error"
            self.unexpected_error = "Unexpected error"
            self.archive_not_existing_error = "Archive doesn't exist"
            self.archive_open_error = "Opening archive failed"
            self.invalid_archive = "is either not a valid archive or it is corrupted."
            self.invalid_archive_1 = "is either not a valid"
            self.invalid_archive_2 = " file or it is corrupted."
            self.file_not_found_error_1 = "The archive"
            self.file_not_found_error_2 = "cannot be found."
            self.file_not_found_error_3 = "It was deleted, moved or renamed while viewing."
            self.file_not_found_error_1_1 = "During creation at least one file"
            self.file_not_found_error_1_2 = "was deleted, moved or renamed."
            self.extract_error = "Extraction failed!"
            self.verify_error = "Verification failed!"
            self.corrupted_error = "In most cases this means that the archive is corrupted."
            self.create_error = "Creating the archive failed!"
            self.error_code = "This error code may provide further information."
            self.verify_warning_1 = "At least one defect found."
            self.verify_warning_2 = "First bad file"
            self.no_destination_chosen = "No destination folder specified!"
            self.no_files_to_zip_chosen = "No files selected!"
            self.cancelled_by_user = "Action cancelled by user."

            # information
            self.information = "Information"
            self.extract_success_information = "Files were extracted successfully!"
            self.create_success_information = "Archive created successfully!"
            self.verify_information_1 = "No bad files found!"
            self.verify_information_2 = "CRCs and file headers are OK."

            # phrases
            self.sure = "Really?"
            self.are_you_sure = "Are you sure?"
            self.really_quit = "Really quit PyZIP?"
            self.really_clear_list = "Really clear list?"
            self.please_wait = "Please wait"
            self.busy_info = "archive is being created..."
            self.close = "Cancel"
            self.result = "Result"

            # toolbar
            self.open_tool_label = "Open"
            self.open_tool_shortHelp = "Open existing archive"
            self.extract_tool_label = "Extract"
            self.extract_tool_shortHelp = "Extract selected files"
            self.verify_tool_label = "Verify"
            self.verify_tool_shortHelp = "Verify archive (CRCs, file headers)"
            self.create_tool_label = "Create"
            self.create_tool_shortHelp = "Create new archive"
            self.about_tool_label = "About"
            self.about_tool_shortHelp = "About PyZIP"

            # ListCtrl
            self.filename_column = "Filename"
            self.size_column = "Size"
            self.changed_column = "Last changed"
            self.empty_list = "No archive opened"

            self.archive_member_count_0_files = "0 files"
            self.archive_member_count_files = "files"

            # file dialogs
            self.wildcard_archives = "Archives|*.zip;*.bz2;*.xz;*.lzma"
            self.wildcard_zip = "ZIP archive (*.zip) |*.zip"
            self.choose_files_title = "Select files"
            self.choose_folder_title = "Select folders"
            self.choose_destination_title = "Choose destination folder"

            # about dialog
            self.about_dialog_description_1 = "Archive manager"
            self.about_dialog_description_2 = "for Windows and Linux"
            self.about_dialog_description_3 = "using Python and wxPython"
            self.about_dialog_website_description = "\u21E8  Program website"

            # under development dialog
            self.under_development = "This functionality is being developed actively."
            self.beta_version = "Not available yet"

            # create archive dialog
            self.create_zip_title = "New archive"
            self.create_zip_box_sizer_1 = "1.  Select files to include"
            self.create_zip_box_sizer_2 = "2.  Choose compression method"
            self.create_zip_box_sizer_3 = "3.  Choose destination folder"
            self.open_file = "Open file..."
            self.open_folder = "Open folder..."
            self.selection = "Selection"
            self.show_selection = "Show selected"
            self.chosen_files = "Selected files and folders"
            self.clear_list = "Clear list"
            self.remove = "Remove"
            self.compression_method_zip_stored = "ZIP"
            self.compression_method_zip_deflated = "ZIP (compressed)"
            self.compression_method_zip_bzip2 = "BZIP2"
            self.compression_method_zip_lzma = "LZMA"
            self.zip_destination = "Destination:"
            self.create_archive = "Create archive"

            self.progress = "Progress"
            self.informations = "Information"
            self.elapsed_time = "Elapsed time:"
            self.file = "File:"

        else:
            try:
                import wx
                app = wx.App()
                wx.MessageBox("\"" + language + "\" language is not available!", "Unexpected error",
                              style=wx.OK | wx.ICON_ERROR)
                del app
            finally:
                raise SystemExit("Error: \"" + language + "\" language is not available!\n"
                                 + "PyZIP could not be executed correctly.\n\n"
                                 + "Contact the developer: https://github.com/FranzPio/PyZIP")
