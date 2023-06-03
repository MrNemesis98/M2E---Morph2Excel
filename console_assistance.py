import sys
import os
import urllib.request
import datetime
import openpyxl
import time


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


def download_database(url):
    def progress(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write("\r" + "\t[%-100s] %d%%" % ("#" * percent, percent))
        sys.stdout.flush()

    os.system('cls')
    print("\n\tDownloading wiki_morph...\n")
    urllib.request.urlretrieve(url, "data/wiki_morph.json", reporthook=progress)


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


def show_version_description():
    time.sleep(1.5)
    os.system('cls')
    print("\n\tWhat´s new in version 2.0?")
    time.sleep(.5)
    print("\n\t1) The instructions and this version description are new features, separated from the main function of "
          "searching terms in the database.")
    time.sleep(.5)
    print("\t2) This version introduces Part of Speech (PoS) filters, as described in the instructions.")
    time.sleep(.5)
    print("\t3) The excel output has got a new structure since the program is now able to capture morphological "
          "information up to the database´s maximum depth of three levels (etymology compound level).")
    time.sleep(.5)
    print("\t4) Smaller improvements on the function for automatic updating of the database.")
    time.sleep(.5)
    print("\t5) There is a new consistency test at the beginning of the program to proof whether the last download of "
          "the database was either successful or has been interrupted. This consistency data is saved to and managed "
          "by the file 'savedata.txt' and an external script savedata_manager.py.")
    time.sleep(.5)
    print("\t6) The created excel file will now open automatically after the program terminated correctly.")
    time.sleep(.5)
    print("\t7) General revision of the displayed text, supplemented by the addition of data size information.")
    time.sleep(.5)
