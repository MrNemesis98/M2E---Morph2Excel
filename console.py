import json, os, sys
import urllib.request
import time
import datetime
import subprocess


def create_logfile():
    now = datetime.datetime.now()
    date_format = "%d_%m_%Y_(%H_%M_%S)"
    formatted_date = now.strftime(date_format)

    log_title = "data/Morph2Excel_logfile_(" + str(formatted_date) + ").txt"
    with open(log_title, "w") as log:
        log.write("Morph2Excel Log from " + str(formatted_date))
    log.close()

    return log_title


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


def search_for_terms(log_title):
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

    while not stop:
        found = False

        term = input("\n\tSearch term: ")
        os.system('cls')
        if term == "exit!":
            print("\n\tProgram terminated!")
            stop = True
        else:

            found_entries = 0
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
            if found_entries == 0:
                final_output += "\n\tWarning: no results found for '" + term + "'."
            else:
                final_output += "\n\tEntries found: " + str(found_entries) + "\n"
                final_output += output
            print(final_output)
            log = open(log_title, "a")
            log.write("\n\n" + final_output)
            log.close()


os.system('cls')
print("\033[32m" + "\n\tWelcome to Morph2Excel - the wiki_morph API!" + "\033[0m")
log_name = create_logfile()
check_paths()
search_for_terms(log_name)
