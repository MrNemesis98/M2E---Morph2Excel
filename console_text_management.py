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

        response = ''
        while True:
            if msvcrt.kbhit():
                char = msvcrt.getch().decode()
                response += char
                if char == 'R':
                    break

        response = response.lstrip('\033[').rstrip('R')
        row, col = map(int, response.split(';'))
        return row, col

    except Exception as e:

        # erster versuch der behebung des fehlers
        print("Unexpected error:", sys.exc_info()[0])
        time.sleep(10)
        get_cursor_position()



def calculate_tab_width():
    try:
        row_0, col_0 = get_cursor_position()
    except Exception as e:
        draw("\n\t\33[91mWarning: a fatal system error occurred.\33[0m\n\n\tThis can happen from time to time and "
             "will be solved with the next start. \n\tThe program will end automatically in a few seconds..")
        time.sleep(7)
        sys.exit(1)
    print("\t", end='', flush=True)
    try:
        row_1, col_1 = get_cursor_position()
    except Exception as e:
        draw("\n\t\33[91mWarning: a fatal system error occurred.\33[0m\n\n\tThis can happen from time to time and "
             "will be solved with the next start. \n\tThe program will end automatically in a few seconds..")
        time.sleep(7)
        sys.exit(1)
    tab_width = col_1 - col_0
    return tab_width


# 3. Functions for Working with Text -----------------------------------------------------------------------------------

def draw(text, clear=True, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print(end='', flush=True) if clear else print()


def stack(lines_of_text, clear=True, delay=0.1):
    for line in lines_of_text:
        print(line, end='', flush=True) if clear else print(line)
        time.sleep(delay)


def clear_screen_backwards(down_to_row=1, delay=0.01):

    def clear_line():
        sys.stdout.write("\033[2K")
        sys.stdout.flush()

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

        # erster versuch der behebung des fehlers
        print("Unexpected error:", sys.exc_info()[0],
              "\nautomatic cursor shift")
        time.sleep(10)

        move_cursor_to(20, 0)
        clear_screen_backwards(down_to_row, delay)
