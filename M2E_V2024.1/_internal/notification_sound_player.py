import sys
from io import StringIO

original_stdout = sys.stdout
fake_stdout = StringIO()
sys.stdout = fake_stdout

import pygame

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


# Test the sounds
# play_start_sound()
# play_request_sound()
# play_accept_sound()
# play_deny_sound()
