import sys
import os
import urllib.request
import datetime
import openpyxl
import time
import pandas as pd
from PyQt5.QtWidgets import QApplication, QFileDialog
from openpyxl.styles import Font, Color
from urllib3.exceptions import NameResolutionError, MaxRetryError


def print_opening(version):
    os.system('cls')
    print("\033[32m" + "\n\tWelcome to Morph2Excel - the wiki_morph API!\n\t~ " + version + " ~" + "\033[0m")


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
            print("\n\tDownloading wiki_morph...\n")
            urllib.request.urlretrieve(url, "src/database/wiki_morph.json", reporthook=progress)
            stop = True
        except NameResolutionError or MaxRetryError:
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


def search_and_output(worksheet, excel_row, pos_filters, term, entries_list, print_console_output=True,
                      only_not_found_terms=False, headlines_necessary=True):

    # Set the color for blue entries
    blue_color = "0000FF"
    blue_font = Font(color=Color(rgb=blue_color))

    # Set the color for brown entries
    brown_color = "6E2C00"
    brown_font = Font(color=Color(rgb=brown_color))

    if headlines_necessary:
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
        worksheet[morph_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))

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

        entry = entries_list[x]

        # preparing level 3 information variables
        print_etymology_compounds = False
        etcom_value = None
        sub_affix_values = []
        sub_language_values = []
        decoded_values = []
        sub_sub_pos_values = []
        sub_meaning_values = []
        # cleaned_sub_affix_values = []
        # cleaned_sub_language_values = []
        # cleaned_decoded_values = []
        # cleaned_sub_sub_pos_values = []
        # cleaned_sub_meaning_values = []

        if entry["Word"] == term and entry["PoS"] in pos_filters:
            found_entries += 1

            if not only_not_found_terms:
                keys = list(entry.keys())

                # Data Structure Level 1 ---------------------------------------------------------------------

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

                output += "\n\t" + str(found_entries) + ")" + \
                          "\t" + str(keys[1]) + ": " + str(pos_value) + "\n" + \
                          "\t\t" + str(keys[2]) + ": " + str(syllables_value) + "\n" + \
                          "\t\t" + str(keys[3]) + ": " + str(definition_value) + "\n" + \
                          "\t\t" + str(keys[4]) + ": " + str(morphemes_value) + "\n"

                # Data Structure Level 2 ---------------------------------------------------------------------

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

                    worksheet[affix_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
                    worksheet[lang_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
                    worksheet[sub_pos_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
                    worksheet[mean_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
                    worksheet[etcom_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))

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

                        worksheet[affix_cell].font = blue_font
                        worksheet[lang_cell].font = blue_font
                        worksheet[pos_cell].font = blue_font
                        worksheet[mean_cell].font = blue_font

                        excel_row += 1

                        if etcom_value is not None:

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

                            print_etymology_compounds = True

                    if print_etymology_compounds:

                        # Data Structure Level 3 -------------------------------------------------------------

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

                        sub_affix_Hcell = 'J' + str(excel_row)
                        sub_lang_Hcell = 'K' + str(excel_row)
                        decoded_Hcell = 'L' + str(excel_row)
                        sub_sub_pos_Hcell = 'M' + str(excel_row)
                        sub_meaning_Hcell = 'N' + str(excel_row)

                        worksheet[sub_affix_Hcell] = 'Affix'
                        worksheet[sub_lang_Hcell] = 'Language'
                        worksheet[decoded_Hcell] = 'Decoded'
                        worksheet[sub_sub_pos_Hcell] = 'PoS'
                        worksheet[sub_meaning_Hcell] = 'Meanings'

                        worksheet[sub_affix_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))
                        worksheet[sub_lang_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))
                        worksheet[decoded_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))
                        worksheet[sub_sub_pos_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))
                        worksheet[sub_meaning_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))

                        for x in range(len(cleaned_sub_affix_values)):
                            excel_row += 1

                            sub_affix_cell = "J" + str(excel_row)
                            sub_language_cell = "K" + str(excel_row)
                            decoded_cell = "L" + str(excel_row)
                            sub_sub_pos_cell = "M" + str(excel_row)
                            sub_meaning_cell = "N" + str(excel_row)

                            worksheet[sub_affix_cell].font = brown_font
                            worksheet[sub_language_cell].font = brown_font
                            worksheet[decoded_cell].font = brown_font
                            worksheet[sub_sub_pos_cell].font = brown_font
                            worksheet[sub_meaning_cell].font = brown_font

                            worksheet[sub_affix_cell] = str(cleaned_sub_affix_values[x])
                            worksheet[sub_language_cell] = str(cleaned_sub_language_values[x])
                            worksheet[decoded_cell] = str(cleaned_decoded_values[x])
                            worksheet[sub_sub_pos_cell] = str(cleaned_sub_sub_pos_values[x])
                            worksheet[sub_meaning_cell] = str(cleaned_sub_meaning_values[x])

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

        final_output += "\n\tWarning: no results found for '" + term + "' with filters '" + \
                        pos_output + "'. \n\tYou can try to extend the filtering."
        log_output += "\n\tWarning: no results for '" + term + "' with filters '" + \
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
    if print_console_output:
        print(final_output)

    return worksheet, excel_row, log_output


def select_excel_file():
    # Path to your Excel file
    # excel_file = r'C:\Users\tillp\Desktop\Morph2Excel - Version 2.0c\output\M2E_Output_(06_06_2023_(14_17_55)).xlsx'

    # Create a QApplication instance
    app = QApplication([])

    # Open file dialog to choose the Excel file
    excel_file, _ = QFileDialog.getOpenFileName(None, "Select Excel File", "./data", "Excel Files (*.xlsx)")

    return excel_file


def autoscan(excel_file):
    # Read the Excel file
    data = pd.read_excel(excel_file)

    # Get the values from the first column (assuming it's named 'mot_lpd')
    terms = data.iloc[:, 0].dropna().tolist()
    terms = list(set(terms))    # eliminates duplicates
    terms = sorted(terms)       # alphabetical order (ascending)

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

