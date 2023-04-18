import json, os, sys
import urllib.request

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *

import GUI


def start_initiator():
    I_App = QApplication(sys.argv)
    I = GUI.Initiator()
    I.closed.connect(I_App.quit)
    I.show()
    I_App.exec()


def check_paths():
    if not os.path.exists("data"):
        print("Warnung: Der Speicherort für die WikiMorph-DatenBank wurde nicht gefunden.")
        os.makedirs("data")
        print("Das Problem wurde automatisch behoben. "
              "Allerdings müssen Sie die Datenbank neu herunterladen, wenn Sie dieses Programm nutzen möchten."
              "Soll die Datenbank jetzt heruntergeladen werden? (y/n)")
        answer = input()
        if answer == "y":

            # Funktion, um Fortschrittsbalken anzuzeigen
            def progress(count, block_size, total_size):
                percent = int(count * block_size * 100 / total_size)
                sys.stdout.write("\r" + "[%-100s] %d%%" % ("#" * percent, percent))
                sys.stdout.flush()

            print("Datenbank wird heruntergeladen...")
            url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
            urllib.request.urlretrieve(url, "data/wiki_morph.json", reporthook=progress)
        else:
            print("Download wird nicht ausgeführt.")

    else:
        if not os.path.exists("data/wiki_morph.json"):
            print("Warnung: Die Wiki_Morph Datenbank wurde unter dem Standard Pfad nicht gefunden."
                  "Möchten Sie die Datenbank erneut herunterladen?")
            answer = input()
            if answer == "y":

                # Funktion, um Fortschrittsbalken anzuzeigen
                def progress(count, block_size, total_size):
                    percent = int(count * block_size * 100 / total_size)
                    sys.stdout.write("\r" + "[%-100s] %d%%" % ("#" * percent, percent))
                    sys.stdout.flush()

                print("Datenbank wird heruntergeladen...")
                url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
                urllib.request.urlretrieve(url, "data/wiki_morph.json", reporthook=progress)
                print("Download abgeschlossen")
            else:
                print("Download wird nicht ausgeführt.")


# start_initiator()
# check_paths()


term = input()

# Lade die englische Flexionsdatei von Wiki_Morph
with open("data/wiki_morph.json", "r", encoding="utf-8") as f:
    entries_list = json.load(f)

for x in range(len(entries_list)):

    for key, value in entries_list[x].items():

        if key == "Word":
            if value == term:
                
                print(entries_list[x])


# focus on console input and output
# -> first visualizastion regarding output
