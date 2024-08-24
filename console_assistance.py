"""
Copyright © MrNemesis98, GitHub, 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software. The software is provided “as is”, without warranty of any kind, express or implied, including but not
limited to the warranties of merchantability, fitness for a particular purpose and noninfringement.
In no event shall the author(s) or copyright holder(s) be liable for any claim, damages or other liability, whether
in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or
other dealings in the software.
"""

import sys
import os
import urllib.request
import datetime
import openpyxl
import time
import pandas as pd
import json
import requests

from PyQt5.QtWidgets import QApplication, QFileDialog
from openpyxl.styles import Font, Color

import console_text_management as CTM
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

    allowed_inputs = ['exit!', 's!', 'i!', 'v!', 'c!', '?', '',
                      'set!', 'set1!', 'set2!', 'set3!', 'set4!',
                      'set5!', 'set6!', 'set7!', 'set8!']
    for char in i:
        if not (char.isalpha() or i in allowed_inputs):
            CTM.clear_screen_backwards(down_to_row=5)
            print("\n\t\033[91mWarning:\033[0m Invalid input!\033[0m")
            NSP.play_deny_sound() if SDM.get_system_sound_level() >= 2 else None
            CTM.stack(["\n\n\tFor typing in the term please use standard characters only.",
                      "\n\tNumbers and special signs are only allowed as described in the manual."])
            time.sleep(8)
            return False

    allowed_pos_filters = ['noun', 'verb', 'adjective', 'adverb', 'preposition', 'phrase']
    for filter in pos:
        if not filter in allowed_pos_filters:
            CTM.clear_screen_backwards(down_to_row=5)
            print("\n\t\033[91mWarning:\033[0m Invalid input!")
            NSP.play_deny_sound() if SDM.get_system_sound_level() >= 2 else None
            CTM.stack(["\n\n\tPlease use valid pos filters only.",
                      "\n\tMore information can be found in the manual."])
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


def print_opening(version, colour=False):
    header_line = "| Morph2Excel ~ Version {} ~ Copyright (c) 2024 MrNemesis98 (MIT License) |".format(version)
    upperline = "*" + "—" * (len(header_line) - 2) + "*"
    underline = "*" + "—" * (len(header_line) - 2) + "*"
    if colour:
        print("\33[92m\t" + upperline + "\n\t" + header_line + "\n\t" + underline + "\33[0m")
    else:
        print("\33[90m\t" + upperline + "\n\t" + header_line + "\n\t" + underline + "\33[0m")


def print_manual_search_headline(tip=False):
    CTM.clear_screen_backwards(down_to_row=5)
    print("\n\t\033[97m- Manual term search -\033[0m"
          "\n\t\033[97m-------------------------------------------------------------------------------\033[0m")
    if tip:
        CTM.draw('\n\t\33[92mTip:\33[0m If you want to display the\033[92m main menu\033[0m again '
                 'just press \033[92menter\033[0m.', clear=False)


def print_main_menu():

    def get_database_installation_info(colored=False):

        normal_text = ("\n\tManual search mode is prepared."
                       "\n\tYou can now search for terms."
                       "\n\n\tAlternative search modes:"
                       "\n\tI)  For Automatic Scan Mode type s! instead of a term.")
        normal_text_colored = ("\n\t\33[97mManual search mode is prepared."
                               "\n\tYou can now search for terms.\33[0m"
                               "\n\n\t\033[97mAlternative search modes:\033[0m"
                               "\n\tI)  For \033[38;5;130mAutomatic Scan Mode\033[0m type \033[38;5;130ms!\033[0m "
                               "instead of a term.")
        exception_text = ("\n\tWarning: the wikimorph database is not installed!"
                          "\n\tAccess to manual search mode is restricted!"
                          "\n\n\tAlternative search modes:"
                          "\n\tI) Access to automatic scan mode is restricted!")
        exception_text_colored = ("\n\t\33[91mWarning: the wikimorph database is not installed!\33[0m"
                                  "\n\tAccess to \33[91mmanual search mode\33[0m is \33[91mrestricted\33[0m!"
                                  "\n\n\t\033[97mAlternative search modes:\033[0m"
                                  "\n\tI) Access to \33[91mautomatic scan mode\33[0m is \33[91mrestricted\33[0m!")
        if SDM.get_database_version_date() != "":
            return normal_text_colored if colored else normal_text
        else:
            return exception_text_colored if colored else exception_text

    # preparing displays ------------------------------------------------------
    headline = "\n\t\33[92m~ Main Menu ~\33[0m"

    menu_monochrom_display = [
        get_database_installation_info(),
        '\tII) For Comparison Mode type c! instead of a term.',
        '\tFurther options:',
        '\tA) For an instructions overview type i! or ? instead of a term.',
        '\tB) For a version description type v! instead of a term.',
        '\tC) For settings type set! instead of a term.',
        '\tD) For ending the program type exit! instead of a term.',
        '\tCurrent settings:',
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
        get_database_installation_info(colored=True),
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
    tab_width = CTM.calculate_tab_width()

    sys.stdout.write(f"\033[{4};\tH")
    sys.stdout.flush()
    print(headline)
    NSP.play_start_sound() if SDM.get_system_sound_level() >= 2 else None

    line_col = tab_width + 1
    text_row = 7
    for line in range(len(menu_monochrom_display)):
        sys.stdout.write(f"\033[{6};{line_col}H")
        sys.stdout.flush()
        CTM.draw("\33[92m------\33[0m", delay=0.001)

        sys.stdout.write(f"\033[{34};{line_col}H")
        sys.stdout.flush()
        CTM.draw("------", delay=0.001)

        sys.stdout.write(f"\033[{text_row};\tH")
        sys.stdout.flush()
        print(menu_monochrom_display[line])

        if text_row == 7:
            text_row = 13
        elif text_row == 13:
            text_row = 15
        elif text_row == 19:
            text_row = 21
        elif text_row == 29:
            text_row = 31
        else:
            text_row += 1
        line_col += 4

    CTM.clear_screen_backwards(7, delay=0)
    for line in range(len(menu_color_display)):
        print(menu_color_display[line])

    sys.stdout.write(f"\033[{36};{line_col}H")


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
    workbook = openpyxl.Workbook()
    workbook.save(workbook_title)

    return workbook_title


def create_comparison_result_excel(fd, counter):

    workbook_title = "output/excel_files/M2E_Comparison_Results_" + str(counter) + "_(" + str(fd) + ").xlsx"
    workbook = openpyxl.Workbook()
    workbook.save(workbook_title)

    return workbook_title


def download_database(url, directly_after_start=False):
    def progress(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write("\r" + "\t[%-100s] \33[33m%d%%\33[0m" % ("#" * percent, percent))
        sys.stdout.flush()

    stop = False
    normal = True

    while not stop:
        try:
            response = requests.get(url, stream=True)
            remote_size = int(response.headers.get("Content-Length", 0))
            remote_size = int(remote_size / (1024 * 1024))
            SDM.set_download_size(remote_size)
            SDM.set_current_size()

            if directly_after_start:
                CTM.clear_screen_backwards(down_to_row=5)
            if os.path.exists("src/database/wiki_morph.json"):
                os.remove("src/database/wiki_morph.json")
            NSP.play_request_sound() if SDM.get_system_sound_level() >= 2 else None
            CTM.draw("\033[33m" + "\n\tDownload of wikimorph database in progress...\n" + "\033[0m", clear=False)
            urllib.request.urlretrieve(url, "src/database/wiki_morph.json", reporthook=progress)
            stop = True
            normal = True
            SDM.set_database_version_date(datetime.date.today().strftime("%d_%m_%Y"))
            SDM.set_database_version_description("")
            current_size = os.path.getsize("src/database/wiki_morph.json")
            current_size = int(current_size / (1024 * 1024))
            SDM.set_current_size(current_size)
        except Exception:

            CTM.clear_screen_backwards(down_to_row=5) if directly_after_start \
                else CTM.clear_screen_backwards(down_to_row=9)

            print("\n\t\033[91mWarning: There was an error detected during the download!\033[0m")
            NSP.play_request_sound() if SDM.get_system_sound_level() >= 2 else None
            CTM.draw("\n\tPlease check your internet connection."
                     "\n\n\tYou can \33[92mtry again\33[0m by pressing \33[92menter\33[0m.")
            if directly_after_start:
                CTM.draw('\n\tAlternatively you can \33[91mend the program\33[0m by typing \33[91mexit!\33[0m.')
            else:
                CTM.draw("\n\tAlternatively you can \33[33mcancel the process and return to settings menu\33[0m by "
                         "typing in \33[33mexit!\33[0m.")
            normal = False
            CTM.unblock_input()
            i = input("\n\n\t")
            CTM.block_input()
            if i == "exit!" or i == "exit" or i == "exit1":
                if directly_after_start:
                    CTM.clear_screen_backwards(down_to_row=5)
                    CTM.draw("\n\t\33[91mProgram terminated!\33[0m")
                    time.sleep(1.5)
                    stop = True
                else:
                    CTM.draw("\n\t\33[91mProcess cancelled!\33[0m")
                    time.sleep(1.5)
                    CTM.clear_screen_backwards(down_to_row=9)
                    stop = True

    return normal


def database_installation_confirmed(right_after_program_start=False):

    def deny_access():
        CTM.clear_screen_backwards(down_to_row=5)
        print("\n\t\33[91mWarning: Access denied!\33[0m")
        NSP.play_deny_sound() if SDM.get_system_sound_level() >= 2 else None
        time.sleep(1)
        CTM.stack(["\n\n\tThis problem can occur if you have no wikimorph installation yet or the last installation "
                   "was interrupted.",
                   "\n\tPlease make sure that you have installed a complete version of the WikiMorph database.",
                   "\n\n\tIn both cases you need to reinstall the database.",
                   "\n\tThere are respective options given in the \33[33msettings menu\33[0m.",
                   "\n\n\tPress \33[92menter\33[0m to continue."])

        return False

    def give_advice():
        print("\n\t\33[91mWarning: No valid wikimorph database version found!\33[0m")
        NSP.play_deny_sound() if SDM.get_system_sound_level() >= 2 else None
        time.sleep(1)
        CTM.stack(["\n\n\tThis problem can occur if you have no wikimorph installation yet or the last installation was"
                   " interrupted.",
                   "\n\tSome functionalities of Morph2Excel will be "
                   "\33[91mrestricted\33[0m until the database is installed "
                   "completely.",
                   "\n\n\tYou are free to install wikimorph now or later with a new program start.",
                   "\n\tThere is also the possibility to download the database in the \33[33msettings menu\33[0m.",
                   "\n\n\tOptions:",
                   "\n\t\t1. Type in \33[92mstart!\33[0m if you want to \33[92mstart the download now\33[0m.",
                   "\n\t\t2. Otherwise press \33[94menter\33[0m or type in anything else to "
                   "\33[94mcontinue without downloading\33[0m."])
        return False

    if not os.path.exists("src/database/wiki_morph.json"):
        give_advice() if right_after_program_start else deny_access()
    else:
        current_size = os.path.getsize("src/database/wiki_morph.json")
        current_size = int(current_size / (1024 * 1024))
        soll_size = SDM.get_soll_size()
        if current_size < soll_size:
            give_advice() if right_after_program_start else deny_access()
        else:
            return True


def load_database(version):
    os.system('cls')
    print_opening(version, colour=True)
    CTM.draw("\n\tLoading wiki_morph database...")
    with open("src/database/wiki_morph.json", "r", encoding="utf-8") as f:
        entries_list = json.load(f)
    return entries_list


def show_instructions():
    CTM.clear_screen_backwards(down_to_row=5)
    print("\n\t\033[92m~ Instructions ~\033[0m"
          "\n\t\033[92m[-----------------------------------------------------------------------------]\033[0m")
    NSP.play_accept_sound() if SDM.get_system_sound_level() == 3 else None

    time.sleep(.5)

    CTM.draw("\n\t\033[33m" + "\n\tOpening PDF Handbook...\n" + "\033[0m", clear=False)
    absolute_path = os.getcwd() + r"\src\data\Externals"
    if " " in absolute_path:
        absolute_path = absolute_path.replace(" ", "%20")
    relative_path = SDM.get_manpath()
    if " " in relative_path:
        relative_path = relative_path.replace(" ", "%20")
    print("\t\33[33mPath:\33[0m " + absolute_path + relative_path)
    time.sleep(1)
    try:
        os.system(absolute_path+relative_path)
        CTM.unblock_input()
        input("\n\tPress \33[92menter\33[0m to return to main menu.")
        CTM.block_input()
    except FileNotFoundError or Exception:
        print("\n\t\033[91mWarning:\033[0m The program was not able to open the handbook file "
              "due to problems with the source path!"
              'You can find the respective file under '
              '\033[33msrc/data/Externals/\33[0m and open it manually.')
        CTM.unblock_input()
        input("\n\n\tType in any character to return to main menu: ")
        CTM.block_input()
    CTM.clear_screen_backwards(down_to_row=5)
    CTM.draw("\n\tReturning to main menu...")
    time.sleep(.5)


def show_version_description():
    CTM.clear_screen_backwards(5)
    print("\033[95m" + "\n\n\t~ What´s new in version 2024.1 ? ~" + "\033[0m"
          "\n\t\033[95m[-----------------------------------------------------------------------------]\033[0m")
    NSP.play_accept_sound() if SDM.get_system_sound_level() == 3 else None
    time.sleep(1.5)
    print("\n\t\33[95m1)\33[0m There is a new \33[95mcomparison mode\33[0m, "
          "\n\t\twhich allows you to select two excel files in the directory. "
          "\n\t\tThe first column of these files will be scanned and for every term, "
          "\n\t\tM2E will determine, in which of the files the term occurs."
          "\n\t\tThe results of this comparison will not be saved in the standard output_excel file,"
          "\n\t\tbut in an additional comparison_results excel file in the same folder,"
          "\n\t\tas described in the instructions."
          "\n\n\t\t\033[33m" + "Note:" + "\033[0m The program will ignore the first row of your excel files, "
          "\n\t\tsince headlines should not be taken into account."
          "\n\t\tAccordingly please take care if your terms do not start with the second row!")
    time.sleep(.25)
    print("\n\t\33[95m2)\33[0m There is also a new \33[95msettings mode\33[0m, "
          "\n\t\tin which you can adjust several system variables. "
          "\n\t\tMost of them relate to the output. Changes will be saved on the flow."
          "\n\t\tFor every setting there are a description and the respective options given."
          "\n\t\tFurthermore there is a new \33[95mdatabase version control center\33[0m integrated in the settings,"
          "\n\t\tthat allows you to manage your installed version of the wikimorph database.")
    time.sleep(.25)
    print("\n\t\33[95m3)\33[0m Four different \33[95msystem sounds\33[0m were integrated."
          "\n\t\t1) A notification sound for program launch and main menu, "
          "\n\t\t2) an audio signal for the request of an user interaction,"
          "\n\t\t3) as well as sounds for negative and positive audio feedback."
          "\n\t\tThese sounds can be limited or deactivated in the settings menu.")
    time.sleep(.25)
    print("\n\t\33[95m4)\33[0m The system menus were revised."
          "\n\t\t1. Better structure and new \33[95mcolor schemes\33[0m in the menus."
          "\n\t\t2. A new \33[95moverview of the current system settings\33[0m for the main menu was added.")
    time.sleep(.25)
    print("\n\n\tFor more information have a look at the \33[94minstructions / user manual\33[0m of this version."
          "\n\tPress \33[92menter\33[0m to return to main menu.")


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
                      headline_printing, hdlp_start, hdlp_doc):

    pos_filters = pos_filters.split(", ")

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
        elif 1 < len(pos_filters) < 6:
            pos_info_string = ""
            for x in range(len(pos_filters)):
                pos_info_string += pos_filters[x]
                if x != len(pos_filters) - 1:
                    pos_info_string += ", "
            worksheet[filter_cell] = pos_info_string
        else:
            worksheet[filter_cell] = str(pos_filters[0]) + "s only"

    # Begin writing term to Excel file ---------------------------------------------------------------------------------

    # print control in dependency of chosen 3 way output option plus headline printing management
    found_entries = 0
    for x in range(len(entries_list)):
        entry = entries_list[x]
        if entry["Word"] == term and entry["PoS"] in pos_filters:
            found_entries += 1

    if found_entries != 0 and not only_not_found_terms:     # Term gefunden und gefundene Terms sollen gedruckt werden
        if headline_printing == 3:                          # Term-Überschrift angeordnet
            if not hdlp_start and not hdlp_doc:             # keine Tabellen- oder Dokumentüberschrift voraus?
                worksheet, excel_row = print_headlines(worksheet, excel_row, output_detail_level)
            else:
                hdlp_start = False
                hdlp_doc = False
        print_term()
        if headline_printing == 2:                          # Überschrift für Dokumente im AS wieder
            hdlp_start = False                              # freigeben, nachdem ein erster Term gedruckt wurde
            hdlp_doc = False

    elif found_entries == 0 and not only_found_terms:       # Term nicht gefunden, soll aber gedruckt werden
        if headline_printing == 3:                          # Term-Überschrift angeordnet
            if not hdlp_start and not hdlp_doc:             # keine Tabellen- oder Dokumentüberschrift voraus?
                worksheet, excel_row = print_headlines(worksheet, excel_row, output_detail_level)
            else:
                hdlp_start = False
                hdlp_doc = False
        print_term()
        if headline_printing == 2:                          # Überschrift für Dokumente im AS wieder
            hdlp_start = False                              # freigeben, nachdem ein erster Term gedruckt wurde
            hdlp_doc = False

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
    for fil in pos_filters:

        for index in range(len(entries_list)):

            entry = entries_list[index]
            multiline_at_level2_already_executed = False

            if entry["Word"] == term and entry["PoS"] == fil:
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

    return worksheet, excel_row, log_output, hdlp_start, hdlp_doc


def select_excel_file():
    NSP.play_request_sound() if SDM.get_system_sound_level() >= 2 else None

    app = QApplication([])
    excel_file, _ = QFileDialog.getOpenFileName(None, "Select Excel File", "./data", "Excel Files (*.xlsx)")

    return excel_file


def autoscan(excel_file, duplicates=False, abc=True, abc_ascending=True, test_for_invalides=True):

    data = pd.read_excel(excel_file)

    # Get the values from the first column
    terms = data.iloc[:, 0].dropna().tolist()
    if not duplicates:
        terms = list(dict.fromkeys(terms))  # eliminates duplicates
    if abc:
        if abc_ascending:
            terms = sorted(terms)           # alphabetical order (ascending)
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

        property_Cell = 'B' + str(excel_row)
        worksheet[property_Cell] = "common"

        file_Cell = 'C' + str(excel_row)
        worksheet[file_Cell] = "File 1: " + file_1 + "   +   File 2: " + file_2

        excel_row += 1

    return worksheet


def display_settings(setting, current_var, current_var_2=""):

    if setting == 1:
        print("\n\n\tSetting \33[33m1\33[0m/8: \33[33mDatabase Version Control\33[0m"
              "\n\t\33[33m[\33[0m-------\33[33m]\33[0m---------------------------------------------------------------"
              "\n\n\tDescription: "
              "\n\tHere you can delete or update the currently installed version of"
              "\n\tthe wikimorph database or just change its description."
              "\n\tOnly one database version can be installed so far.")

        if current_var == "":
            print("\n\tCurrently installed version:\t\33[91mNo version installed!\33[0m",
                  "\n\tInstallation date:\t\t\33[91mNo version installed!\33[0m")
        elif current_var != "" and current_var_2 == "":
            print("\n\tCurrently installed version:\t\33[91mNo description found!\33[0m",
                  "\n\tInstallation date:\t\t\33[92m" + SDM.get_database_version_date() + "\33[0m")
        else:
            print("\n\tCurrently installed version:\t\33[92m" + SDM.get_database_version_description() + "\33[0m",
                  "\n\tInstallation date:\t\t\33[92m" + SDM.get_database_version_date() + "\33[0m")

        print("\n\tOptions:"
              '\n\t\t\t1. Type in \33[94m1\33[0m to \33[94mupdate / reinstall\33[0m the database.'
              '\n\t\t\t2. Type in \33[33m2\33[0m to change the \33[33mdescription\33[0m '
              'for the currently installed version.'
              '\n\t\t\t3. Type in \33[91m3\33[0m to \33[91mremove (delete)\33[0m the currently installed version.'
              '\n\n\tPress \33[92menter\33[0m or type in anything else to \33[92mcontinue\33[0m without '
              'making changes.'
              '\n\tType in \33[91mexit!\33[0m to \33[91mreturn to main menu\33[0m.')

    elif setting == 2:
        print("\n\n\tSetting \33[33m2\33[0m/8: \33[33mTerm Output Diplomacy\33[0m"
              "\n\t---------\33[33m[\33[0m-------\33[33m]\33[0m------------------------------------------------------"
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
        print("\n\n\tSetting \33[33m3\33[0m/8: \33[33mOutput Format\33[0m"
              "\n\t------------------\33[33m[\33[0m-------\33[33m]\33[0m---------------------------------------------"
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
        print("\n\n\tSetting \33[33m4\33[0m/8: \33[33mHeadline Printing\33[0m"
              "\n\t---------------------------\33[33m[\33[0m-------\33[33m]\33[0m------------------------------------"
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
        print("\n\n\tSetting \33[33m5\33[0m/8: \33[33mAlphabetical Output Order\33[0m"
              "\n\t------------------------------------\33[33m[\33[0m-------\33[33m]\33[0m---------------------------"
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
        print("\n\n\tSetting \33[33m6\33[0m/8: \33[33mAutomatic Scan Filters\33[0m"
              "\n\t---------------------------------------------\33[33m[\33[0m-------\33[33m]\33[0m------------------"
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
        print("\n\n\tSetting \33[33m7\33[0m/8: \33[33mOutput Detail Level\33[0m"
              "\n\t------------------------------------------------------\33[33m[\33[0m-------\33[33m]\33[0m---------"
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
        print("\n\n\tSetting \33[33m8\33[0m/8: \33[33mSystem Sound Level\33[0m"
              "\n\t---------------------------------------------------------------\33[33m[\33[0m-------\33[33m]\33[0m"
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
        print("\n\n\tSetting \33[33m1\33[0m/8: \33[33mDatabase Version Control\33[0m"
              "\n\t\33[33m[\33[0m-------\33[33m]\33[0m---------------------------------------------------------------")

        if current_var == "u1":
            # update
            print("\n\t\33[33mNote:\33[0m This option allows you to install the latest version of the wikimorph database"
                  "\n\tdirectly from the Zenovo server. The procedure may take a while."
                  "\n\tPlease make sure you are connected to a reliable internet access before starting the download!")
        elif current_var == "d1":
            # change description
            print("\n\t\33[33mType in the new description for your installed version (max. 25 characters).\33[0m")
        elif current_var == "d2":
            print("\n\tDescription changed to \33[92m" + current_var_2 + "\33[0m!")
        elif current_var == "r1":
            print("\n\t\33[91mWarning:\33[0m"
                  "\n\tYou are about to delete the currently installed version of the wikimorph database!"
                  "\n\n\t1. Press \33[33menter\33[0m to \33[33mproceed\33[0m."
                  "\n\t2. Type in \33[91mexit!\33[0m to \33[91mreturn to settings menu without deleting\33[0m.")
        elif current_var == "r2":
            print("\n\t\33[92mDeletion successful!\33[0m"
                  "\n\tWikimorph version was removed."
                  "\n\n\tPress \33[33menter\33[0m to \33[33mproceed\33[0m.")

    elif setting == 2:
        print("\n\n\tSetting \33[33m2\33[0m/8: \33[33mTerm Output Diplomacy\33[0m"
              "\n\t---------\33[33m[\33[0m-------\33[33m]\33[0m------------------------------------------------------"
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
        print("\n\n\tSetting \33[33m3\33[0m/8: \33[33mOutput Format\33[0m"
              "\n\t------------------\33[33m[\33[0m-------\33[33m]\33[0m---------------------------------------------"
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
        print("\n\n\tSetting \33[33m4\33[0m/8: \33[33mHeadline Printing\33[0m"
              "\n\t---------------------------\33[33m[\33[0m-------\33[33m]\33[0m------------------------------------"
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
        print("\n\n\tSetting \33[33m5\33[0m/8: \33[33mAlphabetical Output Order\33[0m"
              "\n\t------------------------------------\33[33m[\33[0m-------\33[33m]\33[0m---------------------------"
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
        print("\n\n\tSetting \33[33m6\33[0m/8: \33[33mAutomatic Scan Filters\33[0m"
              "\n\t---------------------------------------------\33[33m[\33[0m-------\33[33m]\33[0m------------------"
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
        print("\n\n\tSetting \33[33m7\33[0m/8: \33[33mOutput Detail Level\33[0m"
              "\n\t------------------------------------------------------\33[33m[\33[0m-------\33[33m]\33[0m---------"
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
        print("\n\n\tSetting \33[33m8\33[0m/8: \33[33mSystem Sound Level\33[0m"
              "\n\t---------------------------------------------------------------\33[33m[\33[0m-------\33[33m]\33[0m"
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
