import sys
from io import StringIO

# Speichern Sie den ursprünglichen Standard-Output
original_stdout = sys.stdout

# Erstellen Sie einen leeren StringIO-Puffer, um die Ausgabe abzufangen
fake_stdout = StringIO()

# Leiten Sie den Standard-Output auf den Puffer um
sys.stdout = fake_stdout

# Importieren Sie pygame (die Begrüßungsnachricht wird jetzt in fake_stdout geschrieben)
import pygame

# Setzen Sie den Standard-Output wieder auf den ursprünglichen Wert zurück
sys.stdout = original_stdout

# Jetzt können Sie pygame normal verwenden, ohne dass die Begrüßungsnachricht angezeigt wird


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


play_mp3("./src/data/GUI_sound/Signal.mp3")