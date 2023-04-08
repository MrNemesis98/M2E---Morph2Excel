from PyQt5.QtCore import QEventLoop, QTimer, pyqtSignal

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

import GUI_Stylesheets as gss
import GUI_Text_Inputs as gti


def delay(milliseconds):
    dl = QEventLoop()
    QTimer.singleShot(milliseconds, dl.quit)
    dl.exec_()


class Initiator(QMainWindow):

    # System Variables

    closed = pyqtSignal()
    gui_mode = None
    general_memory = None

    def __init__(self):
        super().__init__()
        self.create_window()

        self.background_label = None
        self.chapter_label = None
        self.info_label = None
        self.user_name_input_item = None
        self.password_input_item = None
        self.checkbox = None
        self.design_label = None
        self.back_button = None
        self.forward_button = None
        self.start_button = None

        self.timer = QTimer()

        self.create_window()

    def create_window(self):
        # Main Properties
        self.setFixedSize(1000, 650)
        self.setWindowTitle("Morph2Excel")
        self.setWindowIcon(QIcon("data/GUI_img/17636.ico"))

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 1000, 650)
        self.background_label.setStyleSheet("background-color:black")
        self.background_label.show()

        # Headline Widgets
        self.chapter_label = QLabel(self)
        self.chapter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.chapter_label.setFont(QFont("Times New Roman", 16))
        self.chapter_label.setGeometry(-2, 0, 404, 60)

        self.design_label = QLabel(self)

        self.info_label = QLabel(self)
        self.info_label.setGeometry(50, 85, 300, 240)
        self.info_label.setWordWrap(True)
        self.info_label.setFont(QFont("Times New Roman", 14))
        self.info_label.setAlignment(QtCore.Qt.AlignVCenter)

        # self.text_input_item = GSI.SpecialTextEdit(self)
        # self.text_input_item.setAlignment(QtCore.Qt.AlignLeft)
        # self.text_input_item.setFont(QFont("Times New Roman", 12))
        # self.text_input_item.Change_Focus.connect(self.change_focus_of_text_item)
        # self.text_input_item.Enter_Event.connect(self.change_focus_of_text_item)

        """
        self.password_input_item = GSI.SpecialTextEdit(self)
        self.password_input_item.setStyleSheet(gss.text_input_item())
        self.password_input_item.setAlignment(QtCore.Qt.AlignLeft)
        self.password_input_item.setFont(QFont("Times New Roman", 12))
        self.password_input_item.Change_Focus.connect(self.change_focus_of_text_item)
        self.password_input_item.Enter_Event.connect(self.mode_login)
        """
        """
        self.checkbox = QCheckBox(self)
        self.checkbox.setFont(QFont("Times New Roman", 15))
        self.checkbox.setCheckable(True)
        self.checkbox.setStyleSheet(gss.checkbox())
        self.checkbox.clicked.connect(self.checkbox_clicked)
        """

        self.back_button = QPushButton(self)
        self.back_button.setFont(QFont("Times New Roman", 12))
        # self.back_button.clicked.connect(self.back_button_pressed)

        self.forward_button = QPushButton(self)
        self.forward_button.setFont(QFont("Times New Roman", 12))
        # self.forward_button.clicked.connect(self.forward_button_pressed)

        self.start_button = QPushButton(self)
        self.start_button.setFont(QFont("Times New Roman", 12))
        # self.start_button.clicked.connect(self.start_button_pressed)

        self.main_window()

    def main_window(self):
        self.gui_mode = "main_window"
        # self.update_system_parameters()

        self.chapter_label.setStyleSheet(gss.chapter_label())
        # self.design_label.setStyleSheet(gss.design_label())
        # self.info_label.setStyleSheet(gss.info_label(False, True))
        self.design_label.setGeometry(-2, 350, 404, 100)
        self.forward_button.setGeometry(75, 380, 250, 45)
        self.start_button.setGeometry(75, 470, 250, 45)
        self.back_button.setGeometry(75, 530, 250, 45)
        self.back_button.setText("Konfigurator starten")

        self.chapter_label.show()



