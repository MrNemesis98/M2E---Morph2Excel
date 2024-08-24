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

import sys
from io import StringIO
import pygame

original_stdout = sys.stdout
fake_stdout = StringIO()
sys.stdout = fake_stdout

sys.stdout = original_stdout


def play_start_sound(file="./src/data/GUI_sound/start_sound.mp3"):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except pygame.error as e:

        print(f"\n\tWarning: notification sound could not be played!"
              f"\n\tDetail Message: {e}\n")

    finally:
        pygame.mixer.quit()


def play_request_sound(file="./src/data/GUI_sound/request_sound.mp3"):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except pygame.error as e:

        print(f"\n\tWarning: notification sound could not be played!"
              f"\n\tDetail Message: {e}\n")

    finally:
        pygame.mixer.quit()


def play_accept_sound(file="./src/data/GUI_sound/accept_sound.mp3"):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except pygame.error as e:

        print(f"\n\tWarning: notification sound could not be played!"
              f"\n\tDetail Message: {e}\n")

    finally:
        pygame.mixer.quit()


def play_deny_sound(file="./src/data/GUI_sound/deny_sound.mp3"):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except pygame.error as e:

        print(f"\n\tWarning: notification sound could not be played!"
              f"\n\tDetail Message: {e}\n")

    finally:
        pygame.mixer.quit()
