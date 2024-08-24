import msvcrt
import sys
import threading
import time


# 1. Keyboard Input Management -----------------------------------------------------------------------------------------

block_input_flag = False
ignore_thread = None


def block_input():
    global block_input_flag, ignore_thread
    if not block_input_flag:
        block_input_flag = True
        ignore_thread = threading.Thread(target=ignore_inputs)
        ignore_thread.daemon = True
        ignore_thread.start()


def ignore_inputs():
    while block_input_flag:
        if msvcrt.kbhit():
            msvcrt.getch()
        time.sleep(0.01)


def unblock_input():
    global block_input_flag
    if block_input_flag:
        block_input_flag = False
        if ignore_thread:
            ignore_thread.join()


# 2. Basic Functions for Navigation ------------------------------------------------------------------------------------
def get_cursor_position():
    try:
        sys.stdout.write("\033[6n")
        sys.stdout.flush()

        # Antwort einlesen und verarbeiten
        response = ''
        while True:
            if msvcrt.kbhit():  # Überprüft, ob eine Taste gedrückt wurde
                char = msvcrt.getch().decode()
                response += char
                if char == 'R':
                    break

        # Response ist im Format '\033[{ROW};{COLUMN}R'
        response = response.lstrip('\033[').rstrip('R')
        row, col = map(int, response.split(';'))
        return row, col

    except Exception as e:
        get_cursor_position()


def calculate_tab_width():
    row_0, col_0 = get_cursor_position()
    print("\t", end='', flush=True)
    row_1, col_1 = get_cursor_position()
    tab_width = col_1 - col_0
    return tab_width


# 3. Functions for Working with Text -----------------------------------------------------------------------------------

def draw(text, clear=True, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()          # clear puffer / print content from puffer directly
        time.sleep(delay)
    print(end='', flush=True) if clear else print()


def stack(lines_of_text, clear=True, delay=0.1):
    for line in lines_of_text:
        print(line, end='', flush=True) if clear else print(line)
        time.sleep(delay)


def clear_screen_backwards(down_to_row=1, delay=0.01):

    def clear_line():
        sys.stdout.write("\033[2K")  # Löscht die aktuelle Zeile
        sys.stdout.flush()

    # Funktion, um den Cursor zu einer bestimmten Position zu setzen
    def move_cursor_to(row, col):
        sys.stdout.write(f"\033[{row};{col}H")
        sys.stdout.flush()

    try:
        row, col = get_cursor_position()

        while row > down_to_row:
            move_cursor_to(row, 0)
            clear_line()
            time.sleep(delay)
            row -= 1

        move_cursor_to(down_to_row, 0)
        clear_line()

    except Exception as e:
        clear_line()
