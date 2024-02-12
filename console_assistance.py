import sys
import os
import urllib.request
import datetime
import openpyxl
import time
import pandas as pd
import re

import notification_sound_player as NSP
from PyQt5.QtWidgets import QApplication, QFileDialog
from openpyxl.styles import Font, Color

import savedata_manager as SDM


def is_valid_input(i):
    if i == "":
        return False
    pos = []
    if ":" in i:
        pos = i.split(":")
        i = pos[0]
        pos.pop(0)

    allowed_inputs = ['exit!', 'set!', 's!', 'i!', 'v!', 'c!', '?', ]
    for char in i:
        if not (char.isalpha() or i in allowed_inputs):
            print("\n\t\033[91mWarning:\033[0m Invalid input!"
                  "\n\n\tFor typing in the term please use standard characters only. No numbers."
                  "\n\tSpecial signs are only allowed as described in the instructions.")
            time.sleep(8)
            return False

    allowed_pos_filters = ['noun', 'verb', 'adjective', 'adverb', 'preposition', 'phrase']
    for filter in pos:
        if not filter in allowed_pos_filters:
            print("\n\t\033[91mWarning:\033[0m Invalid input!"
                  "\n\n\tPlease use valid pos filters only."
                  "\n\tMore information can be found in the instructions.")
            time.sleep(8)
            return False

    return True


def is_valid_scan(i):
    if i == "":
        return False

    for char in i:
        if not char.isalpha():
            return False

    return True


def measure_time(start, end, search=True):
    # Zeitdifferenz in Minuten und Sekunden berechnen
    elapsed_time_seconds = end - start
    elapsed_minutes = int(elapsed_time_seconds // 60)
    elapsed_seconds = int(elapsed_time_seconds % 60)
    elapsed_seconds_formatted = "{:02d}".format(elapsed_seconds)
    if search:
        return (f"\t\033[92mTime needed for search:\033[0m {elapsed_minutes} minutes and "
                f"{elapsed_seconds_formatted} seconds.")
    else:
        return (f"\t\033[92mTime needed for scan:\033[0m "
                f"{elapsed_minutes} minutes and {elapsed_seconds_formatted} seconds.")


def print_opening(version):
    os.system('cls')
    print("\033[92m" + "\n\tMorph2Excel ~ Version " + version + "\033[0m")


def print_main_menu(version):
    os.system('cls')
    print("\033[92m" + "\n\tMorph2Excel ~ Version " + version + "\033[0m"
          "\n\n\t\033[92mMain Menu\033[0m"
          "\n\t\033[92m----------------------------------------------------------------\033[0m")

    NSP.play_mp3("./src/data/GUI_sound/Signal.mp3")

    print(
        "\n\tManual search mode is prepared."
        "\n\tYou can now search for terms."
    )
    time.sleep(.5)
    os.system('cls')
    print("\033[92m" + "\n\tMorph2Excel ~ Version " + version + "\033[0m"
          "\n\n\t\033[92mMain Menu\033[0m"
          "\n\t\033[92m----------------------------------------------------------------\033[0m")
    print(
        "\n\tManual search mode is prepared."
        "\n\tYou can now search for terms."

        '\n\n\t\033[97mAlternative search modes:\033[0m'
        '\n'
        '\n'

        '\n\n\t\033[97mFurther options:\033[0m'
        '\n'
        '\n'
        '\n'
        '\n'

        '\n\n\t\033[97mCurrent settings:\033[0m',
        '\n'
        '\n'
        '\n'
        '\n'
        '\n'
        '\n'
        '\n'

        '\n\n\tHint: If you want to \033[92mdisplay this overview again\033[0m type \033[92m?\033[0m instead of a term.'
    )
    time.sleep(1)
    os.system('cls')
    print("\033[92m" + "\n\tMorph2Excel ~ Version " + version + "\033[0m"
          "\n\n\t\033[92mMain Menu\033[0m"
          "\n\t\033[92m----------------------------------------------------------------\033[0m")
    print(
        "\n\tManual search mode is prepared."
        "\n\tYou can now search for terms."

        '\n\n\t\033[97mAlternative search modes:\033[0m'
        '\n\tI)  For \033[38;5;130mAutomatic scan mode\033[0m type \033[38;5;130ms!\033[0m instead of a term.'
        '\n\tII) For \033[94mComparison mode\033[0m type \033[94mc!\033[0m instead of a term.\t\t\033[94m<- New!\033[0m'

        '\n\n\t\033[97mFurther options:\033[0m'
        '\n\tA) For an \033[32minstructions\033[0m overview type \033[32mi!\033[0m instead of a term.'
        '\n\tB) For a \033[95mversion description\033[0m type \033[95mv!\033[0m instead of a term.'
        '\n\tC) For \033[93msettings\033[0m type \033[93mset!\033[0m instead of a term.\t\t\t\033[93m<- New!\033[0m'
        '\n\tD) For \033[91mending the program\033[0m type \033[91mexit!\033[0m instead of a term.'

        '\n\n\t\033[97mCurrent settings:\033[0m',
        SDM.get_auto_update_as_text(),
        SDM.get_term_output_diplomacy_as_text(),
        SDM.get_one_line_output_as_text(),
        SDM.get_headline_printing_as_text(),
        SDM.get_alphabetical_output_as_text(),
        SDM.get_auto_scan_filters_as_text(),
        SDM.get_output_detail_level_as_text(),

        '\n\n\tHint: If you want to \033[92mdisplay this overview again\033[0m type \033[92m?\033[0m instead of a term.'
    )


def print_exit_without_download():
    os.system('cls')
    print("\n\tDownload will \033[91mnot\033[0m start.")
    time.sleep(2.5)
    os.system('cls')
    print("\n\t\033[93mNotice:\033[0m You have to download the database another time to use this program.")
    time.sleep(6)
    os.system('cls')
    print("\n\tThe Program will now terminate. \n\tFor downloading wiki_morph you can start it again.")
    time.sleep(7)
    os.system('cls')
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
            print_opening(version="2.3c")
            print("\033[93m" + "\n\tDownloading wikimorph database...\n" + "\033[0m")
            urllib.request.urlretrieve(url, "src/database/wiki_morph.json", reporthook=progress)
            stop = True
        except Exception:
            print_opening(version="2.3c")
            print("\n\tDownload not possible: \033[91mNo internet connection!\033[0m"
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

    print("\033[91m" + "\n\tInstructions:" + "\033[0m")
    time.sleep(1.5)
    print("\n\t1) Please type in the term you want to SEARCH and press ENTER.")
    time.sleep(.25)
    print("\n\t2) You are free to repeat this procedure till you end this program.")
    time.sleep(.25)
    print("\n\t3) You can only SEARCH for one term at the same time.")
    time.sleep(.25)
    print("\n\t4) To END this program you can type in 'exit!'.")
    time.sleep(.25)
    print("\n\t5) Results are saved into an excel file (.xlsx),"
          " which will open automatically after the end of the program.")
    time.sleep(.25)
    print("\n\t6) There is also a short logfile (.txt), which covers the search history and system information.")
    time.sleep(.25)
    print("\n\t7) To FILTER your results you can define the part of speech characteristics of the term as follows:"
          '\n\n\t\tgeneral:     "term:PoS"'
          '\n\t\texamples:    "cool:Noun"  /  "cool:Adjective"  /  "hide:Verb"  /  "hide:Adjective:Adverb"'
          '\n\n\t\tThere are the following pos types you can filter on: '
          '(Noun, Verb, Adverb, Adjective, Preposition, Phrase).'
          '\n\t\tYou can search for more than one pos type by connecting them via ":" (see last example).')
    time.sleep(.25)
    print('\n\t8) By typing in "s!" you can enter the scan mode. '
          '\n\t\tHere you are free to select an excel file in the directory, which will be scanned for possible terms. '
          '\n\t\tThese terms will automatically be searched in the wiki_morph database. '
          '\n\t\tYou can use the manual search before or after the automatic scan. '
          '\n\t\tThese modes do not depend from each other.'
          '\n\t\tYou can also execute the automatic scan several times in a row. '
          '\n\t\tBut be aware that the respective outputs are combined in one final output table!'
          '\n\t\tFor separating the outputs and getting different tables you need to end\n\t\tand restart the program'
          ' and plan the scans / manual searches respectively. '
          '\n\t\tHint: soon there will be a version update which allows outputting and cleaning the cache on the flow.')
    time.sleep(.25)
    print('\n\t9) You can find the outputs in the folder "Output/excel_files" and the logs in "Output/log_files".')
    time.sleep(.25)
    print('\n\t10) There is a new mode called "Comparison mode", which allows you to scan in two excel tables'
          '\n\t\tand compare them. The program will generate an overview which terms were found in which table'
          '\n\t\tand which are common or unique.'
          '\n\n\t\tAttention: This only works with excel files which contain the terms in the first column!'
          '\n\t\tThe resulting overview is an excel file which will be saved as "M2E_Comparion_Results_[]" in'
          '\n\t\tthe folder Output/excel_files.')
    time.sleep(.25)
    print("\n\t11) The settings mode is a new feature as well and allows you to influence several aspects"
          "\n\t\tof the program, mostly regarding the output. There are always a description and the "
          "\n\t\trespective options given for a setting for an intuitive user experience. "
          "\n\t\tChanges are saved on the flow, so a crash of the program will not delete the progress.")
    time.sleep(.25)
    print("\n\n\tYou can type in any character/number now to return to main menu.")


def show_version_description():
    time.sleep(1)
    os.system('cls')
    print("\033[91m" + "\n\tWhat´s new in version 2.3c?" + "\033[0m")
    time.sleep(1.5)
    print("\n\t1) There is a new comparison mode, "
          "\n\t\twhich allows you to select two excel files in the directory. "
          "\n\t\tThe first column of these files will be scanned and for every term, "
          "\n\t\tM2E will determine, in which of the files the term occurs."
          "\n\t\tThe results of this comparison will not be saved in the standard output_excel file,"
          "\n\t\tbut in an additional comparison_results excel file in the same folder,"
          "\n\t\tas described in the instructions.")
    time.sleep(.25)
    print("\n\t2) There is also a new settings mode, "
          "\n\t\tin which you can adjust several system variables. "
          "\n\t\tMost of them relate to the output. Changes will be saved on the flow."
          "\n\n\t\tIn total there are six variables to change:"
          "\n\t\t\t1. Automatic Update Control"
          "\n\t\t\t2. Term Output Diplomacy"
          "\n\t\t\t3. Output Line Format"
          "\n\t\t\t4. Headline Printing Control"
          "\n\t\t\t5. Alphabetical Output Formation"
          "\n\t\t\t6. Output Detail Level Control"
          "\n\n\t\tFor every setting there are a description and the respective options given.")
    time.sleep(.25)
    print("\n\t3) There is a new notification sound which informs you about a finished process like: "
          "\n\t\t\t1. Loading the database."
          "\n\t\t\t2. Saving results from auto scan mode."
          "\n\t\t\t3. Saving results from comparison mode."
          "\n\t\t\t4. Saving changes in settings mode."
          "\n\t\t\t5. ..."
          "\n\n\t\tNote: Depending on the hardware of your system there could be compatibility problems"
          "\n\t\twith the module used to load the sound. In this case the sound is not playing and"
          "\n\t\tyou will get an error message during the runtime."
          "\n\t\tBut the problem is captured by exception handling, so you don´t have to worry."
          "\n\t\tThe Program will not crash and you can continue your work as usual.")
    time.sleep(.25)
    print("\n\t4) As always: General revision of the displayed text, "
          "\n\t\tupdate of instructions and version description.")
    time.sleep(.25)
    print("\n\n\tYou can type in any character/number now to return to main menu.")


def print_headlines(worksheet, excel_row, output_detail_level):

    blue_color = "0000FF"
    brown_color = "6E2C00"

    term_Hcell = 'A' + str(excel_row)
    filter_Hcell = 'B' + str(excel_row)
    pos_Hcell = 'C' + str(excel_row)
    syll_Hcell = 'D' + str(excel_row)
    def_Hcell = 'E' + str(excel_row)
    worksheet[term_Hcell] = 'Term'
    worksheet[filter_Hcell] = 'Filter'
    worksheet[pos_Hcell] = 'PoS'
    worksheet[syll_Hcell] = 'Syllables'
    worksheet[def_Hcell] = 'Definition'
    worksheet[term_Hcell].font = Font(bold=True)
    worksheet[filter_Hcell].font = Font(bold=True)
    worksheet[pos_Hcell].font = Font(bold=True)
    worksheet[syll_Hcell].font = Font(bold=True)
    worksheet[def_Hcell].font = Font(bold=True)

    if output_detail_level >= 2:
        affix_Hcell = 'F' + str(excel_row)
        lang_Hcell = 'G' + str(excel_row)
        sub_pos_Hcell = 'H' + str(excel_row)
        mean_Hcell = 'I' + str(excel_row)
        worksheet[affix_Hcell] = 'Affix'
        worksheet[lang_Hcell] = 'Language'
        worksheet[sub_pos_Hcell] = 'PoS'
        worksheet[mean_Hcell] = 'Meaning'
        worksheet[affix_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
        worksheet[lang_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
        worksheet[sub_pos_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
        worksheet[mean_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))

    if output_detail_level == 3:
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

    excel_row += 1
    return worksheet, excel_row


def search_and_output(worksheet, excel_row, pos_filters, term, entries_list,
                      only_found_terms, only_not_found_terms, multiline_output, output_detail_level,
                      headline_printing, hap):

    pos_filters = pos_filters.split(",")

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
            worksheet[filter_cell] = str(pos_filters[0])

    # Begin writing term to Excel file ---------------------------------------------------------------------------------

    # print control in dependency of chosen 3 way output option
    found_entries = 0
    for x in range(len(entries_list)):
        entry = entries_list[x]
        if entry["Word"] == term and entry["PoS"] in pos_filters:
            found_entries += 1

    if found_entries != 0 and not only_not_found_terms:
        if headline_printing == 3 and not hap:
            worksheet, excel_row = print_headlines(worksheet, excel_row, output_detail_level)
        print_term()
    elif found_entries == 0 and not only_found_terms:
        if headline_printing == 3 and not hap:
            worksheet, excel_row = print_headlines(worksheet, excel_row, output_detail_level)
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
        multiline_at_level2_already_executed = False

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

                            if multiline_output and not multiline_at_level2_already_executed:
                                excel_row += 1
                                multiline_at_level2_already_executed = True

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
                            else:
                                excel_row += 1
                else:
                    excel_row += 1

    if found_entries == 0 and len(pos_filters) == 6:
        final_output += "\n\tWarning: database has no entry for '" + term + "'."
        log_output += "\n\tWarning: no entry for '" + term + "'."

        if not only_found_terms:
            set_level_1_cell_data(excel_row, pos="N/V", syllables="N/V", definition="N/V")
            if output_detail_level >= 2:
                if multiline_output:
                    excel_row += 1
                set_level_2_cell_data(excel_row, affix="N/V", language="N/V", sub_pos="N/V", meaning="N/V")
            if output_detail_level == 3:
                if multiline_output:
                    excel_row += 1
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
            if output_detail_level >= 2:
                set_level_2_cell_data(excel_row, affix="N/V", language="N/V", sub_pos="N/V", meaning="N/V")
            if output_detail_level == 3:
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

    invalid_terms = []
    for term in terms:
        if not is_valid_scan(term):
            terms.pop(terms.index(term))
            invalid_terms.append(term)

    terms = [term.lower() for term in terms]

    return terms, invalid_terms


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


def display_settings(setting, current_var, current_var_2=""):

    if setting == 1:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 1/7: Automatic Database Updates"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tThe program will automatically search for wiki_morph updates "
              "\n\tbefore loading the installed version of the database. "
              "\n\tIf there is a new version you will have the option to download it."
              "\n\tBut the search itself may take a few seconds every time the program is started.")
        if current_var == 0:
            print("\n\tOptions:\n\t\t\t\t1. on\n\t\t\t\033[93m" + "->" + "\033[0m\t2. off")
        else:
            print("\n\tOptions:\n\t\t\t\033[93m" + "->" + "\033[0m\t1. on\n\t\t\t\t2. off")

    elif setting == 2:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 2/7: Term Output Diplomacy"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tDecide, which of the terms you searched shall be considered in the output."
              "\n\tThis only affects the excel table. The log_file.txt cannot be changed.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t\033[93m" + "->" + "\033[0m\t1. only found terms"
                  "\n\t\t\t\t2. only not found terms\n\t\t\t\t3. all searched terms")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. only found terms"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t2. only not found terms\n\t\t\t\t3. all searched terms")
        else:
            print("\n\tOptions:\n\t\t\t\t1. only found terms"
                  "\n\t\t\t\t2. only not found terms\n\t\t\t\033[93m" + "->" + "\033[0m\t3. all searched terms")

    elif setting == 3:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 3/7: Output Format"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tThe excel output can either be structured with one-line or multiline format."
              "\n\tMulti-line format is more readable and provides a better overview for the user."
              "\n\tOne-line format is recommended in case of further processing of the output data, "
              "\n\tsince it is easier to access data which is covered in only one line.")
        if current_var:
            print("\n\tOptions:\n\t\t\t\033[93m" + "->" + "\033[0m\t1. one-line\n\t\t\t\t2. multi-line")
        else:
            print("\n\tOptions:\n\t\t\t\t1. one-line\n\t\t\t\033[93m" + "->" + "\033[0m\t2. multi-line")

    elif setting == 4:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 4/7: Headline Printing"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tThe program is able to repeat the printing of a standardized headline for the"
              "\n\tresulting output excel file."
              "\n\tHere you can decide, how often a headline shall be printed.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t\033[93m" + "->" + "\033[0m\t1. only at top of excel / no repeat"
                  "\n\t\t\t\t2. for every new document scanned in"
                  "\n\t\t\t\t\t(note: only in scan mode; for manual search option 1 will be used)"
                  "\n\t\t\t\t3. for every new term printed")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. only at top of excel / no repeat"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t2. for every new document scanned in"
                  "\n\t\t\t\t\t(note: only in scan mode; for manual search option 1 will be used)"
                  "\n\t\t\t\t3. for every new term printed")
        else:
            print("\n\tOptions:\n\t\t\t\t1. only at top of excel / no repeat"
                  "\n\t\t\t\t2. for every new document scanned in"
                  "\n\t\t\t\t\t(note: only in scan mode; for manual search option 1 will be used)"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t3. for every new term printed")

    elif setting == 5:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 5/7: Alphabetical Output Order"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tDecide, if the output shall be structured in alphabetical order."
              "\n\tNote: For the moment this functionality is only available for auto scan mode."
              "\n\tManual search output will not be structured anyway.")
        if current_var and current_var_2:
            print("\n\tOptions:\n\t\t\t\033[93m" + "->" + "\033[0m\t1. alphabetical, ascending"
                  "\n\t\t\t\t2. alphabetical, descending"
                  "\n\t\t\t\t3. non-alphabetical")
        elif current_var and not current_var_2:
            print("\n\tOptions:\n\t\t\t\t1. alphabetical, ascending"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t2. alphabetical, descending"
                  "\n\t\t\t\t3. non-alphabetical")
        else:
            print("\n\tOptions:\n\t\t\t\t1. alphabetical, ascending"
                  "\n\t\t\t\t2. alphabetical, descending"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t3. non-alphabetical")

    elif setting == 6:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 6/7: Automatic Scan Filters"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tSince you are familiar with the automatic scan mode,"
              "\n\tyou can specify the search of the scanned terms by presetting"
              "\n\tthe pos (part of speech) filters for these terms."
              "\n\tThis is based on the concept from the manual search mode."
              "\n\tYou can choose the following pos filter settings:")
        if current_var == "Noun":
            print("\n\tOptions:\n\t\t\t\033[93m" + "->" + "\033[0m\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Verb":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Adjective":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Adverb":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Preposition":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Phrase":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        else:
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t7. All pos types / no restrictions")
        print("\n\t\033[93m" + "Hint:" + "\033[0m Of course not all possible combinations could be considered here."
              "\n\tFor instance if you want to scan for Nouns and Verbs in a document,"
              "\n\tyou can choose one of the two options, execute the automatic scan mode with this document,"
              "\n\tchange the pos filter setting to the other option and execute the AS mode again."
              "\n\tThe results will be saved into the same excel file as usual.")

    elif setting == 7:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 7/7: Output Detail Level"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tFor every term entry in the database there are three levels of information:"
              "\n\tThe basic term data (Level 1, output print color: black), "
              "\n\tthe morphology data (Level 2, output print color: blue) and "
              "\n\tetymology compound data (Level 3, output print color brown)."
              "\n\tHere you can set the depth of the output information according to these levels.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t\033[93m" + "->" + "\033[0m\t1. Level 1: only term data"
                  "\n\t\t\t\t2. Level 2: term data + morphology data"
                  "\n\t\t\t\t3. Level 3: term data + morphology data + etymology data")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. Level 1: only term data"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t2. Level 2: term data + morphology data"
                  "\n\t\t\t\t3. Level 3: term data + morphology data + etymology data")
        else:
            print("\n\tOptions:\n\t\t\t\t1. Level 1: only term data"
                  "\n\t\t\t\t2. Level 2: term data + morphology data"
                  "\n\t\t\t\033[93m" + "->" + "\033[0m\t3. Level 3: term data + morphology data + etymology data")


def display_settings_after_changes(setting, current_var, current_var_2=""):

    if setting == 1:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 1/7: Automatic Database Updates"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tThe program will automatically search for wiki_morph updates "
              "\n\tbefore loading the installed version of the database. "
              "\n\tIf there is a new version you will have the option to download it."
              "\n\tBut the search itself may take a few seconds every time the program is started.")
        if current_var == 0:
            print("\n\tOptions:\n\t\t\t\t1. on\n\t\t\t\033[92m" + "->" + "\033[0m\t2. off")
        else:
            print("\n\tOptions:\n\t\t\t\033[92m" + "->" + "\033[0m\t1. on\n\t\t\t\t2. off")

    elif setting == 2:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 2/7: Term Output Diplomacy"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tDecide, which of the terms you searched shall be considered in the output."
              "\n\tThis only affects the excel table. The log_file.txt cannot be changed.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t\033[92m" + "->" + "\033[0m\t1. only found terms"
                  "\n\t\t\t\t2. only not found terms\n\t\t\t\t3. all searched terms")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. only found terms"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t2. only not found terms\n\t\t\t\t3. all searched terms")
        else:
            print("\n\tOptions:\n\t\t\t\t1. only found terms"
                  "\n\t\t\t\t2. only not found terms\n\t\t\t\033[92m" + "->" + "\033[0m\t3. all searched terms")

    elif setting == 3:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 3/7: Output Format"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tThe excel output can either be structured with one-line or multiline format."
              "\n\tMulti-line format is more readable and provides a better overview for the user."
              "\n\tOne-line format is recommended in case of further processing of the output data, "
              "\n\tsince it is easier to access data which is covered in only one line.")
        if current_var:
            print("\n\tOptions:\n\t\t\t\033[92m" + "->" + "\033[0m\t1. one-line\n\t\t\t\t2. multi-line")
        else:
            print("\n\tOptions:\n\t\t\t\t1. one-line\n\t\t\t\033[92m" + "->" + "\033[0m\t2. multi-line")

    elif setting == 4:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 4/7: Headline Printing"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tThe program is able to repeat the printing of a standardized headline for the"
              "\n\tresulting output excel file."
              "\n\tHere you can decide, how often a headline shall be printed.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t\033[92m" + "->" + "\033[0m\t1. only at top of excel / no repeat"
                  "\n\t\t\t\t2. for every new document scanned in"
                  "\n\t\t\t\t\t(note: only in scan mode; for manual search option 1 will be used)"
                  "\n\t\t\t\t3. for every new term printed")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. only at top of excel / no repeat"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t2. for every new document scanned in"
                  "\n\t\t\t\t\t(note: only in scan mode; for manual search option 1 will be used)"
                  "\n\t\t\t\t3. for every new term printed")
        else:
            print("\n\tOptions:\n\t\t\t\t1. only at top of excel / no repeat"
                  "\n\t\t\t\t2. for every new document scanned in"
                  "\n\t\t\t\t\t(note: only in scan mode; for manual search option 1 will be used)"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t3. for every new term printed")

    elif setting == 5:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 5/7: Alphabetical Output Order"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tDecide, if the output shall be structured in alphabetical order."
              "\n\tNote: For the moment this functionality is only available for auto scan mode."
              "\n\tManual search output will not be structured anyway.")
        if current_var and current_var_2:
            print("\n\tOptions:\n\t\t\t\033[92m" + "->" + "\033[0m\t1. alphabetical, ascending"
                  "\n\t\t\t\t2. alphabetical, descending"
                  "\n\t\t\t\t3. non-alphabetical")
        elif current_var and not current_var_2:
            print("\n\tOptions:\n\t\t\t\t1. alphabetical, ascending"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t2. alphabetical, descending"
                  "\n\t\t\t\t3. non-alphabetical")
        else:
            print("\n\tOptions:\n\t\t\t\t1. alphabetical, ascending"
                  "\n\t\t\t\t2. alphabetical, descending"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t3. non-alphabetical")

    elif setting == 6:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 6/7: Automatic Scan Filters"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tSince you are familiar with the automatic scan mode,"
              "\n\tyou can specify the search of the scanned terms by presetting"
              "\n\tthe pos (part of speech) filters for these terms."
              "\n\tThis is based on the concept from the manual search mode."
              "\n\tYou can choose the following pos filter settings:")
        if current_var == "Noun":
            print("\n\tOptions:\n\t\t\t\033[92m" + "->" + "\033[0m\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Verb":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Adjective":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Adverb":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Preposition":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Phrase":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        else:
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t7. All pos types / no restrictions")
        print("\n\t\033[93m" + "Hint:" + "\033[0m Of course not all possible combinations could be considered here."
              "\n\tFor instance if you want to scan for Nouns and Verbs in a document,"
              "\n\tyou can choose one of the two options, execute the automatic scan mode with this document,"
              "\n\tchange the pos filter setting to the other option and execute the AS mode again."
              "\n\tThe results will be saved into the same excel file as usual.")

    elif setting == 7:
        print("\033[93m" + "\n\t~ Settings Menu ~" + "\033[0m"
              "\n\n\tSetting 7/7: Output Detail Level"
              "\n\t----------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tFor every term entry in the database there are three levels of information:"
              "\n\tThe basic term data (Level 1, output print color: black), "
              "\n\tthe morphology data (Level 2, output print color: blue) and "
              "\n\tetymology compound data (Level 3, output print color brown)."
              "\n\tHere you can set the depth of the output information according to these levels.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t\033[92m" + "->" + "\033[0m\t1. Level 1: only term data"
                  "\n\t\t\t\t2. Level 2: term data + morphology data"
                  "\n\t\t\t\t3. Level 3: term data + morphology data + etymology data")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. Level 1: only term data"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t2. Level 2: term data + morphology data"
                  "\n\t\t\t\t3. Level 3: term data + morphology data + etymology data")
        else:
            print("\n\tOptions:\n\t\t\t\t1. Level 1: only term data"
                  "\n\t\t\t\t2. Level 2: term data + morphology data"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t3. Level 3: term data + morphology data + etymology data")