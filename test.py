"""
print("\033[32m<- New!\033[0m df")  # grün
print("\033[33m<- Old!\033[0m df")  # gelb / gold
print("\033[91m<- Old!\033[0m df")  # (hell) rot
print("\033[92m<- Old!\033[0m df")  # neon grün
print("\033[93m<- Old!\033[0m df")  # neon gelb
print("\033[94m<- Old!\033[0m df")  # hell blau
print("\033[95m<- Old!\033[0m df")  # hell lila
print("\033[96m<- Old!\033[0m df")  # cyan / türkis
print("\033[38;5;130m<- Old!\033[0m df")  # braun
print("\033[97m<- Old!\033[0m df")  # neon weiß
"""
"""
import pygetwindow as gw

def set_console_window_size(width, height):
    # Erhalte das aktive Fenster (die Konsole)
    console_window = gw.getWindowsWithTitle("Dein Fenstertitel")

    # Überprüfe, ob das Fenster gefunden wurde
    if console_window:
        console_window = console_window[0]

        # Setze die Fenstergröße
        console_window.resizeTo(width, height)

print("Helloo World!")

# Rufe die Funktion auf, um die Fenstergröße zu setzen (z.B., 800x600)
set_console_window_size(800, 600)
"""
"""
import time
import sys

text = '\n\tI)  For \033[38;5;130mAutomatic scan mode\033[0m type \033[38;5;130ms!\033[0m instead of a term.'

for char in text:
    sys.stdout.write(char)
    sys.stdout.flush()
    time.sleep(0.05)  # Füge eine kurze Verzögerung (in Sekunden) zwischen den Buchstaben ein

# Füge eine neue Zeile am Ende hinzu
print()
"""
"""
import time

# Vor der Suche
start_time = time.time()

# Dein Suchprozess hier

# Nach der Suche
end_time = time.time()

# Zeitdifferenz in Minuten und Sekunden berechnen
elapsed_time_seconds = end_time - start_time
elapsed_minutes = int(elapsed_time_seconds // 60)
elapsed_seconds = int(elapsed_time_seconds % 60)
elapsed_seconds_formatted = "{:02d}".format(elapsed_seconds)
print(f"Die Suche dauerte {elapsed_minutes} Minuten und {elapsed_seconds} Sekunden.")

import subprocess
import webbrowser
import os

# subprocess.Popen(["r'file:./src/data/Externals/MEDEL_Report.pdf"], shell=True)
# webbrowser.open_new("./src/data/Externals/MEDEL_Report.pdf")
import os

# Get the current working directory
current_directory = os.getcwd()
print(current_directory)
instructions_pdf_path = r"\src\data\Externals\M2E_v3.0c_EAP_Handbook.pdf"
path = current_directory + instructions_pdf_path
# path = os.path.join(os.getcwd(), instructions_pdf_path)
print(path)
os.system(path)

import os


current_directory = os.getcwd()
print(current_directory)

# Fügen Sie doppelte Anführungszeichen um den Dateipfad hinzu
command = f'"{path}"'
os.system(command)

current_directory = os.getcwd()
# print(current_directory)
# path = os.path.join(current_directory, r"src\data\Externals\M2E_v3.0c_EAP_Handbook.pdf")
path = 'M2E_v3.0c_EAP_Handbook.pdf'
subprocess.Popen([path], shell=True)
"""