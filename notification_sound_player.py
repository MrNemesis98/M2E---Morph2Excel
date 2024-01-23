import pygame


def play_mp3(file):
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
