"""
print("\033[32m<- New!\033[0m df")  # grün
print("\033[33m<- Old!\033[0m df")  # gelb / gold
print("\033[91m<- Old!\033[0m df")  # (hell) rot
print("\033[92m<- Old!\033[0m df")  # neon grün
print("\033[93m<- Old!\033[0m df")  # neon gelb
print("\033[94m<- Old!\033[0m df")  # hell blau
print("\033[95m<- Old!\033[0m df")  # hell lila
print("\033[96m<- Old!\033[0m df")  # cyan / türkis
print("\033[38;5;130m<- Old!\033[0m df")  # cyan / türkis
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
"""
import speedtest

def check_speed():
    st = speedtest.Speedtest()

    # Get the best server
    st.get_best_server()

    # Download speed in bits per second
    download_speed = st.download()

    # Convert download speed to megabits per second
    download_speed_mbps = download_speed / 1_000_000

    # Display the results
    print(f"Download Speed: {download_speed_mbps:.2f} Mbps")

check_speed()
