class Locale:

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

            # informations
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

        elif language == "en":
            return
