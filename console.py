import json, os, sys
import urllib.request
import time
import datetime
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Font


def get_datetime():
    now = datetime.datetime.now()
    date_format = "%d_%m_%Y_(%H_%M_%S)"
    formatted_date = now.strftime(date_format)
    return formatted_date


def create_logfile(fd):
    log_title = "data/M2E_Log_(" + str(fd) + ").txt"
    with open(log_title, "w") as log:
        log.write("Morph2Excel Log from " + str(fd))
    log.close()

    return log_title


def create_excel(fd):

    workbook_title = "data/M2E_Output_(" + str(fd) + ").xlsx"
    # Eine neue Excel-Datei erstellen
    workbook = openpyxl.Workbook()

    """
    for col in worksheet.iter_cols(min_row=1, max_row=1):
        for cell in col:
            cell.border = Border(bottom=Side(border_style='thin', color='000000'))  # untere Grenze
    """
    workbook.save(workbook_title)

    return workbook_title


def check_paths():
    time.sleep(2)
    os.system('cls')
    print("\n\tChecking for database status...")
    if not os.path.exists("data/wiki_morph.json"):
        os.system('cls')
        print("\n\tWarning: wiki_morph database could not be found on your system!"
              "\n\tDo you want to download it automatically? (y/n)")
        answer = input()
        if answer == "y":

            # Function for generating loading bar
            def progress(count, block_size, total_size):
                percent = int(count * block_size * 100 / total_size)
                sys.stdout.write("\r" + "[%-100s] %d%%" % ("#" * percent, percent))
                sys.stdout.flush()

            os.system('cls')
            print("\n\tDownloading wiki_morph...\n")
            url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
            urllib.request.urlretrieve(url, "data/wiki_morph.json", reporthook=progress)
            os.system('cls')
            print("\n\tDownload completed!"
                  "\n\tDo you wish to search for terms now? (y/n)")
            answer = input()
            if answer == "n":
                sys.exit(0)

        else:
            os.system('cls')
            print("\n\tDownload will not start.")
            time.sleep(1.5)
            os.system('cls')
            print("\n\tNotice: You have to download the database another time to use this program.")
            time.sleep(3)
            os.system('cls')
            print("\n\tProgram will now terminate. For downloading wiki_morph you can start it again.")
            sys.exit(0)
        time.sleep(1)
    else:
        os.system('cls')
        print("\n\tDatabase installed and available.")


def show_instructions():
    time.sleep(1.5)
    os.system('cls')
    print("\n\tInstructions:")
    time.sleep(.5)
    print("\n\t1) Please type in the term you want to SEARCH and press Enter.")
    time.sleep(.5)
    print("\t2) You are free to repeat this procedure till you end this program.")
    time.sleep(.5)
    print("\t3) You can only SEARCH for one term at the same time.")
    time.sleep(.5)
    print("\t4) To END this program you can type in 'exit!'.")
    time.sleep(.5)
    print("\t5) Results are saved into an excel file (.xlsx),"
          " which will open automatically after the end of the program.")
    time.sleep(.5)
    print("\t6) There is also a short logfile (.txt), which covers the search history.")
    time.sleep(.5)
    print("\t7) To FILTER your results you can define the part of speech characteristics of the term as follows:"
          '\n\n\tgeneral:     "term:PoS"'
          '\n\texamples:    "cool:Noun"  /  "cool:Adjective"  /  "hide:Verb"  /  "hide:Adjective:Adverb"'
          '\n\n\tThere are the following pos types you can filter on: '
          '(Noun, Verb, Adverb, Adjective, Preposition, Phrase).'
          '\n\tYou can search for more than one pos type by connecting them via ":" (see last example).')


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
    print('\tFor instructions type "i!".')
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
            show_instructions()

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

            term_Hcell = 'A' + str(excel_row)
            pos_Hcell = 'B' + str(excel_row)
            syll_Hcell = 'C' + str(excel_row)
            def_Hcell = 'D' + str(excel_row)
            morph_Hcell = 'E' + str(excel_row)

            worksheet[term_Hcell] = 'Term'
            worksheet[pos_Hcell] = 'PoS'
            worksheet[syll_Hcell] = 'Syllables'
            worksheet[def_Hcell] = 'Definition'
            worksheet[morph_Hcell] = 'Morphemes'

            worksheet[term_Hcell].font = Font(bold=True)
            worksheet[pos_Hcell].font = Font(bold=True)
            worksheet[syll_Hcell].font = Font(bold=True)
            worksheet[def_Hcell].font = Font(bold=True)
            worksheet[morph_Hcell].font = Font(bold=True)

            excel_row += 1

            term_cell = "A" + str(excel_row)
            worksheet[term_cell] = term
            found_entries = 0

            log_output = "\t------------------------------------------------------------\n\n\tWord: " + term
            final_output = "\t------------------------------------------------------------\n\n\tWord: " + term
            output = ""

            for x in range(len(entries_list)):

                # print(type(entries_list[x]))
                # print(entries_list[x])
                entry = entries_list[x]

                if entry["Word"] == term and entry["PoS"] in pos_filters:

                    keys = list(entry.keys())

                    """
                    Data Structure Level 1 ---------------------------------------------------------------------
                    """

                    pos_value = entry[keys[1]]
                    syllables_value = entry[keys[2]]
                    definition_value = entry[keys[3]]
                    morphemes_value = entry[keys[4]]

                    pos_cell = "B" + str(excel_row)
                    syll_cell = "C" + str(excel_row)
                    def_cell = "D" + str(excel_row)

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

                    """
                    Data Structure Level 2 ---------------------------------------------------------------------
                    """
                    if morphemes_value is not None:

                        affix_Hcell = 'E' + str(excel_row)
                        lang_Hcell = 'F' + str(excel_row)
                        sub_pos_Hcell = 'G' + str(excel_row)
                        mean_Hcell = 'H' + str(excel_row)
                        etcom_Hcell = 'I' + str(excel_row)

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

                            affix_cell = "E" + str(excel_row)
                            lang_cell = "F" + str(excel_row)
                            pos_cell = "G" + str(excel_row)
                            mean_cell = "H" + str(excel_row)

                            worksheet[affix_cell] = str(affix_value)
                            worksheet[lang_cell] = str(language_value)
                            worksheet[pos_cell] = str(sub_pos_value)
                            worksheet[mean_cell] = str(meaning_value)

                            excel_row += 1

                            """
                            Data Structure Level 3 -------------------------------------------------------------
                            """
                            if etcom_value is not None:

                                sub_affix_Hcell = 'I' + str(excel_row)
                                sub_lang_Hcell = 'J' + str(excel_row)
                                decoded_Hcell = 'K' + str(excel_row)
                                sub_sub_pos_Hcell = 'L' + str(excel_row)
                                sub_meaning_Hcell = 'M' + str(excel_row)

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

                                    sub_affix_cell = "I" + str(excel_row)
                                    sub_language_cell = "J" + str(excel_row)
                                    decoded_cell = "K" + str(excel_row)
                                    sub_sub_pos_cell = "L" + str(excel_row)
                                    sub_meaning_cell = "M" + str(excel_row)

                                    worksheet[sub_affix_cell] = str(sub_affix_value)
                                    worksheet[sub_language_cell] = str(sub_language_value)
                                    worksheet[decoded_cell] = str(decoded_value)
                                    worksheet[sub_sub_pos_cell] = str(sub_sub_pos_value)
                                    worksheet[sub_meaning_cell] = str(sub_meaning_value)

                                    excel_row += 1

            if found_entries == 0:
                final_output += "\n\tWarning: no results found for '" + term + "'."
                log_output += "\n\tWarning: no results found for '" + term + "'."

                pos_cell = "B" + str(excel_row)
                syll_cell = "C" + str(excel_row)
                def_cell = "D" + str(excel_row)
                morph_cell = "E" + str(excel_row)
                worksheet[pos_cell] = "N/V"
                worksheet[syll_cell] = "N/V"
                worksheet[def_cell] = "N/V"
                worksheet[morph_cell] = "N/V"
                excel_row += 1
            else:
                log_output += "\n\tEntries found: " + str(found_entries) + "\n"
                final_output += "\n\tEntries found: " + str(found_entries) + "\n"
                final_output += output
            print(final_output)

            log = open(log_title, "a", encoding="utf-8")
            log.write("\n\n" + log_output)
            log.close()

            workbook.save(workbook_title)


os.system('cls')
print("\033[32m" + "\n\tWelcome to Morph2Excel - the wiki_morph API!" + "\033[0m")
check_paths()
time.sleep(1.5)
formatted_date = get_datetime()
log_name = create_logfile(fd=formatted_date)
wb_name = create_excel(fd=formatted_date)
search_for_terms(log_name, wb_name)


# what to fix next?
# xlsx output: add filter column
# console output: add filter information
# multiple filter tests
# launch version 1.3c

# IMPORTANT: Proof version consistency with GitHub batches!


