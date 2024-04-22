import sys
import os
import urllib.request
import datetime
import openpyxl
import time
import pandas as pd

from PyQt5.QtWidgets import QApplication, QFileDialog
from openpyxl.styles import Font, Color

import savedata_manager as SDM
import notification_sound_player as NSP


def is_valid_input(i):
    if i == "":
        return False
    pos = []
    if ":" in i:
        pos = i.split(":")
        i = pos[0]
        pos.pop(0)

    allowed_inputs = ['exit!', 'set!', 's!', 'i!', 'v!', 'c!', '?', '']
    for char in i:
        if not (char.isalpha() or i in allowed_inputs):
            print_opening(version="3.0c")
            print("\n\t\033[91mWarning:\033[0m Invalid input!"
                  "\n\n\tFor typing in the term please use standard characters only. No numbers."
                  "\n\tSpecial signs are only allowed as described in the main menu.")
            time.sleep(8)
            return False

    allowed_pos_filters = ['noun', 'verb', 'adjective', 'adverb', 'preposition', 'phrase']
    for filter in pos:
        if not filter in allowed_pos_filters:
            print_opening(version="3.0c")
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


def measure_time(start, end, search=True, comparison=False):
    # Zeitdifferenz in Minuten und Sekunden berechnen
    elapsed_time_seconds = end - start
    elapsed_minutes = int(elapsed_time_seconds // 60)
    elapsed_seconds = int(elapsed_time_seconds % 60)
    elapsed_seconds_formatted = "{:02d}".format(elapsed_seconds)
    if comparison:
        return (f"\tTime needed for comparison:\033[94m {elapsed_minutes} minutes and "
                f"{elapsed_seconds_formatted} seconds.\33[0m")
    if search:
        return (f"\tTime needed for search:\33[92m {elapsed_minutes} minutes and "
                f"{elapsed_seconds_formatted} seconds.\33[0m")
    else:
        return (f"\tTime needed for scan: "
                f"\33[38;5;130m{elapsed_minutes} minutes and {elapsed_seconds_formatted} seconds.\33[0m")


def print_opening(version):
    os.system('cls')
    print("\033[92m" + "\n\tMorph2Excel ~ Version " + version + "\033[0m")


def print_manual_search_headline(tip=False):
    print("\n\t\033[97mManual term search\033[0m"
          "\n\t\033[97m------------------------------------------------------------------------\033[0m")
    if tip:
        print('\n\t\33[92mTip:\33[0m If you want to display the\033[92m main menu\033[0m again '
              'just press \033[92menter\033[0m.')


def print_main_menu(version):

    # preparing displays ------------------------------------------------------
    headline = "\033[92m" + "\n\tMorph2Excel ~ Version " + version + "\033[0m"\
               "\n\n\t\033[92mMain Menu\033[0m"
    progress = [
        "\t\033[92m------------------------------------------------------------------------\033[0m",
        "\t\033[92m[--]--------------------------------------------------------------------\033[0m",
        "\t\033[92m----[--]----------------------------------------------------------------\033[0m",
        "\t\033[92m--------[--]------------------------------------------------------------\033[0m",
        "\t\033[92m------------[--]--------------------------------------------------------\033[0m",
        "\t\033[92m----------------[--]----------------------------------------------------\033[0m",
        "\t\033[92m--------------------[--]------------------------------------------------\033[0m",
        "\t\033[92m------------------------[--]--------------------------------------------\033[0m",
        "\t\033[92m----------------------------[--]----------------------------------------\033[0m",
        "\t\033[92m--------------------------------[--]------------------------------------\033[0m",
        "\t\033[92m------------------------------------[--]--------------------------------\033[0m",
        "\t\033[92m----------------------------------------[--]----------------------------\033[0m",
        "\t\033[92m--------------------------------------------[--]------------------------\033[0m",
        "\t\033[92m------------------------------------------------[--]--------------------\033[0m",
        "\t\033[92m----------------------------------------------------[--]----------------\033[0m",
        "\t\033[92m--------------------------------------------------------[--]------------\033[0m",
        "\t\033[92m------------------------------------------------------------[--]--------\033[0m",
        "\t\033[92m----------------------------------------------------------------[--]----\033[0m",
        "\t\033[92m--------------------------------------------------------------------[--]\033[0m",
        "\t\033[92m[----------------------------------------------------------------------]\033[0m",
        "\t\033[92m------------------------------------------------------------------------\033[0m"
        ]
    menu_monochrom_display = [
        "\n\tManual search mode is prepared.",
        "\tYou can now search for terms.",
        '\n\tAlternative search modes:',
        '\tI)  For Automatic Scan Mode type s! instead of a term.',
        '\tII) For Comparison Mode type c! instead of a term.',
        '\n\tFurther options:',
        '\tA) For an instructions overview type i! or ? instead of a term.',
        '\tB) For a version description type v! instead of a term.',
        '\tC) For settings type set! instead of a term.',
        '\tD) For ending the program type exit! instead of a term.',
        '\n\tCurrent settings:',
        SDM.get_database_version_as_text(),
        SDM.get_term_output_diplomacy_as_text(),
        SDM.get_one_line_output_as_text(),
        SDM.get_headline_printing_as_text(),
        SDM.get_alphabetical_output_as_text(),
        SDM.get_auto_scan_filters_as_text(),
        SDM.get_output_detail_level_as_text(),
        SDM.get_system_sound_level_as_text(),
        '\n\tHint: If you want to display this menu again just press enter.'
    ]
    menu_color_display = [
        "\n\t\33[97mManual search mode is prepared.",
        "\tYou can now search for terms.\33[0m",
        '\n\t\033[97mAlternative search modes:\033[0m',
        '\tI)  For \033[38;5;130mAutomatic Scan Mode\033[0m type \033[38;5;130ms!\033[0m instead of a term.',
        '\tII) For \033[94mComparison Mode\033[0m type \033[94mc!\033[0m instead of a term.\t\t\033[94m<- New!\033[0m',
        '\n\t\033[97mFurther options:\033[0m',
        '\tA) For an \033[92minstructions\033[0m overview type \033[92mi!\033[0m or \033[92m?\033[0m instead of a term.',
        '\tB) For a \033[95mversion description\033[0m type \033[95mv!\033[0m instead of a term.',
        '\tC) For \033[33msettings\033[0m type \033[33mset!\033[0m instead of a term.\t\t\t\033[33m<- New!\033[0m',
        '\tD) For \033[91mending the program\033[0m type \033[91mexit!\033[0m instead of a term.',
        '\n\t\033[97mCurrent settings:\033[0m',
        SDM.get_database_version_as_text(),
        SDM.get_term_output_diplomacy_as_text(),
        SDM.get_one_line_output_as_text(),
        SDM.get_headline_printing_as_text(),
        SDM.get_alphabetical_output_as_text(),
        SDM.get_auto_scan_filters_as_text(),
        SDM.get_output_detail_level_as_text(),
        SDM.get_system_sound_level_as_text(),
        '\n\tHint: If you want to \033[92mdisplay this menu again\033[0m just press \033[92menter\033[0m.'
    ]

    # printing main menu ------------------------------------------------------
    os.system('cls')
    print(headline)
    print(progress[0])
    NSP.play_start_sound() if SDM.get_system_sound_level() >= 2 else None
    time.sleep(.5)

    for lines in range(len(menu_monochrom_display)):

        os.system('cls')
        print(headline)
        print(progress[lines+1])
        for l in range(0, lines+1):
            print(menu_monochrom_display[l])
        time.sleep(.05)

    os.system('cls')
    print(headline)
    print(progress[0])
    for line in range(len(menu_color_display)):
        print(menu_color_display[line])


def print_exit_without_download():
    os.system('cls')
    print("\n\tDownload will \033[91mnot\033[0m start.")
    time.sleep(2.5)
    os.system('cls')
    print("\n\t\033[33mNotice:\033[0m You have to download the database another time to use this program.")
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


def create_comparison_result_excel(fd, counter):

    workbook_title = "output/excel_files/M2E_Comparison_Results_" + str(counter) + "_(" + str(fd) + ").xlsx"
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
            print_opening(version="3.0c")
            print("\033[33m" + "\n\tDownloading wikimorph database...\n" + "\033[0m")
            urllib.request.urlretrieve(url, "src/database/wiki_morph.json", reporthook=progress)
            stop = True
        except Exception:
            print_opening(version="3.0c")
            print("\n\tDownload not possible: \033[91mNo internet connection!\033[0m"
                  "\n\tYou can try again by pressing enter."
                  '\n\tAlternatively you can end the program by typing "exit!".')
            normal = False
            i = input("\n\t")
            if i == "exit!" or i == "exit":
                stop = True

    return normal


def show_instructions():
    os.system('cls')
    print_opening(version="3.0c")
    print("\n\t\033[92mInstructions\033[0m"
          "\n\t\033[92m[----------------------------------------------------------------------]\033[0m")
    NSP.play_accept_sound() if SDM.get_system_sound_level() == 3 else None
    time.sleep(.5)
    print("\n\t\033[33m" + "\n\tOpening PDF Handbook...\n" + "\033[0m")
    time.sleep(1)
    try:
        current_directory = os.getcwd()
        instructions_pdf_path = r"src\data\Externals\M2E_v3.0c_EAP_Handbook.pdf"
        # path = current_directory + instructions_pdf_path
        os.system(instructions_pdf_path)
    except Exception:
        print("\n\t\033[91mWarning:\033[0m The program was not able to open the handbook file "
              "due to problems with the source path!"
              'You can find the respective file under '
              '\033[33msrc/data/Externals/M2E_v3.0c_EAP_Handbook.pdf\033[0m and open it manually.')
        input("\n\n\tType in any character to return to main menu: ")
        os.system('cls')
    os.system('cls')
    print_opening(version="3.0c")
    print("\n\t\033[92mInstructions\033[0m"
          "\n\t\033[92m[----------------------------------------------------------------------]\033[0m")
    print("\n\tReturning to main menu...")
    time.sleep(1)


def show_version_description():
    os.system('cls')
    print_opening(version="3.0c")
    print("\033[95m" + "\n\tWhat´s new in version 3.0c?" + "\033[0m"
          "\n\t\033[95m[----------------------------------------------------------------------]\033[0m")
    NSP.play_accept_sound() if SDM.get_system_sound_level() == 3 else None
    time.sleep(1.5)
    print("\n\t\33[95m1)\33[0m There is a new comparison mode, "
          "\n\t\twhich allows you to select two excel files in the directory. "
          "\n\t\tThe first column of these files will be scanned and for every term, "
          "\n\t\tM2E will determine, in which of the files the term occurs."
          "\n\t\tThe results of this comparison will not be saved in the standard output_excel file,"
          "\n\t\tbut in an additional comparison_results excel file in the same folder,"
          "\n\t\tas described in the instructions."
          "\n\n\t\t\033[33m" + "Note:" + "\033[0m The program will ignore the first column of your excel files, "
          "\n\t\tsince headlines should not be taken into account."
          "\n\t\tAccordingly please take care if your terms do not start with the second row!")
    time.sleep(.25)
    print("\n\t\33[95m2)\33[0m There is also a new settings mode, "
          "\n\t\tin which you can adjust several system variables. "
          "\n\t\tMost of them relate to the output. Changes will be saved on the flow."
          "\n\n\t\tIn total there are seven variables to change:"
          "\n\t\t\t1. Automatic Update Control"
          "\n\t\t\t2. Term Output Diplomacy"
          "\n\t\t\t3. Output Line Format"
          "\n\t\t\t4. Headline Printing Control"
          "\n\t\t\t5. Alphabetical Output Formation"
          "\n\t\t\t6. Automatic Scan Filters"
          "\n\t\t\t7. Output Detail Level Control"
          "\n\n\t\tFor every setting there are a description and the respective options given.")
    time.sleep(.25)
    print("\n\t\33[95m3)\33[0m There is a new notification sound which informs you about a finished process like: "
          "\n\t\t1. Loading the database or the main menu."
          "\n\t\t2. Saving results from auto scan mode."
          "\n\t\t3. Saving results from comparison mode."
          "\n\t\t4. Saving changes in settings mode."
          "\n\t\t5. ...")
    time.sleep(.25)
    print("\n\t\33[95m4)\33[0m The system menus were revised."
          "\n\t\t1. Better structure and new color schemes."
          "\n\t\t2. A new overview of the current system settings for the main menu was added.")
    time.sleep(.25)
    print("\n\n\tYou can type in any character to return to main menu.")


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
    NSP.play_request_sound() if SDM.get_system_sound_level() >= 2 else None
    # Create a QApplication instance
    app = QApplication([])

    # Open file dialog to choose the Excel file
    excel_file, _ = QFileDialog.getOpenFileName(None, "Select Excel File", "./data", "Excel Files (*.xlsx)")

    return excel_file


def autoscan(excel_file, duplicates=False, abc=True, abc_ascending=True, test_for_invalides=True):
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
    if test_for_invalides:
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
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 1/8: Database Version Control"
              "\n\t[-------]---------------------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tHere you can delete or update the currently installed version of"
              "\n\tthe wikimorph database or just change its description."
              "\n\tOnly one database version can be installed so far.")

        if current_var == "":
            print("\n\tCurrently installed version:\tNo version installed!",
                  "\n\tInstallation date:\tNo version installed!")
        elif current_var != "" and current_var_2 == "":
            print("\n\tCurrently installed version:\tNo description found!",
                  "\n\tInstallation date:\t" + SDM.get_database_version_date())
        else:
            print("\n\tCurrently installed version:\t" + SDM.get_database_version_description(),
                  "\n\tInstallation date:\t" + SDM.get_database_version_date())

        print("\n\tOptions:"
              '\n\t\t\t\t1. Type in \33[94mu!\33[0m to \33[94mupdate (reinstall)\33[0m the database.'
              '\n\t\t\t\t2. Type in \33[33mc!\33[0m to \33[33mchange the description\33[0m '
              'for the currently installed version.'
              '\n\t\t\t\t3. Type in \33[91md!\33[0m to \33[91mdelete\33[0m the currently installed version.'
              '\n\n\t\t\t\tPress \33[92menter\33[0m or type in anything else to \33[92mcontinue\33[0m without '
              'making changes.')

    elif setting == 2:
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 2/8: Term Output Diplomacy"
              "\n\t---------[-------]------------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tDecide, which of the terms you searched shall be considered in the output."
              "\n\tThis only affects the excel table. The log_file.txt cannot be changed.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t\033[33m" + "->" + "\033[0m\t1. only found terms"
                  "\n\t\t\t\t2. only not found terms\n\t\t\t\t3. all searched terms")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. only found terms"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t2. only not found terms\n\t\t\t\t3. all searched terms")
        else:
            print("\n\tOptions:\n\t\t\t\t1. only found terms"
                  "\n\t\t\t\t2. only not found terms\n\t\t\t\033[33m" + "->" + "\033[0m\t3. all searched terms")

    elif setting == 3:
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 3/8: Output Format"
              "\n\t------------------[-------]---------------------------------------------"
              "\n\n\tDescription: "
              "\n\tThe excel output can either be structured with one-line or multiline format."
              "\n\tMulti-line format is more readable and provides a better overview for the user."
              "\n\tOne-line format is recommended in case of further processing of the output data, "
              "\n\tsince it is easier to access data which is covered in only one line.")
        if current_var:
            print("\n\tOptions:\n\t\t\t\033[33m" + "->" + "\033[0m\t1. one-line\n\t\t\t\t2. multi-line")
        else:
            print("\n\tOptions:\n\t\t\t\t1. one-line\n\t\t\t\033[33m" + "->" + "\033[0m\t2. multi-line")

    elif setting == 4:
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 4/8: Headline Printing"
              "\n\t---------------------------[-------]------------------------------------"
              "\n\n\tDescription: "
              "\n\tThe program is able to repeat the printing of a standardized headline for the"
              "\n\tresulting output excel file."
              "\n\tHere you can decide, how often a headline shall be printed.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t\033[33m" + "->" + "\033[0m\t1. only at top of excel / no repeat"
                  "\n\t\t\t\t2. for every new document scanned in"
                  "\n\t\t\t\t\t(note: only in scan mode; for manual search option 1 will be used)"
                  "\n\t\t\t\t3. for every new term printed")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. only at top of excel / no repeat"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t2. for every new document scanned in"
                  "\n\t\t\t\t\t(note: only in scan mode; for manual search option 1 will be used)"
                  "\n\t\t\t\t3. for every new term printed")
        else:
            print("\n\tOptions:\n\t\t\t\t1. only at top of excel / no repeat"
                  "\n\t\t\t\t2. for every new document scanned in"
                  "\n\t\t\t\t\t(note: only in scan mode; for manual search option 1 will be used)"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t3. for every new term printed")

    elif setting == 5:
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 5/8: Alphabetical Output Order"
              "\n\t------------------------------------[-------]---------------------------"
              "\n\n\tDescription: "
              "\n\tDecide, if the output shall be structured in alphabetical order."
              "\n\tNote: For the moment this functionality is only available for auto scan mode."
              "\n\tManual search output will not be structured anyway.")
        if current_var and current_var_2:
            print("\n\tOptions:\n\t\t\t\033[33m" + "->" + "\033[0m\t1. alphabetical, ascending"
                  "\n\t\t\t\t2. alphabetical, descending"
                  "\n\t\t\t\t3. non-alphabetical")
        elif current_var and not current_var_2:
            print("\n\tOptions:\n\t\t\t\t1. alphabetical, ascending"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t2. alphabetical, descending"
                  "\n\t\t\t\t3. non-alphabetical")
        else:
            print("\n\tOptions:\n\t\t\t\t1. alphabetical, ascending"
                  "\n\t\t\t\t2. alphabetical, descending"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t3. non-alphabetical")

    elif setting == 6:
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 6/8: Automatic Scan Filters"
              "\n\t---------------------------------------------[-------]------------------"
              "\n\n\tDescription: "
              "\n\tSince you are familiar with the automatic scan mode,"
              "\n\tyou can specify the search of the scanned terms by presetting"
              "\n\tthe pos (part of speech) filters for these terms."
              "\n\tThis is based on the concept from the manual search mode."
              "\n\tYou can choose the following pos filter settings:")
        if current_var == "Noun":
            print("\n\tOptions:\n\t\t\t\033[33m" + "->" + "\033[0m\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Verb":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Adjective":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Adverb":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Preposition":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        elif current_var == "Phrase":
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t6. Phrases only"
                  "\n\t\t\t\t7. All pos types / no restrictions")
        else:
            print("\n\tOptions:\n\t\t\t\t1. Nouns only"
                  "\n\t\t\t\t2. Verbs only"
                  "\n\t\t\t\t3. Adjectives only"
                  "\n\t\t\t\t4. Adverbs only"
                  "\n\t\t\t\t5. Prepositions only"
                  "\n\t\t\t\t6. Phrases only"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t7. All pos types / no restrictions")
        print("\n\t\033[33m" + "Hint:" + "\033[0m Of course not all possible combinations could be considered here."
              "\n\tFor instance if you want to scan for Nouns and Verbs in a document,"
              "\n\tyou can choose one of the two options, execute the automatic scan mode with this document,"
              "\n\tchange the pos filter setting to the other option and execute the AS mode again."
              "\n\tThe results will be saved into the same excel file as usual.")

    elif setting == 7:
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 7/8: Output Detail Level"
              "\n\t------------------------------------------------------[-------]---------"
              "\n\n\tDescription: "
              "\n\tFor every term entry in the database there are three levels of information:"
              "\n\tThe basic term data (Level 1, output print color: black), "
              "\n\tthe morphology data (Level 2, output print color: blue) and "
              "\n\tetymology compound data (Level 3, output print color brown)."
              "\n\tHere you can set the depth of the output information according to these levels.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t\033[33m" + "->" + "\033[0m\t1. Level 1: only term data"
                  "\n\t\t\t\t2. Level 2: term data + morphology data"
                  "\n\t\t\t\t3. Level 3: term data + morphology data + etymology data")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. Level 1: only term data"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t2. Level 2: term data + morphology data"
                  "\n\t\t\t\t3. Level 3: term data + morphology data + etymology data")
        else:
            print("\n\tOptions:\n\t\t\t\t1. Level 1: only term data"
                  "\n\t\t\t\t2. Level 2: term data + morphology data"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t3. Level 3: term data + morphology data + etymology data")

    elif setting == 8:
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 8/8: System Sound Level"
              "\n\t---------------------------------------------------------------[-------]"
              "\n\n\tDescription: "
              "\n\tMorph2Excel is able to give you audio feedback for several interactions."
              "\n\tThis is especially useful if you have to wait longer for an automatic scan or"
              "\n\tin general if you execute the program in the background."
              "\n\tYou can get an audio feedback for most of the user interactions or"
              "\n\tjust keep the notification sounds. Of course you can also set all the sounds off.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t\033[33m" + "->" + "\033[0m\t1. Level 1: no sounds"
                  "\n\t\t\t\t2. Level 2: notification sounds only"
                  "\n\t\t\t\t3. Level 3: all sounds (notification sounds + user feedback audio)")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. Level 1: no sounds"
                  "\n\t\t\t\033[33m" + "->" + "\033[0m\t2. Level 2: notification sounds only"
                  "\n\t\t\t\t3. Level 3: all sounds (notification sounds + user feedback audio)")
        else:
            print("\n\tOptions:\n\t\t\t\t1. Level 1: no sounds"
                  "\n\t\t\t\t2. Level 2: notification sounds only"
                  "\n\t\t\t\033[33m" + "->" +
                  "\033[0m\t3. Level 3: all sounds (notification sounds + user feedback audio)")


def display_settings_after_changes(setting, current_var, current_var_2=""):

    if setting == 1:
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 1/8: Database Version Control"
              "\n\t[-------]---------------------------------------------------------------")

        if current_var == "u1":
            # update
            pass
        elif current_var == "c1":
            # change description
            print("\n\t\33[33mType in the new description for your installed version (max. 25 characters).\33[0m")
        elif current_var == "c2":
            print("\n\tDescription changed to \33[92m" + current_var_2 + "\33[0m.!")
        elif current_var == "d1":
            # delete current version
            pass

    elif setting == 2:
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 2/8: Term Output Diplomacy"
              "\n\t---------[-------]------------------------------------------------------"
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
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 3/8: Output Format"
              "\n\t------------------[-------]---------------------------------------------"
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
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 4/8: Headline Printing"
              "\n\t---------------------------[-------]------------------------------------"
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
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 5/8: Alphabetical Output Order"
              "\n\t------------------------------------[-------]---------------------------"
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
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 6/8: Automatic Scan Filters"
              "\n\t---------------------------------------------[-------]------------------"
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
        print("\n\t\033[33m" + "Hint:" + "\033[0m Of course not all possible combinations could be considered here."
              "\n\tFor instance if you want to scan for Nouns and Verbs in a document,"
              "\n\tyou can choose one of the two options, execute the automatic scan mode with this document,"
              "\n\tchange the pos filter setting to the other option and execute the AS mode again."
              "\n\tThe results will be saved into the same excel file as usual.")

    elif setting == 7:
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 7/8: Output Detail Level"
              "\n\t------------------------------------------------------[-------]---------"
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

    elif setting == 8:
        print_opening(version="3.0c")
        print("\033[33m\n\t~ Settings Menu ~"
              "\n\t------------------------------------------------------------------------\033[0m"
              "\n\n\tSetting 8/8: System Sound Level"
              "\n\t---------------------------------------------------------------[-------]"
              "\n\n\tDescription: "
              "\n\tMorph2Excel is able to give you audio feedback for several interactions."
              "\n\tThis is especially useful if you have to wait longer for an automatic scan or"
              "\n\tin general if you execute the program in the background."
              "\n\tYou can get an audio feedback for most of the user interactions or"
              "\n\tjust keep the notification sounds. Of course you can also set all the sounds off.")
        if current_var == 1:
            print("\n\tOptions:\n\t\t\t\033[92m" + "->" + "\033[0m\t1. Level 1: no sounds"
                  "\n\t\t\t\t2. Level 2: notification sounds only"
                  "\n\t\t\t\t3. Level 3: all sounds (notification sounds + user feedback audio)")
        elif current_var == 2:
            print("\n\tOptions:\n\t\t\t\t1. Level 1: no sounds"
                  "\n\t\t\t\033[92m" + "->" + "\033[0m\t2. Level 2: notification sounds only"
                  "\n\t\t\t\t3. Level 3: all sounds (notification sounds + user feedback audio)")
        else:
            print("\n\tOptions:\n\t\t\t\t1. Level 1: no sounds"
                  "\n\t\t\t\t2. Level 2: notification sounds only"
                  "\n\t\t\t\033[92m" + "->" +
                  "\033[0m\t3. Level 3: all sounds (notification sounds + user feedback audio)")