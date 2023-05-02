import json, os, sys
import urllib.request
import time
import datetime
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Font
import subprocess


def create_logfile():
    now = datetime.datetime.now()
    date_format = "%d_%m_%Y_(%H_%M_%S)"
    formatted_date = now.strftime(date_format)

    log_title = "data/M2E_Log_(" + str(formatted_date) + ").txt"
    with open(log_title, "w") as log:
        log.write("Morph2Excel Log from " + str(formatted_date))
    log.close()

    return log_title


def create_excel():
    now = datetime.datetime.now()
    date_format = "%d_%m_%Y_(%H_%M_%S)"
    formatted_date = now.strftime(date_format)

    workbook_title = "data/M2E_Output_(" + str(formatted_date) + ").xlsx"
    # Eine neue Excel-Datei erstellen
    workbook = openpyxl.Workbook()

    # Eine Tabelle auswählen
    worksheet = workbook.active

    # Daten in die Tabelle schreiben
    worksheet['A1'] = 'Term'
    worksheet['B1'] = 'Part of Speech'
    worksheet['C1'] = 'Syllables'
    worksheet['D1'] = 'Definition'
    worksheet['E1'] = 'Morphemes'
    worksheet['A1'].font = Font(bold=True)
    worksheet['B1'].font = Font(bold=True)
    worksheet['C1'].font = Font(bold=True)
    worksheet['D1'].font = Font(bold=True)
    worksheet['E1'].font = Font(bold=True)

    for col in worksheet.iter_cols(min_row=1, max_row=1):
        for cell in col:
            cell.border = Border(bottom=Side(border_style='thin', color='000000'))  # untere Grenze

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
        print("\tdatabase installed and available.")


def search_for_terms(log_title, workbook_title):
    # loading database
    os.system('cls')
    print("\n\tLoading wiki_morph database...")
    with open("data/wiki_morph.json", "r", encoding="utf-8") as f:
        entries_list = json.load(f)
    os.system('cls')
    print("\n\tCompleted!")
    time.sleep(1.5)
    os.system('cls')
    print("\n\tYou can now use the search function as follows:")
    time.sleep(2)
    print("\n\t1) Please type in the term you want to search and press Enter.")
    time.sleep(.5)
    print("\t2) You are free to repeat this procedure till you end this program.")
    time.sleep(.5)
    print("\t3) You can only search for one term at the same time.")
    time.sleep(.5)
    print("\t4) To end this program you can type in 'exit!'.")
    time.sleep(.5)
    print("\t5) Results are saved into an .txt file (since version 1.1),"
          " which will open automatically when this program ends.")
    time.sleep(.5)

    # search function
    stop = False
    excel_row = 2
    workbook = load_workbook(workbook_title)
    worksheet = workbook.active

    while not stop:

        term = input("\n\tSearch term: ")
        os.system('cls')
        if term == "exit!":
            print("\n\tProgram terminated!")
            stop = True
        else:
            term_cell = "A" + str(excel_row)
            worksheet[term_cell] = term
            found_entries = 0
            excel_row += 1
            log_output = "\t------------------------------------------------------------\n\n\tWord: " + term
            final_output = "\t------------------------------------------------------------\n\n\tWord: " + term
            output = ""

            for x in range(len(entries_list)):

                for key, value in entries_list[x].items():

                    if key == "Word":
                        if value == term:
                            entry = entries_list[x]
                            keys = list(entry.keys())
                            output += "\n\t" + str(found_entries+1) + ")" + \
                                     "\t" + str(keys[1]) + ": " + str(entry[keys[1]]) + "\n" + \
                                     "\t\t" + str(keys[2]) + ": " + str(entry[keys[2]]) + "\n" + \
                                     "\t\t" + str(keys[3]) + ": " + str(entry[keys[3]]) + "\n" + \
                                     "\t\t" + str(keys[4]) + ": " + str(entry[keys[4]]) + "\n"
                            found_entries += 1

                            pos_cell = "B" + str(excel_row)
                            syll_cell = "C" + str(excel_row)
                            def_cell = "D" + str(excel_row)
                            morph_cell = "E" + str(excel_row)

                            worksheet[pos_cell] = str(entry[keys[1]])
                            worksheet[syll_cell] = str(entry[keys[2]])
                            worksheet[def_cell] = str(entry[keys[3]])
                            worksheet[morph_cell] = str(entry[keys[4]])

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
log_name = create_logfile()
wb_name = create_excel()
check_paths()
search_for_terms(log_name, wb_name)

