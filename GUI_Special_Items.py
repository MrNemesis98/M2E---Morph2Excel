from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, pyqtSignal, Qt


class SpecialTextEdit(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("")
        self.index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_letter)

    def add_letter(self):
        if self.index >= len(self.text):
            self.timer.stop()
        else:
            self.setPlaceholderText(self.placeholderText()[:-1] + self.text[self.index] + '.'
                                    if self.index < len(self.text) - 1
                                    else self.placeholderText()[:-1] + self.text[self.index])
            self.index += 1

    def print_placeholder_text(self, text):
        self.setPlaceholderText("")
        self.text = text
        self.index = 0
        self.timer.start(30)

    Change_Focus = pyqtSignal()
    Enter_Event = pyqtSignal()

    def keyPressEvent(self, event):
        if event.key() == 16777220:  # Enter key code
            self.Enter_Event.emit()
            return
        if event.key() == Qt.Key_Tab:
            self.Change_Focus.emit()
            return
        elif event.key() == Qt.Key_Enter:
            self.Change_Focus.emit()
            return
        QTextEdit.keyPressEvent(self, event)