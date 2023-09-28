import sys
import os
import urllib.request
import datetime
import openpyxl
import time
import pandas as pd
from PyQt5.QtWidgets import QApplication, QFileDialog
from openpyxl.styles import Font, Color
from playsound import playsound
from urllib3.exceptions import NameResolutionError, MaxRetryError


def print_opening(version):
    os.system('cls')
    print("\033[32m" + "\n\tMorph2Excel ~ Version " + version + "\033[0m")


def print_opening_extended(version):
    os.system('cls')
    print("\033[32m" + "\n\tMorph2Excel ~ Version " + version + "\033[0m")
    playsound("src/data/GUI_sound/Signal.mp3")
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

def print_exit_without_download():
    os.system('cls')
    print("\n\tDownload will not start.")
    time.sleep(1.5)
    os.system('cls')
    print("\n\tNotice: You have to download the database another time to use this program.")
    time.sleep(5)
    os.system('cls')
    print("\n\tProgram will now terminate. For downloading wiki_morph you can start it again.")
    time.sleep(5)
    sys.exit(0)


def get_datetime():
    now = datetime.datetime.now()
    date_format = "%d_%m_%Y_(%H_%M_%S)"
    formatted_date = now.strftime(date_format)
    return formatted_date


def create_logfile(fd):
    log_title = "output/log_files/M2E_Log_(" + str(fd) + ").txt"
    with open(log_title, "w") as log:
        log.write("Morph2Excel Log from " + str(fd))
    log.close()

    return log_title


def create_excel(fd):

    workbook_title = "output/excel_files/M2E_Output_(" + str(fd) + ").xlsx"
    # Eine neue Excel-Datei erstellen
    workbook = openpyxl.Workbook()

    workbook.save(workbook_title)

    return workbook_title


def create_comparison_result_excel(fd):

    workbook_title = "output/excel_files/M2E_Comparison_Results_(" + str(fd) + ").xlsx"
    # Eine neue Excel-Datei erstellen
    workbook = openpyxl.Workbook()

    workbook.save(workbook_title)

    return workbook_title


def download_database(url):
    def progress(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write("\r" + "\t[%-100s] %d%%" % ("#" * percent, percent))
        sys.stdout.flush()

    stop = False
    normal = True

    while not stop:
        try:
            os.system('cls')
            print_opening(version="Version 2.2c")
            print("\n\tDownloading wiki_morph...\n")
            urllib.request.urlretrieve(url, "src/database/wiki_morph.json", reporthook=progress)
            stop = True
        except NameResolutionError or MaxRetryError:
            print_opening(version="Version 2.2c")
            print("\n\tDownload not possible: No internet connection!"
                  "\n\tYou can try again by pressing enter."
                  '\n\tAlternatively you can end the program by typing "exit!".')
            normal = False
            i = input("\n\t")
            if i == "exit!" or i == "exit":
                stop = True

    return normal


def show_instructions():
    time.sleep(1)
    os.system('cls')
    print("\n\tInstructions:")
    time.sleep(.25)
    print("\n\t1) Please type in the term you want to SEARCH and press Enter.")
    time.sleep(.25)
    print("\t2) You are free to repeat this procedure till you end this program.")
    time.sleep(.25)
    print("\t3) You can only SEARCH for one term at the same time.")
    time.sleep(.25)
    print("\t4) To END this program you can type in 'exit!'.")
    time.sleep(.25)
    print("\t5) Results are saved into an excel file (.xlsx),"
          " which will open automatically after the end of the program.")
    time.sleep(.25)
    print("\t6) There is also a short logfile (.txt), which covers the search history.")
    time.sleep(.25)
    print("\t7) To FILTER your results you can define the part of speech characteristics of the term as follows:"
          '\n\n\t\tgeneral:     "term:PoS"'
          '\n\t\texamples:    "cool:Noun"  /  "cool:Adjective"  /  "hide:Verb"  /  "hide:Adjective:Adverb"'
          '\n\n\t\tThere are the following pos types you can filter on: '
          '(Noun, Verb, Adverb, Adjective, Preposition, Phrase).'
          '\n\t\t\tYou can search for more than one pos type by connecting them via ":" (see last example).')
    time.sleep(.25)
    print('\n\t8) By typing in "s!" you can enter the new scan mode. '
          '\n\t\tHere you are free to select an excel file in the directory, which will be scanned for possible terms. '
          '\n\t\tThese terms will automatically be searched in the wiki_morph database. '
          '\n\t\tThe generated output contains all the morphological information as usual. '
          '\n\t\tYou can use the manual search before or after the automatic scan. '
          '\n\t\tYou can also execute the automatic scan several times in a row. '
          '\n\t\tThese ways the respective outputs are combined in one final output table. '
          '\n\t\tFor separating the outputs and getting different tables you need to end\n\t\tand restart the program'
          ' and plan the scans / manual searches respectively. '
          '\n\t\tHint: soon there will be a version update which allows outputting and cleaning the cache on the flow.')
    time.sleep(.25)
    print('\t9) You can find the outputs in the folder "data".')


def show_version_description():
    time.sleep(1)
    os.system('cls')
    print("\n\tWhat´s new in version 2.1?")
    time.sleep(.25)
    print("\n\t1) The instructions and this version description are new features,\n\t\tseparated from the main function"
          " of searching terms in the database.")
    time.sleep(.25)
    print("\t2) This version introduces Part of Speech (PoS) filters, as described in the instructions.")
    time.sleep(.25)
    print("\t3) The excel output has got a new structure since the program is now able\n\t\tto capture morphological "
          "information up to the database´s maximum depth \n\t\tof three levels (etymology compound level).")
    time.sleep(.25)
    print("\t4) Smaller improvements on the function for automatic updating of the database.")
    time.sleep(.25)
    print("\t5) There is a new consistency test at the beginning of the program to proof\n\t\twhether the last download"
          " of the database was either successful or has been interrupted. "
          "\n\t\tThis consistency data is saved to and managed "
          "by the file 'savedata.txt' \n\t\tand an external script savedata_manager.py.")
    time.sleep(.25)
    print("\t6) The created excel file will now open automatically after the program terminated correctly.")
    time.sleep(.25)
    print("\t7) General revision of the displayed text, supplemented by the addition of data size information.")
    time.sleep(.25)
    print("\t8) There is a new automatic scan mode, "
          "\n\t\twhich allows you to select an excel file in the directory. "
          "\n\t\tThe first column of this file will be scanned and for every term it contains, "
          "\n\t\tM2E will search for the respective etymology "
          "\n\t\tand create an output file containing all the information automatically.")
    time.sleep(.25)


def print_headlines(worksheet, excel_row):

    blue_color = "0000FF"
    brown_color = "6E2C00"

    term_Hcell = 'A' + str(excel_row)
    filter_Hcell = 'B' + str(excel_row)
    pos_Hcell = 'C' + str(excel_row)
    syll_Hcell = 'D' + str(excel_row)
    def_Hcell = 'E' + str(excel_row)
    affix_Hcell = 'F' + str(excel_row)
    lang_Hcell = 'G' + str(excel_row)
    sub_pos_Hcell = 'H' + str(excel_row)
    mean_Hcell = 'I' + str(excel_row)
    sub_affix_Hcell = 'J' + str(excel_row)
    sub_lang_Hcell = 'K' + str(excel_row)
    decoded_Hcell = 'L' + str(excel_row)
    sub_sub_pos_Hcell = 'M' + str(excel_row)
    sub_meaning_Hcell = 'N' + str(excel_row)

    worksheet[term_Hcell] = 'Term'
    worksheet[filter_Hcell] = 'Filter'
    worksheet[pos_Hcell] = 'PoS'
    worksheet[syll_Hcell] = 'Syllables'
    worksheet[def_Hcell] = 'Definition'
    worksheet[affix_Hcell] = 'Affix'
    worksheet[lang_Hcell] = 'Language'
    worksheet[sub_pos_Hcell] = 'PoS'
    worksheet[mean_Hcell] = 'Meaning'
    worksheet[sub_affix_Hcell] = 'Affix'
    worksheet[sub_lang_Hcell] = 'Language'
    worksheet[decoded_Hcell] = 'Decoded'
    worksheet[sub_sub_pos_Hcell] = 'PoS'
    worksheet[sub_meaning_Hcell] = 'Meanings'

    worksheet[term_Hcell].font = Font(bold=True)
    worksheet[filter_Hcell].font = Font(bold=True)
    worksheet[pos_Hcell].font = Font(bold=True)
    worksheet[syll_Hcell].font = Font(bold=True)
    worksheet[def_Hcell].font = Font(bold=True)
    worksheet[affix_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
    worksheet[lang_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
    worksheet[sub_pos_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
    worksheet[mean_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
    worksheet[sub_affix_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))
    worksheet[sub_lang_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))
    worksheet[decoded_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))
    worksheet[sub_sub_pos_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))
    worksheet[sub_meaning_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))

    excel_row += 1
    return worksheet, excel_row


def search_and_output(worksheet, excel_row, pos_filters, term, entries_list,
                      only_found_terms, only_not_found_terms, multiline_output, output_detail_level):

    # Set the color for blue entries
    blue_color = "0000FF"
    blue_font = Font(color=Color(rgb=blue_color))

    # Set the color for brown entries
    brown_color = "6E2C00"
    brown_font = Font(color=Color(rgb=brown_color))

    # defining term print function
    # only desired terms will be printed (depends on chosen 3 way output option as you can see below)
    def print_term():
        term_cell = "A" + str(excel_row)
        worksheet[term_cell] = term
        filter_cell = "B" + str(excel_row)
        if len(pos_filters) == 6:
            worksheet[filter_cell] = "NONE"
        else:
            worksheet[filter_cell] = str(pos_filters)

    # print control in dependency of chosen 3 way output option
    found_entries = 0
    for x in range(len(entries_list)):
        entry = entries_list[x]
        if entry["Word"] == term and entry["PoS"] in pos_filters:
            found_entries += 1

    if found_entries != 0 and not only_not_found_terms:
        print_term()
    elif found_entries == 0 and not only_found_terms:
        print_term()

    found_entries = 0

    log_output = "\t------------------------------------------------------------\n\n\tWord: " + term
    final_output = "\t------------------------------------------------------------\n\n\tWord: " + term
    output = ""
    pos_output = ""

    # preparing functions for printing the values
    # useful to not repeat every cell definition before setting the values
    def set_level_1_cell_data(current_excel_row, pos, syllables, definition):
        pos_cell = "C" + str(current_excel_row)
        syll_cell = "D" + str(current_excel_row)
        def_cell = "E" + str(current_excel_row)

        worksheet[pos_cell] = str(pos)
        worksheet[syll_cell] = str(syllables)
        worksheet[def_cell] = str(definition)

    def set_level_2_cell_data(current_excel_row, affix, language, sub_pos, meaning):

        affix_cell = "F" + str(current_excel_row)
        lang_cell = "G" + str(current_excel_row)
        pos_cell = "H" + str(current_excel_row)
        mean_cell = "I" + str(current_excel_row)

        worksheet[affix_cell].font = blue_font
        worksheet[lang_cell].font = blue_font
        worksheet[pos_cell].font = blue_font
        worksheet[mean_cell].font = blue_font

        worksheet[affix_cell] = str(affix)
        worksheet[lang_cell] = str(language)
        worksheet[pos_cell] = str(sub_pos)
        worksheet[mean_cell] = str(meaning)

    def set_level_3_cell_data(current_excel_row, sub_affix, sub_language, decoded, sub_sub_pos, sub_meaning):

        sub_affix_cell = "J" + str(current_excel_row)
        sub_language_cell = "K" + str(current_excel_row)
        decoded_cell = "L" + str(current_excel_row)
        sub_sub_pos_cell = "M" + str(current_excel_row)
        sub_meaning_cell = "N" + str(current_excel_row)

        worksheet[sub_affix_cell].font = brown_font
        worksheet[sub_language_cell].font = brown_font
        worksheet[decoded_cell].font = brown_font
        worksheet[sub_sub_pos_cell].font = brown_font
        worksheet[sub_meaning_cell].font = brown_font

        worksheet[sub_affix_cell] = str(sub_affix)
        worksheet[sub_language_cell] = str(sub_language)
        worksheet[decoded_cell] = str(decoded)
        worksheet[sub_sub_pos_cell] = str(sub_sub_pos)
        worksheet[sub_meaning_cell] = str(sub_meaning)

    # search term ---------------------------------------------------------------------------------------------
    for x in range(len(entries_list)):

        entry = entries_list[x]

        if entry["Word"] == term and entry["PoS"] in pos_filters:
            found_entries += 1

            if not only_not_found_terms:

                keys = list(entry.keys())

                # Data Structure Level 1 ---------------------------------------------------------------------

                pos_value = entry[keys[1]]
                syllables_value = entry[keys[2]]
                definition_value = entry[keys[3]]
                morphemes_value = entry[keys[4]]

                set_level_1_cell_data(
                    excel_row, pos_value, syllables_value, definition_value)

                output += "\n\t" + str(found_entries) + ")" + \
                          "\t" + str(keys[1]) + ": " + str(pos_value) + "\n" + \
                          "\t\t" + str(keys[2]) + ": " + str(syllables_value) + "\n" + \
                          "\t\t" + str(keys[3]) + ": " + str(definition_value) + "\n" + \
                          "\t\t" + str(keys[4]) + ": " + str(morphemes_value) + "\n"

                # Data Structure Level 2 ---------------------------------------------------------------------

                if output_detail_level >= 2:

                    if morphemes_value is None:
                        set_level_2_cell_data(excel_row, affix="N/V", language="N/V", sub_pos="N/V", meaning="N/V")
                        excel_row += 1

                    else:
                        for respective_morph_dict in morphemes_value:

                            if multiline_output:
                                excel_row += 1

                            morphemes_sub_values = list(respective_morph_dict.values())

                            affix_value = morphemes_sub_values[0]
                            language_value = morphemes_sub_values[1]
                            sub_pos_value = morphemes_sub_values[2]
                            meaning_value = morphemes_sub_values[3]
                            etcom_value = morphemes_sub_values[4]

                            set_level_2_cell_data(
                                excel_row, affix_value, language_value, sub_pos_value, meaning_value)

                            # Data Structure Level 3 -------------------------------------------------------------
                            if output_detail_level == 3:

                                if multiline_output:
                                    excel_row += 1

                                if etcom_value is None:
                                    set_level_3_cell_data(excel_row, sub_affix="N/V", sub_language="N/V", decoded="N/V",
                                                          sub_sub_pos="N/V", sub_meaning="N/V")
                                    excel_row += 1

                                else:

                                    sub_affix_values = []
                                    sub_language_values = []
                                    decoded_values = []
                                    sub_sub_pos_values = []
                                    sub_meaning_values = []

                                    for respective_etcom_dict in etcom_value:
                                        etcom_sub_values = list(respective_etcom_dict.values())

                                        sub_affix_value = etcom_sub_values[0]
                                        sub_language_value = etcom_sub_values[1]
                                        decoded_value = etcom_sub_values[2]
                                        sub_sub_pos_value = etcom_sub_values[3]
                                        sub_meaning_value = etcom_sub_values[4]

                                        sub_affix_values.append(sub_affix_value)
                                        sub_language_values.append(sub_language_value)
                                        decoded_values.append(decoded_value)
                                        sub_sub_pos_values.append(sub_sub_pos_value)
                                        sub_meaning_values.append(sub_meaning_value)

                                    # the lists with all collected information are prepared now
                                    # next step is to filter out redundant (duplicate) information over all
                                    # five information types. so we connect them in a single list:

                                    hyper_list = []
                                    for v in range(len(sub_affix_values)):
                                        value = str(sub_affix_values[v]) + "[/]"
                                        value += str(sub_language_values[v]) + "[/]"
                                        value += str(decoded_values[v]) + "[/]"
                                        value += str(sub_sub_pos_values[v]) + "[/]"
                                        value += str(sub_meaning_values[v])
                                        hyper_list.append(value)

                                    # eliminating duplicates and sorting alphabetical ascending
                                    hyper_list = list(set(hyper_list))
                                    hyper_list = sorted(hyper_list)

                                    # transforming back to separated lists
                                    cleaned_sub_affix_values = []
                                    cleaned_sub_language_values = []
                                    cleaned_decoded_values = []
                                    cleaned_sub_sub_pos_values = []
                                    cleaned_sub_meaning_values = []

                                    for x in range(len(hyper_list)):
                                        values = hyper_list[x].split("[/]")
                                        cleaned_sub_affix_values.append(values[0])
                                        cleaned_sub_language_values.append(values[1])
                                        cleaned_decoded_values.append(values[2])
                                        cleaned_sub_sub_pos_values.append(values[3])
                                        cleaned_sub_meaning_values.append(values[4])

                                    for x in range(len(cleaned_sub_affix_values)):

                                        set_level_3_cell_data(
                                            excel_row, cleaned_sub_affix_values[x], cleaned_sub_language_values[x],
                                            cleaned_decoded_values[x], cleaned_sub_sub_pos_values[x],
                                            cleaned_sub_meaning_values[x])

                                        excel_row += 1

    if found_entries == 0 and len(pos_filters) == 6:
        final_output += "\n\tWarning: database has no entry for '" + term + "'."
        log_output += "\n\tWarning: no entry for '" + term + "'."

        if not only_found_terms:
            set_level_1_cell_data(excel_row, pos="N/V", syllables="N/V", definition="N/V")
            set_level_2_cell_data(excel_row, affix="N/V", language="N/V", sub_pos="N/V", meaning="N/V")
            set_level_3_cell_data(excel_row, sub_affix="N/V", sub_language="N/V", decoded="N/V",
                                  sub_sub_pos="N/V", sub_meaning="N/V")
            excel_row += 1

    elif found_entries == 0 and len(pos_filters) != 6:

        for x in range(len(pos_filters)):
            if x != len(pos_filters) - 1:
                pos_output += pos_filters[x] + ", "
            else:
                pos_output += pos_filters[x]

        final_output += "\n\tWarning: no results found for '" + term + "' with filters '" + \
                        pos_output + "'. \n\tYou can try to extend the filtering."
        log_output += "\n\tWarning: no results for '" + term + "' with filters '" + \
                      pos_output + "'."

        if not only_found_terms:
            set_level_1_cell_data(excel_row, pos="N/V", syllables="N/V", definition="N/V")
            set_level_2_cell_data(excel_row, affix="N/V", language="N/V", sub_pos="N/V", meaning="N/V")
            set_level_3_cell_data(excel_row, sub_affix="N/V", sub_language="N/V", decoded="N/V",
                                  sub_sub_pos="N/V", sub_meaning="N/V")
            excel_row += 1

    else:
        if len(pos_filters) == 6:
            log_output += "\n\tFilters: NONE" + \
                          "\n\tEntries found: " + str(found_entries) + "\n"

            final_output += "\n\tFilters: NONE" + \
                            "\n\tEntries found: " + str(found_entries) + "\n"
        else:
            for x in range(len(pos_filters)):
                if x != len(pos_filters) - 1:
                    pos_output += " " + pos_filters[x] + ","
                else:
                    pos_output += " " + pos_filters[x]

            log_output += "\n\tFilters:" + str(pos_output) + \
                          "\n\tEntries found: " + str(found_entries) + "\n"

            final_output += "\n\tFilters:" + str(pos_output) + \
                            "\n\tEntries found: " + str(found_entries) + "\n"
        final_output += output

    return worksheet, excel_row, log_output


def select_excel_file():
    # Path to your Excel file
    # excel_file = r'C:\Users\tillp\Desktop\Morph2Excel - Version 2.0c\output\M2E_Output_(06_06_2023_(14_17_55)).xlsx'

    # Create a QApplication instance
    app = QApplication([])

    # Open file dialog to choose the Excel file
    excel_file, _ = QFileDialog.getOpenFileName(None, "Select Excel File", "./data", "Excel Files (*.xlsx)")

    return excel_file


def autoscan(excel_file, duplicates=False, abc=True, abc_ascending=True):
    # Read the Excel file
    data = pd.read_excel(excel_file)

    # Get the values from the first column (assuming it's named 'mot_lpd')
    terms = data.iloc[:, 0].dropna().tolist()
    if not duplicates:
        terms = list(set(terms))    # eliminates duplicates
    if abc:
        if abc_ascending:
            terms = sorted(terms)       # alphabetical order (ascending)
        else:
            terms = sorted(terms, reverse=True)     # alphabetical order (descending)

    return terms


def write_comparison_result_excel(worksheet, file_1, file_2, list_of_terms_1, list_of_terms_2, common_terms_list):
    excel_row = 1

    term_Hcell = 'A' + str(excel_row)
    property_Hcell = 'B' + str(excel_row)
    file_Hcell = 'C' + str(excel_row)

    worksheet[term_Hcell] = 'Term'
    worksheet[property_Hcell] = 'Property'
    worksheet[file_Hcell] = 'From File'

    blue_color = "0000FF"
    brown_color = "6E2C00"
    green_color = "00FF00"
    yellow_color = "FFFF00"

    worksheet[term_Hcell].font = Font(bold=True)
    worksheet[property_Hcell].font = Font(bold=True)
    worksheet[file_Hcell].font = Font(bold=True)
    excel_row += 1

    # saving uniques from file 1
    for term in list_of_terms_1:

        term_Cell = 'A' + str(excel_row)
        worksheet[term_Cell] = term
        worksheet[term_Cell].font = Font(color=Color(rgb=brown_color))

        property_Cell = 'B' + str(excel_row)
        worksheet[property_Cell] = "unique"
        worksheet[property_Cell].font = Font(color=Color(rgb=brown_color))

        file_Cell = 'C' + str(excel_row)
        worksheet[file_Cell] = "File 1: " + file_1
        worksheet[file_Cell].font = Font(color=Color(rgb=brown_color))

        excel_row += 1

    # saving uniques from file 2
    for term in list_of_terms_2:
        term_Cell = 'A' + str(excel_row)
        worksheet[term_Cell] = term
        worksheet[term_Cell].font = Font(color=Color(rgb=blue_color))

        property_Cell = 'B' + str(excel_row)
        worksheet[property_Cell] = "unique"
        worksheet[property_Cell].font = Font(color=Color(rgb=blue_color))

        file_Cell = 'C' + str(excel_row)
        worksheet[file_Cell] = "File 2: " + file_2
        worksheet[file_Cell].font = Font(color=Color(rgb=blue_color))

        excel_row += 1

    # saving commons from both files
    for term in common_terms_list:
        term_Cell = 'A' + str(excel_row)
        worksheet[term_Cell] = term
        # worksheet[term_Cell].font = Font(color=Color(rgb=yellow_color))

        property_Cell = 'B' + str(excel_row)
        worksheet[property_Cell] = "common"
        # worksheet[property_Cell].font = Font(color=Color(rgb=yellow_color))

        file_Cell = 'C' + str(excel_row)
        worksheet[file_Cell] = "File 1: " + file_1 + "   +   File 2: " + file_2
        # worksheet[file_Cell].font = Font(color=Color(rgb=yellow_color))

        excel_row += 1

    return worksheet


def prepare_settings_display(auto_update, term_output_diplomacy, oneline_output_format,
                             headline_printing, alphabetical_output, abc_output_ascending,
                             output_detail_level):

    auto_update_option = "\n\t1. Search for database updates automatically:\t\t\t\t\t"
    term_output_diplomacy_option = "\t2. Consider following terms in output:\t\t\t\t\t\t\t"
    oneline_output_format_option = "\t3. Output format:\t\t\t\t\t\t\t\t\t\t\t"
    headline_printing_option = "\t4. Repeat headline printing in output:\t\t\t\t\t\t\t"
    alphabetical_output_option = "\t5. Print output in alphabetical order (only in scan mode):\t\t"
    output_detail_level_option = "\t6. Output detail level:\t\t\t\t\t\t\t\t\t\t"
    # auto_scan_filters_option = "7. "

    auto_update_option += "off\t(1/2)" if auto_update == 0 else "on\t(2/2)"
    if term_output_diplomacy == 0:
        term_output_diplomacy_option += "only found terms\t\t(1/3)"
    elif term_output_diplomacy_option == 1:
        term_output_diplomacy_option += "only not found terms\t(2/3)"
    else:
        term_output_diplomacy_option += "all searched terms\t(3/3)"
    oneline_output_format_option += "one-line\t(1/2)" if oneline_output_format else "multi-line\t(2/2)"
    if headline_printing == 0:
        headline_printing_option += "off, only at beginning of output document\t(1/3)"
    elif headline_printing_option == 1:
        headline_printing_option += "after every scan (only in scan mode, else off)\t(2/3)"
    else:
        headline_printing_option += "after every term\t(3/3)"
    if alphabetical_output and abc_output_ascending:
        alphabetical_output_option += "on (ascending)\t(1/3)"
    elif alphabetical_output and not abc_output_ascending:
        alphabetical_output_option += "on (descending)\t(2/3)"
    else:
        alphabetical_output_option += "off\t(1/3)"
    if output_detail_level == 0:
        output_detail_level_option += "Level 1\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t" \
                                      "only term data\t(1/3)"
    elif output_detail_level == 1:
        output_detail_level_option += "Level 1+2 (black,blue): term + morphology data\t(2/3)"
    else:
        output_detail_level_option += "Level 1+2+3 (black,blue,brown): term, morphology + etymology data\t(3/3)"

    return [auto_update_option, term_output_diplomacy_option, oneline_output_format_option,
            headline_printing_option, alphabetical_output_option, output_detail_level_option]


def display_settings(setting, current_var, current_var_2=""):
    if setting == 1:
        print("\n\t~ Settings Menu ~"
              "\n\n\tSetting 1/6: Automatic Database Updates"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tThe program will automatically search for wiki_morph updates "
              "\n\tbefore loading the installed version of the database. "
              "\n\tIf there is a new version you will have the option to download it."
              "\n\tBut the search itself may take a few seconds every time the program is started.")
        if current_var == 0:
            print("\n\tOptions:\n\t\t\t\t1. on\n\t\t\t->\t2. off")
        else:
            print("\n\tOptions:\n\t\t\t->\t1. on\n\t\t\t\t2. off")
    elif setting == 2:
        print("\n\t~ Settings Menu ~"
              "\n\n\tSetting 2/6: Term Output Diplomacy"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tDecide, which of the terms you searched shall be considered in the output."
              "\n\tThis only affects the excel table. The log_file.txt cannot be changed.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t->\t1. only found terms"
                  "\n\t\t\t\t2. only not found terms\n\t\t\t\t3. all searched terms")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. only found terms"
                  "\n\t\t\t->\t2. only not found terms\n\t\t\t\t3. all searched terms")
        else:
            print("\n\tOptions:\n\t\t\t\t1. only found terms"
                  "\n\t\t\t\t2. only not found terms\n\t\t\t->\t3. all searched terms")
    elif setting == 3:
        print("\n\t~ Settings Menu ~"
              "\n\n\tSetting 3/6: Output Format"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tThe excel output can either be structured with one-line or multiline format."
              "\n\tMulti-line format is more readable and provides a better overview for the user."
              "\n\tOne-line format is recommended in case of further processing of the output data, "
              "\n\tsince it is easier to access data which is covered in only one line.")
        if current_var:
            print("\n\tOptions:\n\t\t\t->\t1. one-line\n\t\t\t\t2. multi-line")
        else:
            print("\n\tOptions:\n\t\t\t\t1. one-line\n\t\t\t->\t2. multi-line")
    elif setting == 4:
        print("\n\t~ Settings Menu ~"
              "\n\n\tSetting 4/6: Headline Printing"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tThe program is able to repeat the printing of a standardized headline for the"
              "\n\tresulting output excel file."
              "\n\tHere you can decide, how often a headline shall be printed.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t->\t1. only at top of excel / no repeat"
                  "\n\t\t\t\t2. for every new document scanned in"
                  "\n\t\t\t\t\t(note: only in scan mode; for manual search option 1 will be used)"
                  "\n\t\t\t\t3. for every new term printed")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. only at top of excel / no repeat"
                  "\n\t\t\t->\t2. for every new document scanned in"
                  "\n\t\t\t\t\t(note: only in scan mode; for manual search option 1 will be used)"
                  "\n\t\t\t\t3. for every new term printed")
        else:
            print("\n\tOptions:\n\t\t\t\t1. only at top of excel / no repeat"
                  "\n\t\t\t\t2. for every new document scanned in"
                  "\n\t\t\t\t\t(note: only in scan mode; for manual search option 1 will be used)"
                  "\n\t\t\t->\t3. for every new term printed")
    elif setting == 5:
        print("\n\t~ Settings Menu ~"
              "\n\n\tSetting 5/6: Alphabetical Output Order"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tDecide, if the output shall be structured in alphabetical order."
              "\n\tNote: For the moment this functionality is only available for auto scan mode."
              "\n\tManual search output will not be structured anyway.")
        if current_var and current_var_2:
            print("\n\tOptions:\n\t\t\t->\t1. alphabetical, ascending"
                  "\n\t\t\t\t2. alphabetical, descending"
                  "\n\t\t\t\t3. non-alphabetical")
        elif current_var and not current_var_2:
            print("\n\tOptions:\n\t\t\t\t1. alphabetical, ascending"
                  "\n\t\t\t->\t2. alphabetical, descending"
                  "\n\t\t\t\t3. non-alphabetical")
        else:
            print("\n\tOptions:\n\t\t\t\t1. alphabetical, ascending"
                  "\n\t\t\t\t2. alphabetical, descending"
                  "\n\t\t\t->\t3. non-alphabetical")
    elif setting == 6:
        print("\n\t~ Settings Menu ~"
              "\n\n\tSetting 6/6: Output Detail Level"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tFor every term entry in the database there are three levels of information:"
              "\n\tThe basic term data (Level 1, output print color: black), "
              "\n\tthe morphology data (Level 2, output print color: blue) and "
              "\n\tetymology compound data (Level 3, output print color brown)."
              "\n\tHere you can set the depht of the output information according to these levels.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t->\t1. Level 1: only term data"
                  "\n\t\t\t\t2. Level 2: term data + morphology data"
                  "\n\t\t\t\t3. Level 3: term data + morphology data + etymology data")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. Level 1: only term data"
                  "\n\t\t\t->\t2. Level 2: term data + morphology data"
                  "\n\t\t\t\t3. Level 3: term data + morphology data + etymology data")
        else:
            print("\n\tOptions:\n\t\t\t\t1. Level 1: only term data"
                  "\n\t\t\t\t2. Level 2: term data + morphology data"
                  "\n\t\t\t->\t3. Level 3: term data + morphology data + etymology data")

