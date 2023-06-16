import json, sys
import time
from openpyxl import load_workbook

import os, requests

from urllib3.exceptions import NameResolutionError, MaxRetryError

import savedata_manager as SDM
import console_assistance as CA

check_for_updates_necessary = True


def check_paths():
    global check_for_updates_necessary
    time.sleep(2)
    os.system('cls')
    print("\n\tChecking database status...")
    time.sleep(1)

    if not os.path.exists("data/wiki_morph.json"):
        SDM.set_current_size()
        try:
            url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
            response = requests.get(url, stream=True)
            remote_size = int(response.headers.get("Content-Length", 0))
            remote_size = int(remote_size / (1024 * 1024))

            os.system('cls')
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
                    current_size = os.path.getsize("data/wiki_morph.json")
                    current_size = int(current_size / (1024 * 1024))
                    SDM.set_current_size(current_size)

                    check_for_updates_necessary = False
                    os.system('cls')
                    print("\n\n\tDownload completed! (" + str(current_size) + " MB)"
                          "\n\n\tDo you wish to search for terms now? (y/n)")
                    answer = input("\n\tanswer: ")
                    if answer == "n":
                        print("\n\tProgramm will now terminate.")
                        time.sleep(3)
                        sys.exit(0)
                else:
                    sys.exit()

            else:
                CA.print_exit_without_download()
            time.sleep(1)

        except NameResolutionError or MaxRetryError:
            os.system('cls')
            print("\tWarning: Database is not installed currently."
                  "\n\n\tThis program offers the possibility to download the database automatically."
                  "\n\tBut for the moment there was no internet connection recognized."
                  "\n\tPlease make sure you are connected and restart the program."
                  "\n\tThe program will now terminate.")
            time.sleep(7)
            sys.exit(0)

    else:
        os.system('cls')
        current_size = os.path.getsize("data/wiki_morph.json")
        current_size = int(current_size / (1024 * 1024))
        soll_size = SDM.get_soll_size()

        if current_size < soll_size:
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

                current_size = os.path.getsize("data/wiki_morph.json")
                current_size = int(current_size / (1024 * 1024))
                SDM.set_current_size(current_size)

                check_for_updates_necessary = False
                os.system('cls')
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
            print("\n\tDatabase installed and available.")
        time.sleep(3)


def check_for_updates():
    os.system('cls')
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
            print("\n\tUpdate check not possible: Server does not provide required information!"
                  "\n\tLast recent locally installed version will be used.")
            time.sleep(7)
        else:
            if current_size < remote_size:
                os.system('cls')
                print("\n\tThere is a new version of wiki_morph available!"
                      "\n\n\tSize: " + str(remote_size) + " MB"
                      "\n\n\t Do you want to download the update now? (y/n)")
                answer = input("\n\tanswer: ")
                if answer == "y":
                    SDM.set_download_size(remote_size)
                    CA.download_database(url=url)

                    os.system('cls')
                    print("\n\n\tUpdate completed! (" + str(current_size) + " MB)"
                          "\n\n\tDo you wish to search for terms now? (y/n)")
                    answer = input("\n\tanswer: ")
                    if answer == "n":
                        print("\n\tProgramm will now terminate.")
                        time.sleep(3)
                        sys.exit(0)
            else:
                os.system('cls')
                print("\n\tThe installed database is up to date!")
                time.sleep(3)
    except NameResolutionError or MaxRetryError:
        print("\n\tUpdate check not possible: No internet connection!"
              "\n\tLast recent locally installed version will be used.")


def search_for_terms(log_title, workbook_title):
    # loading database
    os.system('cls')
    print("\n\tLoading wiki_morph database...")
    with open("data/wiki_morph.json", "r", encoding="utf-8") as f:
        entries_list = json.load(f)
    os.system('cls')
    print("\n\tCompleted!")

    time.sleep(.5)
    print("\n\tYou can now search for terms.")
    time.sleep(.5)
    print('\n\t1) For instructions type "i!".')
    time.sleep(.5)
    print('\t2) For version description type "v!".')
    time.sleep(.5)
    print('\t3) For Automatic scan mode type "s!".')
    time.sleep(.5)
    print('\t4) For ending the program type "exit!".')
    time.sleep(.5)

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
            stop = True
            os.system(f'start "" {workbook_title}')
        elif i == "i!":
            CA.show_instructions()
        elif i == "v!":
            CA.show_version_description()

        elif i == "s!":
            os.system('cls')
            print("\t- Automatic scan mode -"
                  "\n\n\tPlease select an excel file to scan for possible terms.")
            time.sleep(1.5)
            file = CA.select_excel_file()
            terms = CA.autoscan(file)
            number_of_terms = len(terms)
            pos_filters = ["Noun"]
            status = "\t- Automatic scan mode -" \
                     "\n\n\tExcel file: " + file +\
                     "\n\tFound terms: " + str(number_of_terms)
            os.system('cls')
            print(status)
            print("\n\tThe terms will now be searched in the database.")
            time.sleep(2)

            for x in range(number_of_terms):
                term = terms[x]
                os.system('cls')
                progress = format(100*(x/number_of_terms), ".2f")
                print(status)
                print("\n\tSearching for terms..."
                      "\n\tCurrent term: " + term + "\t\tProgress: " + str(progress) + "%")
                worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                        excel_row=excel_row,
                                                                        pos_filters=pos_filters,
                                                                        term=term,
                                                                        entries_list=entries_list,
                                                                        print_console_output=False)
                progress = int(50*(x/number_of_terms))
                progressbar = ("\t[" + "-" * (progress-1) + ">" + " " * (50-(progress+1)) + "]")
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

            time.sleep(3)
            os.system('cls')

        else:
            if ":" in i:
                splitted_input = i.split(":")
                term = splitted_input[0]
                pos_filters = []
                for x in range(1, len(splitted_input)):
                    pos_filters.append(splitted_input[x])
            else:
                pos_filters = ["Noun", "Verb", "Adverb", "Adjective", "Preposition", "Phrase"]
                term = i

            """
            def search_and_output(excel_row):
                term_Hcell = 'A' + str(excel_row)
                filter_Hcell = 'B' + str(excel_row)
                pos_Hcell = 'C' + str(excel_row)
                syll_Hcell = 'D' + str(excel_row)
                def_Hcell = 'E' + str(excel_row)
                morph_Hcell = 'F' + str(excel_row)
    
                worksheet[term_Hcell] = 'Term'
                worksheet[filter_Hcell] = 'Filter'
                worksheet[pos_Hcell] = 'PoS'
                worksheet[syll_Hcell] = 'Syllables'
                worksheet[def_Hcell] = 'Definition'
                worksheet[morph_Hcell] = 'Morphemes'
    
                worksheet[term_Hcell].font = Font(bold=True)
                worksheet[filter_Hcell].font = Font(bold=True)
                worksheet[pos_Hcell].font = Font(bold=True)
                worksheet[syll_Hcell].font = Font(bold=True)
                worksheet[def_Hcell].font = Font(bold=True)
                worksheet[morph_Hcell].font = Font(bold=True)
    
                excel_row += 1
    
                term_cell = "A" + str(excel_row)
                worksheet[term_cell] = term
                filter_cell = "B" + str(excel_row)
                if len(pos_filters) == 6:
                    worksheet[filter_cell] = "NONE"
                else:
                    worksheet[filter_cell] = str(pos_filters)
                found_entries = 0
    
                log_output = "\t------------------------------------------------------------\n\n\tWord: " + term
                final_output = "\t------------------------------------------------------------\n\n\tWord: " + term
                output = ""
                pos_output = ""
    
                for x in range(len(entries_list)):
    
                    # print(type(entries_list[x]))
                    # print(entries_list[x])
                    entry = entries_list[x]
    
                    if entry["Word"] == term and entry["PoS"] in pos_filters:
    
                        keys = list(entry.keys())
                        
                        Data Structure Level 1 ---------------------------------------------------------------------
                        
    
                        pos_value = entry[keys[1]]
                        syllables_value = entry[keys[2]]
                        definition_value = entry[keys[3]]
                        morphemes_value = entry[keys[4]]
    
                        pos_cell = "C" + str(excel_row)
                        syll_cell = "D" + str(excel_row)
                        def_cell = "E" + str(excel_row)
    
                        worksheet[pos_cell] = str(pos_value)
                        worksheet[syll_cell] = str(syllables_value)
                        worksheet[def_cell] = str(definition_value)
    
                        excel_row += 1
                        found_entries += 1
    
                        output += "\n\t" + str(found_entries) + ")" + \
                                  "\t" + str(keys[1]) + ": " + str(pos_value) + "\n" + \
                                  "\t\t" + str(keys[2]) + ": " + str(syllables_value) + "\n" + \
                                  "\t\t" + str(keys[3]) + ": " + str(definition_value) + "\n" + \
                                  "\t\t" + str(keys[4]) + ": " + str(morphemes_value) + "\n"
    
                        
                        Data Structure Level 2 ---------------------------------------------------------------------
                        
                        if morphemes_value is not None:
    
                            affix_Hcell = 'F' + str(excel_row)
                            lang_Hcell = 'G' + str(excel_row)
                            sub_pos_Hcell = 'H' + str(excel_row)
                            mean_Hcell = 'I' + str(excel_row)
                            etcom_Hcell = 'J' + str(excel_row)
    
                            worksheet[affix_Hcell] = 'Affix'
                            worksheet[lang_Hcell] = 'Language'
                            worksheet[sub_pos_Hcell] = 'PoS'
                            worksheet[mean_Hcell] = 'Meaning'
                            worksheet[etcom_Hcell] = 'Etymology Compounds'
    
                            worksheet[affix_Hcell].font = Font(bold=True)
                            worksheet[lang_Hcell].font = Font(bold=True)
                            worksheet[sub_pos_Hcell].font = Font(bold=True)
                            worksheet[mean_Hcell].font = Font(bold=True)
                            worksheet[etcom_Hcell].font = Font(bold=True)
    
                            excel_row += 1
    
                            for respective_morph_dict in morphemes_value:
    
                                morphemes_sub_values = list(respective_morph_dict.values())
    
                                affix_value = morphemes_sub_values[0]
                                language_value = morphemes_sub_values[1]
                                sub_pos_value = morphemes_sub_values[2]
                                meaning_value = morphemes_sub_values[3]
                                etcom_value = morphemes_sub_values[4]
    
                                affix_cell = "F" + str(excel_row)
                                lang_cell = "G" + str(excel_row)
                                pos_cell = "H" + str(excel_row)
                                mean_cell = "I" + str(excel_row)
    
                                worksheet[affix_cell] = str(affix_value)
                                worksheet[lang_cell] = str(language_value)
                                worksheet[pos_cell] = str(sub_pos_value)
                                worksheet[mean_cell] = str(meaning_value)
    
                                excel_row += 1
    
                                
                                Data Structure Level 3 -------------------------------------------------------------
                                
                                if etcom_value is not None:
    
                                    sub_affix_Hcell = 'J' + str(excel_row)
                                    sub_lang_Hcell = 'K' + str(excel_row)
                                    decoded_Hcell = 'L' + str(excel_row)
                                    sub_sub_pos_Hcell = 'M' + str(excel_row)
                                    sub_meaning_Hcell = 'N' + str(excel_row)
    
                                    worksheet[sub_affix_Hcell] = 'Affix'
                                    worksheet[sub_lang_Hcell] = 'Language'
                                    worksheet[decoded_Hcell] = 'Decoded'
                                    worksheet[sub_sub_pos_Hcell] = 'PoS'
                                    worksheet[sub_meaning_Hcell] = 'Meaning'
    
                                    worksheet[sub_affix_Hcell].font = Font(bold=True)
                                    worksheet[sub_lang_Hcell].font = Font(bold=True)
                                    worksheet[decoded_Hcell].font = Font(bold=True)
                                    worksheet[sub_sub_pos_Hcell].font = Font(bold=True)
                                    worksheet[sub_meaning_Hcell].font = Font(bold=True)
    
                                    excel_row += 1
    
                                    for respective_etcom_dict in etcom_value:
    
                                        etcom_sub_values = list(respective_etcom_dict.values())
    
                                        sub_affix_value = etcom_sub_values[0]
                                        sub_language_value = etcom_sub_values[1]
                                        decoded_value = etcom_sub_values[2]
                                        sub_sub_pos_value = etcom_sub_values[3]
                                        sub_meaning_value = etcom_sub_values[4]
    
                                        sub_affix_cell = "J" + str(excel_row)
                                        sub_language_cell = "K" + str(excel_row)
                                        decoded_cell = "L" + str(excel_row)
                                        sub_sub_pos_cell = "M" + str(excel_row)
                                        sub_meaning_cell = "N" + str(excel_row)
    
                                        worksheet[sub_affix_cell] = str(sub_affix_value)
                                        worksheet[sub_language_cell] = str(sub_language_value)
                                        worksheet[decoded_cell] = str(decoded_value)
                                        worksheet[sub_sub_pos_cell] = str(sub_sub_pos_value)
                                        worksheet[sub_meaning_cell] = str(sub_meaning_value)
    
                        excel_row += 1
    
                if found_entries == 0 and len(pos_filters) == 6:
                    final_output += "\n\tWarning: database has no entry for '" + term + "'."
                    log_output += "\n\tWarning: no entry for '" + term + "'."
    
                    pos_cell = "C" + str(excel_row)
                    syll_cell = "D" + str(excel_row)
                    def_cell = "E" + str(excel_row)
                    morph_cell = "F" + str(excel_row)
                    worksheet[pos_cell] = "N/V"
                    worksheet[syll_cell] = "N/V"
                    worksheet[def_cell] = "N/V"
                    worksheet[morph_cell] = "N/V"
                    excel_row += 1
    
                elif found_entries == 0 and len(pos_filters) != 6:
    
                    for x in range(len(pos_filters)):
                        if x != len(pos_filters) - 1:
                            pos_output += pos_filters[x] + ", "
                        else:
                            pos_output += pos_filters[x]
    
                    final_output += "\n\tWarning: no results found for '" + term + "' with filters '" +\
                        pos_output + "'. \n\tYou can try to extend the filtering."
                    log_output += "\n\tWarning: no results for '" + term + "' with filters '" +\
                        pos_output + "'."
    
                    pos_cell = "C" + str(excel_row)
                    syll_cell = "D" + str(excel_row)
                    def_cell = "E" + str(excel_row)
                    morph_cell = "F" + str(excel_row)
                    worksheet[pos_cell] = "N/V"
                    worksheet[syll_cell] = "N/V"
                    worksheet[def_cell] = "N/V"
                    worksheet[morph_cell] = "N/V"
                    excel_row += 1
    
                else:
                    if len(pos_filters) == 6:
                        log_output += "\n\tFilters: NONE" +\
                                      "\n\tEntries found: " + str(found_entries) + "\n"
    
                        final_output += "\n\tFilters: NONE" +\
                                        "\n\tEntries found: " + str(found_entries) + "\n"
                    else:
                        for x in range(len(pos_filters)):
                            if x != len(pos_filters)-1:
                                pos_output += " " + pos_filters[x] + ","
                            else:
                                pos_output += " " + pos_filters[x]
    
                        log_output += "\n\tFilters:" + str(pos_output) + \
                                      "\n\tEntries found: " + str(found_entries) + "\n"
    
                        final_output += "\n\tFilters:" + str(pos_output) + \
                                        "\n\tEntries found: " + str(found_entries) + "\n"
                    final_output += output
                print(final_output)
                """
            worksheet, excel_row, log_output = CA.search_and_output(worksheet=worksheet,
                                                                    excel_row=excel_row,
                                                                    pos_filters=pos_filters,
                                                                    term=term,
                                                                    entries_list=entries_list)

            log = open(log_title, "a", encoding="utf-8")
            log.write("\n\n" + log_output)
            log.close()

            workbook.save(workbook_title)


CA.print_opening(version="Version 2.0")

check_paths()

if check_for_updates_necessary:
    check_for_updates()

formatted_date = CA.get_datetime()

log_name = CA.create_logfile(fd=formatted_date)
wb_name = CA.create_excel(fd=formatted_date)

search_for_terms(log_name, wb_name)

