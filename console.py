import json
import os
import requests
import sys
import time

from openpyxl import load_workbook

import console_assistance as CA
import savedata_manager as SDM
import notification_sound_player as NSP

# system variables
headline_already_printed = False

auto_update = SDM.get_auto_update()
term_output_diplomacy = SDM.get_term_output_diplomacy()
oneline_output_format = SDM.get_one_line_output()
headline_printing = SDM.get_headline_printing()
alphabetical_output, abc_output_ascending = SDM.get_alphabetical_output()
auto_scan_filters = SDM.get_auto_scan_filters()
output_detail_level = SDM.get_output_detail_level()


def set_system_variables_to_default():
    global auto_scan_filters

    SDM.set_auto_update(1)
    SDM.set_term_output_diplomacy(3)
    SDM.set_one_line_output(1)
    SDM.set_headline_printing(2)
    SDM.set_alphabetical_output(True, True)
    SDM.set_auto_scan_filters("Noun,Verb,Adjective,Adverb,Preposition,Phrase")
    SDM.set_output_detail_level(3)


def check_paths():
    global auto_update
    time.sleep(2)

    os.system('cls')
    # For configuring M2E for other base systems:
    # os.system('cls' if os.name == 'nt' else 'clear')

    CA.print_opening(version="3.0c")
    print("\n\tChecking database status...")
    time.sleep(1)

    if not os.path.exists("src/database/wiki_morph.json"):
        SDM.set_current_size()
        try:
            url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
            response = requests.get(url, stream=True)
            remote_size = int(response.headers.get("Content-Length", 0))
            remote_size = int(remote_size / (1024 * 1024))

            os.system('cls')
            CA.print_opening(version="3.0c")
            print("\n\t\033[91mWarning:\033[0m wiki_morph database could not be found on your system!"
                  "\n\tYou have the option to download it automatically.")
            if remote_size == 0:
                print("\n\tSize of file: unknown")
            else:
                print("\tSize of file: " + str(remote_size) + "MB")
            print("\tDo you want to download it now? (y/n)")
            answer = input("\n\tanswer: ")

            if answer == "y":

                SDM.set_download_size(remote_size)

                normal = CA.download_database(url=url)

                if normal:
                    current_size = os.path.getsize("src/database/wiki_morph.json")
                    current_size = int(current_size / (1024 * 1024))
                    SDM.set_current_size(current_size)
                    auto_update = False
                    os.system('cls')
                    CA.print_opening(version="3.0c")
                    print("\n\n\t\033[32mDownload completed!\033[0m (" + str(current_size) + " MB)"
                          "\n\n\tDo you wish to search for terms now? (y/n)")
                    answer = input("\n\tanswer: ")
                    if answer == "n":
                        print("\n\tProgram will now terminate.")
                        time.sleep(3)
                        os.system('cls')
                        sys.exit(0)
                else:
                    sys.exit()

            else:
                CA.print_exit_without_download()
            time.sleep(1)
        except Exception:
            os.system('cls')
            CA.print_opening(version="3.0c")
            print("\n\t\033[91mWarning:\033[0m Database is not installed currently."
                  "\n\n\tThis program offers the possibility to download the database automatically."
                  "\n\tBut for the moment there was \033[91mno internet connection\033[0m recognized."
                  "\n\tPlease make sure you are connected and restart the program."
                  "\n\tThe program will now terminate.")
            time.sleep(15)
            os.system('cls')
            sys.exit(0)

    else:
        os.system('cls')
        current_size = os.path.getsize("src/database/wiki_morph.json")
        current_size = int(current_size / (1024 * 1024))
        soll_size = SDM.get_soll_size()

        if current_size < soll_size:
            CA.print_opening(version="3.0c")
            print("\n\t\033[91mWarning:\033[0m the local database file does not cover the expected amount of "
                  "information!"
                  "\n\n\t(Expected size: min. " + str(soll_size) + " MB)"
                  "\n\t(Local size: " + str(current_size) + " MB)"
                  "\n\n\tThis may be due to an interruption during the last downloading process."
                  "\n\tTo solve this problem you should reinstall the database by downloading it again."
                  "\n\tDo you want to start the download now? (y/n)")
            answer = input("\n\tanswer: ")

            if answer == "y":

                SDM.set_current_size()
                url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
                response = requests.get(url, stream=True)
                remote_size = int(response.headers.get("Content-Length", 0))
                remote_size = int(remote_size / (1024 * 1024))

                SDM.set_download_size(remote_size)
                CA.download_database(url=url)
                NSP.play_mp3("./src/data/GUI_sound/Signal.mp3")

                current_size = os.path.getsize("src/database/wiki_morph.json")
                current_size = int(current_size / (1024 * 1024))
                SDM.set_current_size(current_size)
                auto_update = False
                os.system('cls')
                CA.print_opening(version="3.0c")
                print("\n\n\t\033[32mDownload completed!\033[0m (" + str(current_size) + " MB)"
                      "\n\n\tDo you wish to search for terms now? (y/n)")
                answer = input("\n\tanswer: ")
                if answer == "n":
                    print("\n\tProgramm will now terminate.")
                    time.sleep(3)
                    sys.exit(0)

            else:
                CA.print_exit_without_download()
        else:
            CA.print_opening(version="3.0c")
            print("\n\t\033[32mDatabase installed and available.\033[0m")
        time.sleep(3)


def check_for_updates():
    os.system('cls')
    CA.print_opening(version="3.0c")
    print("\n\tChecking for wiki_morph updates...")
    time.sleep(3)

    current_size = SDM.get_current_size()

    try:
        url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        response = requests.get(url, stream=True, headers=headers, allow_redirects=True)
        remote_size = int(response.headers.get("Content-Length", 0))
        remote_size = int(remote_size / (1024 * 1024))
        print("\tResponse Status Code:", "\033[91m", response.status_code, "\033[0m")
        time.sleep(2)

        if remote_size == 0:
            os.system('cls')
            CA.print_opening(version="3.0c")
            print("\n\tUpdate check not possible: \033[91mServer does not provide required information!\033[0m"
                  "\n\tLast recent locally installed version will be used.")
            time.sleep(7)
        else:
            if current_size < remote_size:
                os.system('cls')
                CA.print_opening(version="3.0c")
                print("\n\tThere is a new version of wiki_morph available!"
                      "\n\n\tSize: " + str(remote_size) + " MB"
                      "\n\n\t Do you want to download the update now? (y/n)")
                answer = input("\n\tanswer: ")
                if answer == "y":
                    SDM.set_download_size(remote_size)
                    CA.download_database(url=url)

                    os.system('cls')
                    CA.print_opening(version="3.0c")
                    print("\n\n\tUpdate completed! (" + str(current_size) + " MB)"
                          "\n\n\tDo you wish to search for terms now? (y/n)")
                    answer = input("\n\tanswer: ")
                    if answer == "n":
                        print("\n\tProgramm will now terminate.")
                        time.sleep(3)
                        sys.exit(0)
            else:
                os.system('cls')
                CA.print_opening(version="3.0c")
                print("\n\tThe installed database is up to date!")
                time.sleep(3)
    except Exception as e:
        CA.print_opening(version="3.0c")
        print("\n\tUpdate check not possible: No internet connection!"
              "\n\tLast recent locally installed version will be used.")
        print("Exception:", e)
        time.sleep(5)


def search_for_terms(log_title, workbook_title):
    global headline_already_printed
    print_opening_again = False

    global auto_update
    global term_output_diplomacy
    global oneline_output_format
    global headline_printing
    global alphabetical_output
    global abc_output_ascending
    global auto_scan_filters
    global output_detail_level

    open_excel_automatically = False

    # loading database
    os.system('cls')
    CA.print_opening(version="3.0c")
    print("\n\tLoading wiki_morph database...")
    with open("src/database/wiki_morph.json", "r", encoding="utf-8") as f:
        entries_list = json.load(f)
    CA.print_main_menu(version="3.0c")

    # search function
    stop = False
    excel_row = 1
    workbook = load_workbook(workbook_title)
    worksheet = workbook.active

    while not stop:

        if print_opening_again:
            CA.print_main_menu(version="3.0c")
            print_opening_again = False
        i = input("\n\tSearch term: ").lower()
        os.system('cls')

        if i == "exit!":
            print("\033[93m" + "\n\tProgram terminated!\033[0m")
            time.sleep(1)
            os.system('cls')
            stop = True
            if open_excel_automatically:
                os.system(f'start "" {workbook_title}')
        elif i == "i!":
            CA.show_instructions()
            time.sleep(3)
            CA.print_main_menu(version="3.0c")
        elif i == "v!":
            CA.show_version_description()
            i = input()
            CA.print_main_menu(version="3.0c")
        elif i == "?":
            CA.print_main_menu(version="3.0c")

        # AUTOMATIC SCAN MODE ------------------------------------------------------------------------------------------
        elif i == "s!":

            if excel_row == 1:
                worksheet, excel_row = CA.print_headlines(worksheet, excel_row, output_detail_level)
                headline_already_printed = True

            open_excel_automatically = True
            os.system('cls')
            print("\n\t\033[38;5;130m- Automatic scan mode -\033[0m"
                  "\n\n\tPlease select an excel file to scan for possible terms.")
            time.sleep(1.5)
            file = CA.select_excel_file()
            start_time = time.time()
            terms, invalid_cases = CA.autoscan(file, duplicates=True, abc=alphabetical_output, abc_ascending=abc_output_ascending)
            end_time = time.time()
            number_of_terms = len(terms) + len(invalid_cases)
            number_of_valid_cases = len(terms)
            status = "\n\t\033[38;5;130m- Automatic scan mode -\033[0m" \
                     "\n\n\tExcel file: " + file +\
                     "\n\tFound terms: " + str(number_of_terms) +\
                     "\n\tValid cases: " + str(number_of_valid_cases) +\
                     "\n\tPos filters: " + str(auto_scan_filters)

            time.sleep(1)
            os.system('cls')
            print(status)
            print("\n\t", CA.measure_time(start_time, end_time, search=False))
            time.sleep(3)
            if not invalid_cases == []:
                print("\n\t\033[91mWarning:\033[0m Scanned file contains terms that are invalid inputs!"
                      "\n\n\tFor searching within the wikimorph database the following terms will be ignored:"
                      "\n\t\t", str(invalid_cases))
                input("\n\tType in anything to start the search: ")
            print("\n\t\033[92mThe valid terms will now be searched in the database.\033[0m")
            time.sleep(3)

            # for preventing double headline printing at the beginning of the Excel
            # only executes the "for every new doc" headline printing
            # the headline printing for every term in case hlp == 3 is defined below
            if headline_printing == 2 and not headline_already_printed:
                worksheet, excel_row = CA.print_headlines(worksheet, excel_row, output_detail_level)
                headline_already_printed = True

            start_time = time.time()
            log = open(log_title, "a", encoding="utf-8")
            if term_output_diplomacy == 1:
                for x in range(number_of_valid_cases):
                    term = terms[x]
                    os.system('cls')
                    progress = format(100*(x/number_of_valid_cases), ".2f")
                    print(status)
                    print("\n\t\033[38;5;130mSearching for terms...\033[0m"
                          "\n\tCurrent term: " + term + "\t\tProgress: " + str(progress) + "%")

                    worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                            excel_row=excel_row,
                                                                            pos_filters=auto_scan_filters,
                                                                            term=term,
                                                                            entries_list=entries_list,
                                                                            only_found_terms=True,
                                                                            only_not_found_terms=False,
                                                                            multiline_output=not oneline_output_format,
                                                                            output_detail_level=output_detail_level,
                                                                            headline_printing=headline_printing,
                                                                            hap=headline_already_printed)
                    progress = int(50*(x/number_of_valid_cases))
                    progressbar = ("\t[" + "-" * (progress-1) + ">" + " " * (50-(progress+1)) + "]")
                    print(progressbar)

                    log.write("\n\n" + log_output)
                    headline_already_printed = False

            elif term_output_diplomacy == 2:
                for x in range(number_of_valid_cases):
                    term = terms[x]
                    os.system('cls')
                    progress = format(100 * (x / number_of_valid_cases), ".2f")
                    print(status)
                    print("\n\t\033[38;5;130mSearching for terms...\033[0m"
                          "\n\tCurrent term: " + term + "\t\tProgress: " + str(progress) + "%")

                    worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                            excel_row=excel_row,
                                                                            pos_filters=auto_scan_filters,
                                                                            term=term,
                                                                            entries_list=entries_list,
                                                                            only_found_terms=False,
                                                                            only_not_found_terms=True,
                                                                            multiline_output=not oneline_output_format,
                                                                            output_detail_level=output_detail_level,
                                                                            headline_printing=headline_printing,
                                                                            hap=headline_already_printed)
                    progress = int(50 * (x / number_of_valid_cases))
                    progressbar = ("\t[" + "-" * (progress - 1) + ">" + " " * (50 - (progress + 1)) + "]")
                    print(progressbar)

                    log.write("\n\n" + log_output)
                    headline_already_printed = False

            else:
                for x in range(number_of_valid_cases):
                    term = terms[x]
                    os.system('cls')
                    progress = format(100 * (x / number_of_valid_cases), ".2f")
                    print(status)
                    print("\n\t\033[38;5;130mSearching for terms...\033[0m"
                          "\n\tCurrent term: " + term + "\t\tProgress: " + str(progress) + "%")

                    worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                            excel_row=excel_row,
                                                                            pos_filters=auto_scan_filters,
                                                                            term=term,
                                                                            entries_list=entries_list,
                                                                            only_found_terms=False,
                                                                            only_not_found_terms=False,
                                                                            multiline_output=not oneline_output_format,
                                                                            output_detail_level=output_detail_level,
                                                                            headline_printing=headline_printing,
                                                                            hap=headline_already_printed)
                    progress = int(50 * (x / number_of_valid_cases))
                    progressbar = ("\t[" + "-" * (progress - 1) + ">" + " " * (50 - (progress + 1)) + "]")
                    print(progressbar)

                    log.write("\n\n" + log_output)
                    headline_already_printed = False

            log.close()
            workbook.save(workbook_title)
            end_time = time.time()
            os.system('cls')
            print(status)
            print("\n\t\033[92mProcess finished!\033[0m"
                  "\n\n\t", CA.measure_time(start_time, end_time))
            time.sleep(6)
            os.system('cls')
            print(status)
            print("\n\t\033[92mProcess finished!\033[0m"
                  "\n\n\t", CA.measure_time(start_time, end_time),
                  "\n\n\tResults were saved."
                  "\n\tReturning to manual search mode...")
            time.sleep(4)
            os.system('cls')
            NSP.play_mp3("./src/data/GUI_sound/Signal.mp3")

        # COMPARISON MODE ----------------------------------------------------------------------------------------------
        elif i == "c!":
            open_excel_automatically = False
            os.system('cls')
            status = "\n\t\033[94m- Comparison mode -\033[0m"
            print(status)
            print("\n\tPlease select two excel files you want to compare.")
            time.sleep(3)
            print("\n\tSelect excel file 1 now.")
            time.sleep(3)
            file_1 = CA.select_excel_file()
            terms_1, invalid_terms_1 = CA.autoscan(file_1)
            number_of_terms_1 = len(terms_1)
            print("\n\tSelected file 1: " + file_1)
            print("\tFound terms: " + str(number_of_terms_1))
            if not invalid_terms_1 == []:
                print("\n\t\033[91mWarning:\033[0m Scanned file contains terms that are invalid inputs!"
                      "\n\n\tFor searching within the wikimorph database the following terms will be ignored:"
                      "\n\t\t", str(invalid_terms_1))
                input("\n\tType in anything to continue: ")
            time.sleep(4)

            os.system('cls')
            print(status)
            print("\n\tSelect excel file 2 now.")
            time.sleep(3)
            file_2 = CA.select_excel_file()
            terms_2, invalid_terms_2 = CA.autoscan(file_2)
            number_of_terms_2 = len(terms_2)
            print("\n\tSelected file 2: " + file_2)
            print("\tFound terms: " + str(number_of_terms_2))
            if not invalid_terms_2 == []:
                print("\n\t\033[91mWarning:\033[0m Scanned file contains terms that are invalid inputs!"
                      "\n\n\tFor searching within the wikimorph database the following terms will be ignored:"
                      "\n\t\t", str(invalid_terms_2))
                input("\n\tType in anything to continue: ")
            time.sleep(4)

            os.system('cls')
            print(status)
            print("\n\tPreparing comparison...")
            unique_terms_1 = []
            unique_terms_2 = []
            common_terms = []

            for x in range(number_of_terms_1):
                term = terms_1[x]
                progress = format(100 * ((x+1) / number_of_terms_1), ".2f")
                os.system('cls')
                print(status)
                print("\n\tComparing terms from file 1..."
                      "\n\tCurrent term: " + str(term) + "\t\tProgress: " + str(progress) + "%")
                time.sleep(.1)

            time.sleep(1)
            os.system('cls')
            print(status)
            print("\n\t\033[92mComparison of terms from file 1 finished!\033[0m"
                  "\n\n\tThe following terms could not be found in file 2:"
                  "\n\t" + str(unique_terms_1))
            input("\n\tType in anything to continue: ")

            for x in range(number_of_terms_2):
                term = terms_2[x]
                progress = format(100 * ((x+1) / number_of_terms_2), ".2f")
                os.system('cls')
                print(status)
                print("\n\t\33[93mComparing terms from file 2...\33[0m"
                      "\n\tCurrent term: " + str(term) + "\t\tProgress: " + str(progress) + "%")
                time.sleep(.1)

            # eliminating duplicates in common terms list
            common_terms = list(set(common_terms))

            time.sleep(1)
            os.system('cls')
            print(status)
            print("\n\t\033[92mComparison of terms from file 2 finished!\033[0m"
                  "\n\n\tThe following terms could not be found in file 1:"
                  "\n\t" + str(unique_terms_2))
            input("\n\tType in anything to continue: ")

            os.system('cls')
            print(status)
            print("\n\t\033[92mProcess finished!\033[0m"
                  "\n\tThe two excel files had the following terms in common:"
                  "\n\t" + str(common_terms) +
                  "\n\n\t\033[92mThe results were saved as an additional comparison excel file!\033[0m")
            input("\n\tType in anything to continue: ")

            # generating new Excel file for comparison results exclusively
            results_wb_name = CA.create_comparison_result_excel(fd=formatted_date)
            results_workbook = load_workbook(results_wb_name)
            results_worksheet = results_workbook.active

            # saving results
            results_worksheet = CA.write_comparison_result_excel(worksheet=results_worksheet,
                                                                 file_1=file_1, file_2=file_2,
                                                                 list_of_terms_1=unique_terms_1,
                                                                 list_of_terms_2=unique_terms_2,
                                                                 common_terms_list=common_terms)
            results_workbook.save(results_wb_name)

            log = open(log_title, "a", encoding="utf-8")
            log_output = "\t------------------------------------------------------------\n\n\tComparison mode accessed"\
                         "\n\tFile 1: " + file_1 + "\n\tFile 2: " + file_2 + "\n"
            log.write("\n\n" + log_output)
            log.close()

            os.system('cls')
            print(status)
            print("\n\tReturning to manual search mode...")
            time.sleep(5)
            NSP.play_mp3("./src/data/GUI_sound/Signal.mp3")

        # SETTINGS MODE ------------------------------------------------------------------------------------------------
        elif i == "set!":
            time.sleep(1)
            intro = "\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m" \
                    "\n\n\tThe several settings you can change will be displayed in succession." \
                    "\n\tFor every setting there will be the respective options given." \
                    "\n\tThe currently selected option will be marked with an arrow." \
                    "\n\tTo keep the currently selected option of a setting just press enter." \
                    "\n\tTo select another option please type in the given number." \
                    "\n\tYou can press enter to start now."
            os.system('cls')
            print(intro)
            input()

            # setting 1 (auto update)
            os.system('cls')
            CA.display_settings(1, auto_update)
            i = input("\n\tOption number: ")
            if i == "1":
                SDM.set_auto_update(1)
                auto_update = SDM.get_auto_update()
                os.system('cls')
                CA.display_settings_after_changes(1, auto_update)
                print("\033[32m" + "\n\tAutomatic update search set on!\033[0m")
                time.sleep(4)
            elif i == "2":
                SDM.set_auto_update(0)
                auto_update = SDM.get_auto_update()
                os.system('cls')
                CA.display_settings_after_changes(1, auto_update)
                print("\033[32m" + "\n\tAutomatic update search set off!\033[0m")
                time.sleep(4)
            else:
                print("\033[32m" + "\n\tPrevious setting will be kept!\033[0m")
                time.sleep(2)

            # setting 2 (term output diplomacy)
            os.system('cls')
            CA.display_settings(2, term_output_diplomacy)
            i = input("\n\tOption number: ")
            if i == "1":
                SDM.set_term_output_diplomacy(1)
                term_output_diplomacy = SDM.get_term_output_diplomacy()
                os.system('cls')
                CA.display_settings_after_changes(2, term_output_diplomacy)
                print("\033[32m" + "\n\tOnly found terms will be considered!\033[0m")
                time.sleep(4)
            elif i == "2":
                SDM.set_term_output_diplomacy(2)
                term_output_diplomacy = SDM.get_term_output_diplomacy()
                os.system('cls')
                CA.display_settings_after_changes(2, term_output_diplomacy)
                print("\033[32m" + "\n\tOnly not found terms will be considered!\033[0m")
                time.sleep(4)
            elif i == "3":
                SDM.set_term_output_diplomacy(3)
                term_output_diplomacy = SDM.get_term_output_diplomacy()
                os.system('cls')
                CA.display_settings_after_changes(2, term_output_diplomacy)
                print("\033[32m" + "\n\tAll terms will be considered!\033[0m")
                time.sleep(4)
            else:
                print("\033[32m" + "\n\tPrevious setting will be kept!\033[0m")
                time.sleep(2)

            # setting 3 (Output format)
            os.system('cls')
            CA.display_settings(3, oneline_output_format)
            i = input("\n\tOption number: ")
            if i == "1":
                SDM.set_one_line_output(True)
                oneline_output_format = SDM.get_one_line_output()
                os.system('cls')
                CA.display_settings_after_changes(3, oneline_output_format)
                print("\033[32m" + "\n\tOutput will be printed in one-line format!\033[0m")
                time.sleep(4)
            elif i == "2":
                SDM.set_one_line_output(False)
                oneline_output_format = SDM.get_one_line_output()
                os.system('cls')
                CA.display_settings_after_changes(3, oneline_output_format)
                print("\033[32m" + "\n\tOutput will be printed in multi-line format!\033[0m")
                time.sleep(4)
            else:
                print("\033[32m" + "\n\tPrevious setting will be kept!\033[0m")
                time.sleep(2)

            # setting 4 (headline-printing)
            os.system('cls')
            CA.display_settings(4, headline_printing)
            i = input("\n\tOption number: ")
            if i == "1":
                SDM.set_headline_printing(1)
                headline_printing = SDM.get_headline_printing()
                os.system('cls')
                CA.display_settings_after_changes(4, headline_printing)
                print("\033[32m" + "\n\tHeadline will be printed only at top of excel!\033[0m")
                time.sleep(4)
            elif i == "2":
                SDM.set_headline_printing(2)
                headline_printing = SDM.get_headline_printing()
                os.system('cls')
                CA.display_settings_after_changes(4, headline_printing)
                print("\033[32m" + "\n\tHeadline will be printed for every new document in scan mode!\033[0m")
                time.sleep(4)
            elif i == "3":
                SDM.set_headline_printing(3)
                headline_printing = SDM.get_headline_printing()
                os.system('cls')
                CA.display_settings_after_changes(4, headline_printing)
                print("\033[32m" + "\n\tHeadline will be printed for every new term!\033[0m")
                time.sleep(4)
            else:
                print("\033[32m" + "\n\tPrevious setting will be kept!\033[0m")
                time.sleep(2)

            # setting 5 (alphabetical output)
            os.system('cls')
            CA.display_settings(5, alphabetical_output, abc_output_ascending)
            i = input("\n\tOption number: ")
            if i == "1":
                SDM.set_alphabetical_output(abc=True, asc=True)
                alphabetical_output, abc_output_ascending = SDM.get_alphabetical_output()
                os.system('cls')
                CA.display_settings_after_changes(5, alphabetical_output, abc_output_ascending)
                print("\033[32m" + "\n\tOutput will be structured in ascending alphabetical order!\033[0m")
                time.sleep(4)
            elif i == "2":
                SDM.set_alphabetical_output(abc=True, asc=False)
                alphabetical_output, abc_output_ascending = SDM.get_alphabetical_output()
                os.system('cls')
                CA.display_settings_after_changes(5, alphabetical_output, abc_output_ascending)
                print("\033[32m" + "\n\tOutput will be structured in descending alphabetical order!\033[0m")
                time.sleep(4)
            elif i == "3":
                SDM.set_alphabetical_output(abc=False, asc=False)
                alphabetical_output, abc_output_ascending = SDM.get_alphabetical_output()
                os.system('cls')
                CA.display_settings_after_changes(5, alphabetical_output, abc_output_ascending)
                print("\033[32m" + "\n\tOutput will not be structured at all!\033[0m")
                time.sleep(4)
            else:
                print("\033[32m" + "\n\tPrevious setting will be kept!\033[0m")
                time.sleep(2)

            # setting 6 (auto scan filters)
            os.system('cls')
            CA.display_settings(6, auto_scan_filters)
            i = input("\n\n\tOption number: ")

            if i == "1":
                SDM.set_auto_scan_filters("Noun")
                auto_scan_filters = SDM.get_auto_scan_filters()
                os.system('cls')
                CA.display_settings_after_changes(6, auto_scan_filters)
                print("\033[32m" + '\n\t"Noun" is set as pos filter now!\033[0m')
                time.sleep(4)
            elif i == "2":
                SDM.set_auto_scan_filters("Verb")
                auto_scan_filters = SDM.get_auto_scan_filters()
                os.system('cls')
                CA.display_settings_after_changes(6, auto_scan_filters)
                print("\033[32m" + '\n\t"Verb" is set as pos filter now!\033[0m')
                time.sleep(4)
            elif i == "3":
                SDM.set_auto_scan_filters("Adjective")
                auto_scan_filters = SDM.get_auto_scan_filters()
                os.system('cls')
                CA.display_settings_after_changes(6, auto_scan_filters)
                print("\033[32m" + '\n\t"Adjective" is set as pos filter now!\033[0m')
                time.sleep(4)
            elif i == "4":
                SDM.set_auto_scan_filters("Adverb")
                auto_scan_filters = SDM.get_auto_scan_filters()
                os.system('cls')
                CA.display_settings_after_changes(6, auto_scan_filters)
                print("\033[32m" + '\n\t"Adverb" is set as pos filter now!\033[0m')
                time.sleep(4)
            elif i == "5":
                SDM.set_auto_scan_filters("Preposition")
                auto_scan_filters = SDM.get_auto_scan_filters()
                os.system('cls')
                CA.display_settings_after_changes(6, auto_scan_filters)
                print("\033[32m" + '\n\t"Preposition" is set as pos filter now!\033[0m')
                time.sleep(4)
            elif i == "6":
                SDM.set_auto_scan_filters("Phrase")
                auto_scan_filters = SDM.get_auto_scan_filters()
                os.system('cls')
                CA.display_settings_after_changes(6, auto_scan_filters)
                print("\033[32m" + '\n\t"Phrase" is set as pos filter now!\033[0m')
                time.sleep(4)
            elif i == "7":
                SDM.set_auto_scan_filters("Noun,Verb,Adjective,Adverb,Preposition,Phrase")
                auto_scan_filters = SDM.get_auto_scan_filters()
                os.system('cls')
                CA.display_settings_after_changes(6, auto_scan_filters)
                print("\033[32m" + '\n\tAll pos types will be considered now!\033[0m')
                time.sleep(4)
            else:
                print("\033[32m" + "\n\tPrevious setting will be kept!\033[0m")
                time.sleep(2)

            # setting 7 (output detail level)
            os.system('cls')
            CA.display_settings(7, output_detail_level)
            i = input("\n\tOption number: ")
            if i == "1":
                SDM.set_output_detail_level(1)
                output_detail_level = SDM.get_output_detail_level()
                os.system('cls')
                CA.display_settings_after_changes(7, output_detail_level)
                print("\033[32m" + "\n\tOutput will cover term data only!\033[0m")
                time.sleep(4)
            elif i == "2":
                SDM.set_output_detail_level(2)
                output_detail_level = SDM.get_output_detail_level()
                os.system('cls')
                CA.display_settings_after_changes(7, output_detail_level)
                print("\033[32m" + "\n\tOutput will cover term data and morphology data!\033[0m")
                time.sleep(4)
            elif i == "3":
                SDM.set_output_detail_level(3)
                output_detail_level = SDM.get_output_detail_level()
                os.system('cls')
                CA.display_settings_after_changes(7, output_detail_level)
                print("\033[32m" + "\n\tOutput will cover all data information!\033[0m")
                time.sleep(4)
            else:
                print("\033[32m" + "\n\tPrevious setting will be kept!\033[0m")
                time.sleep(2)

            os.system('cls')
            outro = "\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m" \
                    "\033[32m" + "\n\n\tNew configurations were saved!" + "\033[0m" \
                    "\n\n\tReturning to main menu..."
            print(outro)
            time.sleep(4)
            print_opening_again = True

        else:
            # BASIC SEARCH ---------------------------------------------------------------------------------------------
            if CA.is_valid_input(i):

                if excel_row == 1:
                    worksheet, excel_row = CA.print_headlines(worksheet, excel_row, output_detail_level)
                    headline_already_printed = True

                open_excel_automatically = True
                if ":" in i:
                    splitted_input = i.split(":")
                    term = splitted_input[0]
                    pos_filters = ""
                    for x in range(1, len(splitted_input)):
                        pos_filters += str(splitted_input[x])
                        if not x == len(splitted_input) - 1:
                            pos_filters += ","
                    os.system('cls')
                    print('\n\tSearching for term "' + term + '" with pos tag (' + pos_filters + ')...')
                    time.sleep(2)
                else:
                    pos_filters = "Noun, Verb, Adjective, Adverb, Preposition, Phrase"
                    term = i
                    os.system('cls')
                    print('\n\tSearching for term "' + term + '" ...')
                    time.sleep(1)
                if term_output_diplomacy == 1:
                    worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                            excel_row=excel_row,
                                                                            pos_filters=pos_filters,
                                                                            term=term,
                                                                            entries_list=entries_list,
                                                                            only_found_terms=True,
                                                                            only_not_found_terms=False,
                                                                            multiline_output=not oneline_output_format,
                                                                            output_detail_level=output_detail_level,
                                                                            headline_printing=headline_printing,
                                                                            hap=headline_already_printed)
                elif term_output_diplomacy == 2:
                    worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                            excel_row=excel_row,
                                                                            pos_filters=pos_filters,
                                                                            term=term,
                                                                            entries_list=entries_list,
                                                                            only_found_terms=False,
                                                                            only_not_found_terms=True,
                                                                            multiline_output=not oneline_output_format,
                                                                            output_detail_level=output_detail_level,
                                                                            headline_printing=headline_printing,
                                                                            hap=headline_already_printed)
                else:
                    worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                            excel_row=excel_row,
                                                                            pos_filters=pos_filters,
                                                                            term=term,
                                                                            entries_list=entries_list,
                                                                            only_found_terms=False,
                                                                            only_not_found_terms=False,
                                                                            multiline_output=not oneline_output_format,
                                                                            output_detail_level=output_detail_level,
                                                                            headline_printing=headline_printing,
                                                                            hap=headline_already_printed)

                print("\n\tSaving...")
                time.sleep(1)

                log = open(log_title, "a", encoding="utf-8")
                log.write("\n\n" + log_output)
                log.close()

                workbook.save(workbook_title)

                os.system('cls')
                print("\033[32m" + "\n\tDone!" + "\033[0m")
                time.sleep(1)
                os.system('cls')
            else:
                print_opening_again = True


CA.print_opening(version="3.0c")
check_paths()
if auto_update == 1:
    check_for_updates()

formatted_date = CA.get_datetime()

log_name = CA.create_logfile(fd=formatted_date)
wb_name = CA.create_excel(fd=formatted_date)

search_for_terms(log_name, wb_name)