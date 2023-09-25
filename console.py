import json, sys
import time
from openpyxl import load_workbook
from playsound import playsound
import os, requests
import keyboard
from urllib3.exceptions import NameResolutionError, MaxRetryError

import savedata_manager as SDM
import console_assistance as CA

# system variables
restart_program = True
auto_update = SDM.get_auto_update()
term_output_diplomacy = SDM.get_term_output_diplomacy()
oneline_output_format = SDM.get_one_line_output()
headline_printing = SDM.get_headline_printing()
alphabetical_output, abc_output_ascending = SDM.get_alphabetical_output()
output_detail_level = SDM.get_output_detail_level()
auto_scan_filters = SDM.get_auto_scan_filters()


def set_system_variables_to_default():

    SDM.set_auto_update(0)
    SDM.set_term_output_diplomacy(3)
    SDM.set_one_line_output(1)
    SDM.set_headline_printing(1)
    SDM.set_alphabetical_output(True, True)
    SDM.set_auto_scan_filters("Noun,Verb,Adverb,Adjective,Preposition,Phrase")
    SDM.set_output_detail_level(2)


def check_paths():
    global auto_update
    time.sleep(2)
    os.system('cls')
    CA.print_opening(version="Version 2.2c")
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
            CA.print_opening(version="Version 2.2c")
            print("\n\tWarning: wiki_morph database could not be found on your system!"
                  "\n\tYou are free to download it automatically.")
            if remote_size == 0:
                print("\tSize of file: unknown")
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
                    CA.print_opening(version="Version 2.2c")
                    print("\n\n\tDownload completed! (" + str(current_size) + " MB)"
                          "\n\n\tDo you wish to search for terms now? (y/n)")
                    answer = input("\n\tanswer: ")
                    if answer == "n":
                        print("\n\tProgram will now terminate.")
                        time.sleep(3)
                        sys.exit(0)
                else:
                    sys.exit()

            else:
                CA.print_exit_without_download()
            time.sleep(1)

        except NameResolutionError or MaxRetryError:
            os.system('cls')
            CA.print_opening(version="Version 2.2c")
            print("\n\tWarning: Database is not installed currently."
                  "\n\n\tThis program offers the possibility to download the database automatically."
                  "\n\tBut for the moment there was no internet connection recognized."
                  "\n\tPlease make sure you are connected and restart the program."
                  "\n\tThe program will now terminate.")
            time.sleep(7)
            sys.exit(0)

    else:
        os.system('cls')
        current_size = os.path.getsize("src/database/wiki_morph.json")
        current_size = int(current_size / (1024 * 1024))
        soll_size = SDM.get_soll_size()

        if current_size < soll_size:
            CA.print_opening(version="Version 2.2c")
            print("\n\tWarning: the local database file does not cover the expected amount of information!"
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
                playsound("src/data/GUI_sound/Signal.mp3")

                current_size = os.path.getsize("src/database/wiki_morph.json")
                current_size = int(current_size / (1024 * 1024))
                SDM.set_current_size(current_size)
                auto_update = False
                os.system('cls')
                CA.print_opening(version="Version 2.2c")
                print("\n\n\tDownload completed! (" + str(current_size) + " MB)"
                      "\n\n\tDo you wish to search for terms now? (y/n)")
                answer = input("\n\tanswer: ")
                if answer == "n":
                    print("\n\tProgramm will now terminate.")
                    time.sleep(3)
                    sys.exit(0)

            else:
                CA.print_exit_without_download()
        else:
            CA.print_opening(version="Version 2.2c")
            print("\n\tDatabase installed and available.")
        time.sleep(3)


def check_for_updates():
    os.system('cls')
    CA.print_opening(version="Version 2.2c")
    print("\n\tChecking for wiki_morph updates...")
    time.sleep(3)

    current_size = SDM.get_current_size()

    try:
        url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
        response = requests.get(url, stream=True)
        remote_size = int(response.headers.get("Content-Length", 0))
        remote_size = int(remote_size / (1024 * 1024))

        if remote_size == 0:
            os.system('cls')
            CA.print_opening(version="Version 2.2c")
            print("\n\tUpdate check not possible: Server does not provide required information!"
                  "\n\tLast recent locally installed version will be used.")
            time.sleep(7)
        else:
            if current_size < remote_size:
                os.system('cls')
                CA.print_opening(version="Version 2.2c")
                print("\n\tThere is a new version of wiki_morph available!"
                      "\n\n\tSize: " + str(remote_size) + " MB"
                      "\n\n\t Do you want to download the update now? (y/n)")
                answer = input("\n\tanswer: ")
                if answer == "y":
                    SDM.set_download_size(remote_size)
                    CA.download_database(url=url)

                    os.system('cls')
                    CA.print_opening(version="Version 2.2c")
                    print("\n\n\tUpdate completed! (" + str(current_size) + " MB)"
                          "\n\n\tDo you wish to search for terms now? (y/n)")
                    answer = input("\n\tanswer: ")
                    if answer == "n":
                        print("\n\tProgramm will now terminate.")
                        time.sleep(3)
                        sys.exit(0)
            else:
                os.system('cls')
                CA.print_opening(version="Version 2.2c")
                print("\n\tThe installed database is up to date!")
                time.sleep(3)
    except NameResolutionError or MaxRetryError:
        CA.print_opening(version="Version 2.2c")
        print("\n\tUpdate check not possible: No internet connection!"
              "\n\tLast recent locally installed version will be used.")
        time.sleep(5)


def search_for_terms(log_title, workbook_title):
    global restart_program
    global auto_update
    global term_output_diplomacy
    global oneline_output_format
    open_excel_automatically = False

    # loading database
    os.system('cls')
    CA.print_opening(version="Version 2.2c")
    print("\n\tLoading wiki_morph database...")
    with open("src/database/wiki_morph.json", "r", encoding="utf-8") as f:
        entries_list = json.load(f)
    os.system('cls')
    CA.print_opening(version="Version 2.2c")
    print("\n\tCompleted!")
    time.sleep(1)
    playsound("src/data/GUI_sound/Signal.mp3")
    os.system('cls')
    CA.print_opening(version="Version 2.2c")
    time.sleep(.25)
    print("\n\tYou can now search for terms.")
    time.sleep(.25)
    print('\n\t1) For searching a term type in the term.')
    time.sleep(.25)
    print('\t2) For searching a term with filter(s) type in the term with the respective filter(s).')
    time.sleep(.25)
    print('\t3) For Automatic scan mode type "s!".')
    time.sleep(.25)
    print('\t4) For Comparison mode type "c!".\t\t\033[32m<- New!\033[0m')
    time.sleep(.25)
    print('\t5) For further instructions type "i!".')
    time.sleep(.25)
    print('\t6) For version description type "v!".')
    time.sleep(.25)
    print('\t7) For Settings mode type "set!".\t\t\033[32m<- New!\033[0m')
    time.sleep(.25)
    print('\t8) For ending the program type "exit!".')
    time.sleep(.25)

    # search function
    stop = False
    excel_row = 1
    workbook = load_workbook(workbook_title)
    worksheet = workbook.active

    while not stop:

        i = input("\n\tSearch term: ")
        os.system('cls')

        if i == "exit!":
            print("\n\tProgram terminated!")
            restart_program = False
            stop = True
            if open_excel_automatically:
                os.system(f'start "" {workbook_title}')
        elif i == "i!":
            CA.show_instructions()
        elif i == "v!":
            CA.show_version_description()

        elif i == "s!":
            open_excel_automatically = True
            os.system('cls')
            print("\n\t- Automatic scan mode -"
                  "\n\n\tPlease select an excel file to scan for possible terms.")
            time.sleep(1.5)
            file = CA.select_excel_file()
            terms = CA.autoscan(file, duplicates=False, abc=alphabetical_output, abc_ascending=abc_output_ascending)
            number_of_terms = len(terms)
            status = "\n\t- Automatic scan mode -" \
                     "\n\n\tExcel file: " + file +\
                     "\n\tFound terms: " + str(number_of_terms)
            time.sleep(2)
            os.system('cls')
            print(status)
            """
            print("\n\tTerm output diplomacy"
                  "\n\tPlease state which terms shall be considered in the output excel file:"
                  '\n\tType in "1" for considering all terms with an entry.'
                  '\n\tType in "2" for considering all terms with no entry.'
                  '\n\tType in "3" for considering all terms in general.')
            output_option = input("\n\tAnswer: ")
            """
            print("\n\tThe terms will now be searched in the database.")
            time.sleep(2)

            worksheet, excel_row = CA.print_headlines(worksheet, excel_row)

            if term_output_diplomacy == "1":
                for x in range(number_of_terms):
                    term = terms[x]
                    os.system('cls')
                    progress = format(100*(x/number_of_terms), ".2f")
                    print(status)
                    print("\n\tSearching for terms..."
                          "\n\tCurrent term: " + term + "\t\tProgress: " + str(progress) + "%")

                    worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                            excel_row=excel_row,
                                                                            pos_filters=auto_scan_filters,
                                                                            term=term,
                                                                            entries_list=entries_list,
                                                                            only_found_terms=True,
                                                                            only_not_found_terms=False,
                                                                            multiline_output=not oneline_output_format)
                    progress = int(50*(x/number_of_terms))
                    progressbar = ("\t[" + "-" * (progress-1) + ">" + " " * (50-(progress+1)) + "]")
                    print(progressbar)

                    log = open(log_title, "a", encoding="utf-8")
                    log.write("\n\n" + log_output)
                    log.close()

                    workbook.save(workbook_title)

            elif term_output_diplomacy == "2":
                for x in range(number_of_terms):
                    term = terms[x]
                    os.system('cls')
                    progress = format(100 * (x / number_of_terms), ".2f")
                    print(status)
                    print("\n\tSearching for terms..."
                          "\n\tCurrent term: " + term + "\t\tProgress: " + str(progress) + "%")

                    worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                            excel_row=excel_row,
                                                                            pos_filters=auto_scan_filters,
                                                                            term=term,
                                                                            entries_list=entries_list,
                                                                            only_found_terms=False,
                                                                            only_not_found_terms=True,
                                                                            multiline_output=not oneline_output_format)
                    progress = int(50 * (x / number_of_terms))
                    progressbar = ("\t[" + "-" * (progress - 1) + ">" + " " * (50 - (progress + 1)) + "]")
                    print(progressbar)

                    log = open(log_title, "a", encoding="utf-8")
                    log.write("\n\n" + log_output)
                    log.close()

                    workbook.save(workbook_title)

            else:
                for x in range(number_of_terms):
                    term = terms[x]
                    os.system('cls')
                    progress = format(100 * (x / number_of_terms), ".2f")
                    print(status)
                    print("\n\tSearching for terms..."
                          "\n\tCurrent term: " + term + "\t\tProgress: " + str(progress) + "%")

                    worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                            excel_row=excel_row,
                                                                            pos_filters=auto_scan_filters,
                                                                            term=term,
                                                                            entries_list=entries_list,
                                                                            only_found_terms=False,
                                                                            only_not_found_terms=False,
                                                                            multiline_output=not oneline_output_format)
                    progress = int(50 * (x / number_of_terms))
                    progressbar = ("\t[" + "-" * (progress - 1) + ">" + " " * (50 - (progress + 1)) + "]")
                    print(progressbar)

                    log = open(log_title, "a", encoding="utf-8")
                    log.write("\n\n" + log_output)
                    log.close()

                    workbook.save(workbook_title)

            os.system('cls')
            print(status)
            print("\n\tProcess finished!"
                  "\n\n\tResults will be saved to output when the program ends."
                  "\n\tReturning to manual search mode...")

            time.sleep(7)
            os.system('cls')
            playsound("src/data/GUI_sound/Signal.mp3")

        elif i == "c!":
            open_excel_automatically = False
            os.system('cls')
            status = "\n\t- Comparison mode -"
            print(status)
            print("\n\tPlease select two excel files you want to compare.")
            time.sleep(3)
            print("\n\tSelect excel file 1 now.")
            time.sleep(3)
            file_1 = CA.select_excel_file()
            terms_1 = CA.autoscan(file_1)
            number_of_terms_1 = len(terms_1)
            print("\n\tSelected file 1: " + file_1)
            print("\tFound terms: " + str(number_of_terms_1))
            time.sleep(4)

            os.system('cls')
            print(status)
            print("\n\tSelect excel file 2 now.")
            time.sleep(3)
            file_2 = CA.select_excel_file()
            terms_2 = CA.autoscan(file_2)
            number_of_terms_2 = len(terms_2)
            print("\n\tSelected file 2: " + file_2)
            print("\tFound terms: " + str(number_of_terms_2))
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
                print("\n\tScanning file 1..."
                      "\n\tCurrent term: " + term + "\t\tProgress: " + str(progress) + "%")
                if term not in terms_2:
                    unique_terms_1.append(term)
                    print("\n\tTerm not found in file 2!")
                else:
                    common_terms.append(term)
                    print("\n\tTerm found in file 2!")

            time.sleep(1)
            os.system('cls')
            print(status)
            print("\n\tScanning of file 1 finished!"
                  "\n\n\tThe following terms could not be found in file 2:"
                  "\n\t" + str(unique_terms_1))
            time.sleep(7)

            for x in range(number_of_terms_2):
                term = terms_2[x]
                progress = format(100 * ((x+1) / number_of_terms_2), ".2f")
                os.system('cls')
                print(status)
                print("\n\tScanning file 2..."
                      "\n\tCurrent term: " + term + "\t\tProgress: " + str(progress) + "%")
                if term not in terms_1:
                    unique_terms_2.append(term)
                    print("\n\tTerm not found in file 1!")
                else:
                    common_terms.append(term)
                    print("\n\tTerm found in file 1!")

            # eliminating duplicates in common terms list
            common_terms = list(set(common_terms))

            time.sleep(1)
            os.system('cls')
            print(status)
            print("\n\tScanning of file 2 finished!"
                  "\n\n\tThe following terms could not be found in file 1:"
                  "\n\t" + str(unique_terms_2))
            time.sleep(7)

            os.system('cls')
            print(status)
            print("\n\tProcess finished!"
                  "\n\tThe two excel files had the following terms in common:"
                  "\n\t" + str(common_terms) +
                  "\n\n\tThe results will now be saved in an additional excel file...")
            time.sleep(10)

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
            log_output = "\t------------------------------------------------------------\n\n\tComparion mode accessed" \
                         "\n\tFile 1: " + file_1 + "\n\tFile 2: " + file_2 + "\n"
            log.write("\n\n" + log_output)
            log.close()

            os.system('cls')
            print(status)
            print("\n\tSaving process finished!"
                  "\n\tReturning to manual search mode...")
            time.sleep(5)
            playsound("src/data/GUI_sound/Signal.mp3")

        elif i == "set!":
            time.sleep(1)
            intro = "\t~ Settings Menu ~" \
                     "\n\n\tThe several settings you can change will be displayed in succession." \
                     "\n\tFor every setting there will be the respective options displayed." \
                     "\n\tTo select an option please type in the given number." \
                     "\n\tTo keep the currently selected option of a setting just press enter." \
                     "\n\tTo break up and return to main menu without saving press escape." \
                     "\n\tYou can press enter to start now."
            os.system('cls')
            print(intro)
            input()

            # setting 1 (auto update)
            os.system('cls')
            CA.display_settings(1, auto_update)
            i = input("\n\tOption number: ")
            if i == "1":
                print("\n\tAutomatic update set on!")
                SDM.set_auto_update(1)
                auto_update = SDM.get_auto_update()
                time.sleep(4)
            elif i == "2":
                print("\n\tAutomatic update set off!")
                SDM.set_auto_update(0)
                auto_update = SDM.get_auto_update()
                time.sleep(4)
            else:
                print("\n\tPrevious setting will be kept!")
                time.sleep(2)

            # setting 2 (term output diplomacy)
            os.system('cls')
            CA.display_settings(2, term_output_diplomacy)
            i = input("\n\tOption number: ")
            if i == "1":
                print("\n\tOnly found terms will be considered!")
                SDM.set_term_output_diplomacy(1)
                term_output_diplomacy = SDM.get_term_output_diplomacy()
            elif i == "2":
                print("\n\tOnly not found terms will be considered!")
                time.sleep(4)
                SDM.set_term_output_diplomacy(2)
                term_output_diplomacy = SDM.get_term_output_diplomacy()
            elif i == "3":
                SDM.set_term_output_diplomacy(3)
                term_output_diplomacy = SDM.get_term_output_diplomacy()
                print("\n\tAll terms will be considered!")
                time.sleep(4)
            else:
                print("\n\tPrevious setting will be kept!")
                time.sleep(2)

            # setting 3 (Output format)
            os.system('cls')
            CA.display_settings(3, oneline_output_format)
            i = input("\n\tOption number: ")
            if i == "1":
                print("\n\tOutput will be printed in one-line format!")
                SDM.set_one_line_output(True)
                oneline_output_format = SDM.get_one_line_output()
                time.sleep(4)
            elif i == "2":
                print("\n\tOutput will be printed in multi-line format!")
                SDM.set_one_line_output(False)
                oneline_output_format = SDM.get_one_line_output()
                time.sleep(4)
            else:
                print("\n\tPrevious setting will be kept!")
                time.sleep(2)

        else:
            open_excel_automatically = True
            if ":" in i:
                splitted_input = i.split(":")
                term = splitted_input[0]
                pos_filters = []
                for x in range(1, len(splitted_input)):
                    pos_filters.append(splitted_input[x])
            else:
                pos_filters = ["Noun", "Verb", "Adverb", "Adjective", "Preposition", "Phrase"]
                term = i

            if term_output_diplomacy == 1:
                worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                        excel_row=excel_row,
                                                                        pos_filters=pos_filters,
                                                                        term=term,
                                                                        entries_list=entries_list,
                                                                        only_found_terms=True,
                                                                        only_not_found_terms=False,
                                                                        multiline_output=not oneline_output_format)
            elif term_output_diplomacy == 2:
                worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                        excel_row=excel_row,
                                                                        pos_filters=pos_filters,
                                                                        term=term,
                                                                        entries_list=entries_list,
                                                                        only_found_terms=False,
                                                                        only_not_found_terms=True,
                                                                        multiline_output=not oneline_output_format)
            else:
                worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                        excel_row=excel_row,
                                                                        pos_filters=pos_filters,
                                                                        term=term,
                                                                        entries_list=entries_list,
                                                                        only_found_terms=False,
                                                                        only_not_found_terms=False,
                                                                        multiline_output=not oneline_output_format)

            log = open(log_title, "a", encoding="utf-8")
            log.write("\n\n" + log_output)
            log.close()

            workbook.save(workbook_title)


CA.print_opening(version="Version 2.2c")
check_paths()
if auto_update == 1:
    check_for_updates()

formatted_date = CA.get_datetime()

log_name = CA.create_logfile(fd=formatted_date)
wb_name = CA.create_excel(fd=formatted_date)

while restart_program:
    search_for_terms(log_name, wb_name)
    time.sleep(.1)

