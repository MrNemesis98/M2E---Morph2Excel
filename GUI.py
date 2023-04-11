from PyQt5.QtCore import QEventLoop, QTimer, pyqtSignal

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

import GUI_Stylesheets as GSS
import GUI_Text_Inputs as GTI
import GUI_Special_Items as GSI
import savedata_manager as SDM


def delay(milliseconds):
    delay_event = QEventLoop()
    QTimer.singleShot(milliseconds, delay_event.quit)
    delay_event.exec_()


class Initiator(QMainWindow):

    # Creating Instance ------------------------------------------------------------------------------------------------
    def __init__(self):
        super().__init__()

        self.headline_label = None
        self.background_label = None
        self.main_button = None
        self.results_button = None
        self.settings_button = None
        self.search_bar = None
        self.alpha_button = None
        self.beta_button = None
        self.gamma_button = None

        self.timer = QTimer()

        self.create_window()

    # System Variables -------------------------------------------------------------------------------------------------

    closed = pyqtSignal()

    gui_mode = None
    results = None
    search_available = None
    general_memory = None
    entries_history = None

    # get current status -----------------------------------------------------------------------------------------------
    def update_system_parameters(self):
        self.entries_history = SDM.get_entry_history()
        print(self.entries_history)

    # creating items ---------------------------------------------------------------------------------------------------

    def create_window(self):
        # Main Properties
        self.setFixedSize(1800, 1000)
        self.setWindowTitle("Morph2Excel")
        self.setWindowIcon(QIcon("data/GUI_img/17636.ico"))

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 1800, 1000)
        self.background_label.setStyleSheet("background-color:black")
        self.background_label.show()

        # Labels
        self.headline_label = QLabel(self)
        self.headline_label.setGeometry(0, 0, 1800, 80)
        self.headline_label.setFont(QFont("Times New Roman", 25))
        self.headline_label.setAlignment(QtCore.Qt.AlignCenter)
        self.headline_label.setText("Morph2Excel - API for Wiki_Morph")

        """
        self.chapter_label = QLabel(self)
        self.chapter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.chapter_label.setFont(QFont("Times New Roman", 16))
        self.chapter_label.setGeometry(-2, 0, 404, 60)
        """
        """
        self.info_label = QLabel(self)
        self.info_label.setGeometry(50, 85, 300, 240)
        self.info_label.setWordWrap(True)
        self.info_label.setFont(QFont("Times New Roman", 14))
        self.info_label.setAlignment(QtCore.Qt.AlignVCenter)
        """

        # Buttons

        self.main_button = QPushButton(self)
        self.main_button.setGeometry(600, 80, 600, 80)
        self.main_button.setFont(QFont("Times New Roman", 20))
        self.main_button.setText("Main Menu")
        self.main_button.clicked.connect(self.main_menu)

        self.results_button = QPushButton(self)
        self.results_button.setGeometry(1200, 80, 600, 80)
        self.results_button.setFont(QFont("Times New Roman", 20))
        self.results_button.setText("Search Results")
        self.results_button.clicked.connect(self.results_menu)

        self.settings_button = QPushButton(self)
        self.settings_button.setGeometry(0, 80, 600, 80)
        self.settings_button.setFont(QFont("Times New Roman", 20))
        self.settings_button.setText("Settings")
        self.settings_button.clicked.connect(self.settings_menu)

        self.alpha_button = QPushButton(self)
        self.alpha_button.setFont(QFont("Times New Roman", 20))
        self.alpha_button.clicked.connect(self.alpha_button_pressed)

        self.beta_button = QPushButton(self)
        self.beta_button.setFont(QFont("Times New Roman", 20))
        self.beta_button.clicked.connect(self.beta_button_pressed)

        self.gamma_button = QPushButton(self)
        self.gamma_button.setFont(QFont("Times New Roman", 20))
        self.gamma_button.clicked.connect(self.gamma_button_pressed)

        # Special Items

        self.search_bar = GSI.SpecialTextEdit(self)
        self.search_bar.setAlignment(QtCore.Qt.AlignLeft)
        self.search_bar.setFont(QFont("Times New Roman", 12))
        self.search_bar.setAlignment(QtCore.Qt.AlignLeft)
        self.search_bar.setStyleSheet(GSS.search_bar())
        self.search_bar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.search_bar.textChanged.connect(self.check_search_bar_text)

        """
        self.checkbox = QCheckBox(self)
        self.checkbox.setFont(QFont("Times New Roman", 15))
        self.checkbox.setCheckable(True)
        self.checkbox.setStyleSheet(gss.checkbox())
        self.checkbox.clicked.connect(self.checkbox_clicked)
        """

        self.main_menu()

    # primary menus ----------------------------------------------------------------------------------------------------

    def main_menu(self):
        self.gui_mode = "main_menu"
        self.search_available = False
        # self.update_system_parameters()
        self.headline_label.setStyleSheet(GSS.headline_label(self.gui_mode))
        self.main_button.setStyleSheet(GSS.main_button(self.gui_mode))
        self.results_button.setStyleSheet(GSS.results_button(self.gui_mode))
        self.settings_button.setStyleSheet(GSS.settings_button(self.gui_mode))

        self.search_bar.setGeometry(700, 500, 400, 51)

        self.alpha_button.setGeometry(700, 600, 190, 50)
        self.alpha_button.setStyleSheet(GSS.alpha_button(False))
        self.alpha_button.setText("Search!")

        self.beta_button.setGeometry(910, 600, 190, 50)
        self.beta_button.setStyleSheet(GSS.beta_button(False))
        self.beta_button.setText("Clear")

        self.gamma_button.setGeometry(1500, 900, 200, 50)
        self.gamma_button.setStyleSheet(GSS.gamma_button())
        self.gamma_button.setText("Delete history")


        self.alpha_button.show()
        self.beta_button.show()
        self.gamma_button.show()
        self.search_bar.show()

        self.search_bar.print_placeholder_text(" Enter a search term...")
        self.search_bar.setFocus()

    def results_menu(self):
        self.gui_mode = "results_menu"
        # self.update_system_parameters()
        self.headline_label.setStyleSheet(GSS.headline_label(self.gui_mode))
        self.main_button.setStyleSheet(GSS.main_button(self.gui_mode))
        self.results_button.setStyleSheet(GSS.results_button(self.gui_mode))
        self.settings_button.setStyleSheet(GSS.settings_button(self.gui_mode))

    def settings_menu(self):
        self.gui_mode = "settings_menu"
        # self.update_system_parameters()
        self.headline_label.setStyleSheet(GSS.headline_label(self.gui_mode))
        self.main_button.setStyleSheet(GSS.main_button(self.gui_mode))
        self.results_button.setStyleSheet(GSS.results_button(self.gui_mode))
        self.settings_button.setStyleSheet(GSS.settings_button(self.gui_mode))

    # Button Functions
    def alpha_button_pressed(self):
        if self.gui_mode == "main_menu":
            if self.search_available:
                self.general_memory = self.search_bar.toPlainText()
                if "/" in self.general_memory:
                    self.general_memory = self.general_memory.replace("/", "")
                SDM.add_entry_to_history(self.general_memory)
                self.update_system_parameters()
                print(self.general_memory)

    def beta_button_pressed(self):
        if self.gui_mode == "main_menu":
            if self.search_available:
                self.search_bar.clear()

    def gamma_button_pressed(self):
        if self.gui_mode == "main_menu":
            SDM.delete_entry_history()
            self.update_system_parameters()

    def check_search_bar_text(self):
        if self.gui_mode == "main_menu":
            if self.search_bar.toPlainText() == "" \
                    or self.search_bar.toPlainText() == self.search_bar.placeholderText():
                self.search_available = False
                self.alpha_button.setStyleSheet(GSS.alpha_button(False))
                self.beta_button.setStyleSheet(GSS.beta_button(False))
            else:
                self.search_available = True
                self.alpha_button.setStyleSheet(GSS.alpha_button(True))
                self.beta_button.setStyleSheet(GSS.beta_button(True))






