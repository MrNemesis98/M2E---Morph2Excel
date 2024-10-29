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

This software accesses the A.I. generated wiki_morph database, introduced in
Yarbro, J.T., Olney, A.M. (2021). WikiMorph: Learning to Decompose
Words into Morphological Structures. In: Roll, I., McNamara, D.,
Sosnovsky, S., Luckin, R., Dimitrova, V. (eds) Artificial Intelligence in Education.
AIED 2021. Lecture Notes in Computer Science(), vol 12749. Springer,
Cham. https://doi.org/10.1007/978-3-030-78270-2_72
Copyright © 2021 Springer Nature Switzerland AG

The software as well as its handbook should be cited as follows:
Preidt, Till, Böker, S., Engel, J., Petri, A., Plock, L.-K., Sloykowski, C. & Arndt-Lappe, S.
(2024, September 30). M2E - Morph2Excel. Retrieved from osf.io/jrdn3
"""

import msvcrt
import os
import sys
import threading
import time
import console_assistance as CA
import savedata_manager as SDM

warning_message = True
request_error = SDM.get_request_error()


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


def calculate_tab_width():
    global warning_message
    global request_error

    # the following is a method for automatic text formatting inclusive exception handling
    # it is currently outsourced since tests showed that it´s more reliable to replace these
    # calculations be manual values, which is of course not system-dependent any more but can
    # avoid access problems regarding e.g. the cursor position
    """
    if not request_error == 1:

        try:
            row_0, col_0 = get_cursor_position()
            print("\t", end='', flush=True)
            time.sleep(0.01)
            row_1, col_1 = get_cursor_position()
            tab_width = col_1 - col_0

        except Exception as e:
            request_error = 1
            SDM.set_request_error(error_code=1)
            if warning_message:
                warning_message = False
                draw("\n\t\33[91mWarning: Your system denies access "
                     "\n\tto basic information of this console window!\33[0m"
                     "\n\n\tAccordingly M2E might encounter some minor formatting problems."
                     "\n\tThe functionality - especially your output results - will not be influenced."
                     "\n\n\tFor more information please have a look at chapter 3 of the user manual.")
                unblock_input()
                input("\n\n\t\33[92mPress Enter to continue.\33[0m")
                block_input()
            sys.stdout.write(f"\033[{30};{0}H")
            sys.stdout.flush()
            clear_screen_backwards(down_to_row=5)

            # emergency solution (will work on most systems properly):
            tab_width = 8

    else:
        tab_width = 8
    """

    tab_width = 8

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

    # the following is a method for automatic text formatting inclusive exception handling
    # it is currently outsourced since tests showed that it´s more reliable to replace these
    # calculations be manual values, which is of course not system-dependent any more but can
    # avoid access problems regarding e.g. the cursor position
    """
    if not request_error == 1:
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

            # optional: warning message like for function "calculate tab width"
            # -> but might be to annoying / repetitive if the error occurs often

            row = 40

            while row > down_to_row:
                move_cursor_to(row, 0)
                clear_line()
                time.sleep(delay)
                row -= 1

            move_cursor_to(down_to_row, 0)
            clear_line()

    else:
        row = 40

        while row > down_to_row:
            move_cursor_to(row, 0)
            clear_line()
            time.sleep(delay)
            row -= 1

        move_cursor_to(down_to_row, 0)
        clear_line()
    """

    row = 40

    while row > down_to_row:
        move_cursor_to(row, 0)
        clear_line()
        time.sleep(delay)
        row -= 1

    move_cursor_to(down_to_row, 0)
    clear_line()


