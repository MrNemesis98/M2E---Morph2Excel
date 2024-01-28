
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

print("Morph2Excel")
