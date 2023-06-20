from PyQt5.QtCore import QEventLoop, QTimer, pyqtSignal
import threading

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


# CLASS DEFINITION *****************************************************************************************************
class Initiator(QMainWindow):

    # Creating Instance ------------------------------------------------------------------------------------------------
    def __init__(self):
        super().__init__()

        self.main_background_label = None
        self.menu_bar_label = None

        self.timer = QTimer()

        self.create_window()

    # System Variables -------------------------------------------------------------------------------------------------

    closed = pyqtSignal()

    gui_mode = None
    entries_history = None

    # get current status -----------------------------------------------------------------------------------------------
    def update_system_parameters(self):
        self.entries_history = SDM.get_entry_history()

    # creating items ---------------------------------------------------------------------------------------------------

    def create_window(self):

        # Main Properties ----------------------------------------------------------------------------------------------
        self.setFixedSize(1800, 1000)
        self.setWindowTitle("Morph2Excel Software")
        self.setWindowIcon(QIcon("data/GUI_img/17636.ico"))

        self.main_background_label = QLabel(self)
        self.main_background_label.setGeometry(0, 0, 1800, 1000)
        self.main_background_label.setStyleSheet(GSS.main_background_label())
        self.main_background_label.show()

        # Labels -------------------------------------------------------------------------------------------------------

        self.menu_bar_label = QLabel(self)
        self.menu_bar_label.setGeometry(0, 0, 120, 1000)
        self.menu_bar_label.setStyleSheet(GSS.menu_bar_label())
        self.menu_bar_label.show()

        # Buttons ------------------------------------------------------------------------------------------------------

        mbl_alpha_button = QPushButton(self)
        mbl_alpha_button.setGeometry(10, 50, 100, 100)
        mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button())

        mbl_beta_button = QPushButton(self)
        mbl_beta_button.setGeometry(10, 550, 100, 100)
        mbl_beta_button.setStyleSheet(GSS.mbl_alpha_button())

        mbl_gamma_button = QPushButton(self)
        mbl_gamma_button.setGeometry(10, 700, 100, 100)
        mbl_gamma_button.setStyleSheet(GSS.mbl_alpha_button())

        mbl_delta_button = QPushButton(self)
        mbl_delta_button.setGeometry(10, 850, 100, 100)
        mbl_delta_button.setStyleSheet(GSS.mbl_alpha_button())

        # Special Items ------------------------------------------------------------------------------------------------

        """
        self.search_bar = GSI.SpecialTextEdit(self)
        self.search_bar.setAlignment(QtCore.Qt.AlignLeft)
        self.search_bar.setFont(QFont("Times New Roman", 12))
        self.search_bar.setAlignment(QtCore.Qt.AlignLeft)
        self.search_bar.setStyleSheet(GSS.search_bar())
        self.search_bar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.search_bar.textChanged.connect(self.check_search_bar_text)

        self.checkbox = QCheckBox(self)
        self.checkbox.setFont(QFont("Times New Roman", 15))
        self.checkbox.setCheckable(True)
        self.checkbox.setStyleSheet(gss.checkbox())
        self.checkbox.clicked.connect(self.checkbox_clicked)
        """

        self.main_menu()

    #  MENUS ***********************************************************************************************************

    def main_menu(self):
        self.gui_mode = "main_menu"




    # Button Functions







