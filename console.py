import json, os, sys
import urllib.request
import time


def check_paths():
    print("\nWelcome to Morph2Excel - the wiki_morph API!")
    time.sleep(1)
    os.system('cls')
    print("Checking for database status...")
    if not os.path.exists("data/wiki_morph.json"):
        print("\n\nWarning: wiki_morph database could not be found on your system!"
              "\nDo you want to download it automatically? (y/n)")
        answer = input()
        if answer == "y":

            # Function for generating loading bar
            def progress(count, block_size, total_size):
                percent = int(count * block_size * 100 / total_size)
                sys.stdout.write("\r" + "[%-100s] %d%%" % ("#" * percent, percent))
                sys.stdout.flush()

            print("\n\nDownloading wiki_morph...\n")
            url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
            urllib.request.urlretrieve(url, "data/wiki_morph.json", reporthook=progress)
            print("\n\nDownload completed!"
                  "\nDo you wish to search for terms now? (y/n)")
            answer = input()
            if answer == "n":
                sys.exit(0)

        else:
            print("\nDownload will not start."
                  "\n\nNotice: You have to download the database another time to use this program."
                  "\nProgram will now terminate. For downloading wiki_morph you can start it again.")
            sys.exit(0)
        time.sleep(1)


def search_for_terms():
    # loading database
    print("Loading wiki_morph database...")
    with open("data/wiki_morph.json", "r", encoding="utf-8") as f:
        entries_list = json.load(f)
    print("\n\nCompleted! \nYou can now use the search function as follows:")
    time.sleep(.5)
    print("1) Please type in the term you want to search and press Enter.")
    time.sleep(.5)
    print("2) You are free to repeat this procedure till you end this program.")
    time.sleep(.5)
    print("3) You can only search for one term at the same time.")
    time.sleep(.5)
    print("4) To end this program you can type in 'exit!'.")
    time.sleep(.5)
    print("5) Results are saved into an .txt file, which will open automatically when this program ends.")
    time.sleep(.5)

    # search function
    stop = False

    while not stop:
        found = False
        term = input("\nSearch term: ")

        if term == "exit!":
            print("\nProgram terminated!")
            sys.exit(0)
        else:
            for x in range(len(entries_list)):

                for key, value in entries_list[x].items():

                    if key == "Word":
                        if value == term:
                            entry = entries_list[x]
                            print(entry.keys())
                            print(entry.values())
                            first_value = next(iter(entry.values()))
                            print(type(first_value))
                            exit(0)
                            # found = True
            if not found:
                print("Warning: no results found for '" + term + "'")


time.sleep(1)
# check_paths()
search_for_terms()

# focus on console input and output
# -> first visualization regarding output
