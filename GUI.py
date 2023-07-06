import sys

import requests
from PyQt5.QtCore import QEventLoop, QTimer, pyqtSignal
import threading

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from urllib3.exceptions import NameResolutionError, MaxRetryError

import GUI_Stylesheets as GSS
import GUI_Text_Inputs as GTI
import GUI_Special_Items as GSI
import savedata_manager as SDM
import time
import os
import console_assistance as CA


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
        self.headline_label = None

        self.alpha_label = None
        self.beta_label = None
        self.gamma_label = None
        self.delta_label = None

        self.alpha_headline = None
        self.alpha_info = None
        self.alpha_widget = None

        self.beta_headline = None
        self.beta_info = None
        self.beta_widget = None

        self.gamma_headline = None
        self.gamma_info = None
        self.gamma_widget = None

        self.delta_headline = None
        self.delta_info = None
        self.delta_widget = None

        self.mbl_alpha_button = None
        self.mbl_beta_button = None
        self.mbl_gamma_button = None
        self.mbl_delta_button = None
        self.mbl_epsilon_button = None
        self.mbl_zeta_button = None

        self.hlm_alpha_button = None
        self.hlm_beta_button = None
        self.hlm_gamma_button = None

        self.sub_alpha_button = None
        self.sub_beta_button = None
        self.sub_gamma_button = None
        self.sub_delta_button = None
        self.sub_epsilon_button = None

        self.timer = QTimer()

        self.create_window()

    # System Variables -------------------------------------------------------------------------------------------------

    closed = pyqtSignal()

    gui_mode = None
    menu_buttons_restricted = False
    entries_history = None
    database_status = 0

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
        self.menu_bar_label.setGeometry(0, 0, 100, 1000)
        self.menu_bar_label.setStyleSheet(GSS.menu_bar_label())
        self.menu_bar_label.show()

        self.headline_label = QLabel(self)
        self.headline_label.setGeometry(150, 15, 1650, 150)
        self.headline_label.setStyleSheet(GSS.headline_label())
        self.headline_label.setFont(QFont("Times New Roman", 35))
        self.headline_label.setAlignment(Qt.AlignVCenter)
        self.headline_label.show()

        self.alpha_label = QLabel(self)
        self.alpha_label.setStyleSheet(GSS.menu_widgets_background_std())

        self.beta_label = QLabel(self)
        self.beta_label.setStyleSheet(GSS.menu_widgets_background_std())

        self.gamma_label = QLabel(self)
        self.gamma_label.setStyleSheet(GSS.menu_widgets_background_std())

        self.delta_label = QLabel(self)
        self.delta_label.setStyleSheet(GSS.menu_widgets_background_std())

        # alpha widgets
        self.alpha_headline = QLabel(self)
        self.alpha_headline.setStyleSheet(GSS.menu_widgets_background_std())
        self.alpha_headline.setFont(QFont("Times New Roman", 25))

        self.alpha_info = QLabel(self)
        self.alpha_info.setStyleSheet(GSS.menu_widgets_background_std())
        self.alpha_info.setFont(QFont("Times New Roman", 20))
        self.alpha_info.setAlignment(Qt.AlignVCenter)

        self.alpha_widget = QLabel(self)

        # beta widgets
        self.beta_headline = QLabel(self)
        self.beta_headline.setStyleSheet(GSS.menu_widgets_background_std())
        self.beta_headline.setFont(QFont("Times New Roman", 25))

        self.beta_info = QLabel(self)
        self.beta_info.setStyleSheet(GSS.menu_widgets_background_std())
        self.beta_info.setFont(QFont("Times New Roman", 20))
        self.beta_info.setAlignment(Qt.AlignVCenter)

        self.beta_widget = QLabel(self)

        # gamma widgets
        self.gamma_headline = QLabel(self)
        self.gamma_headline.setStyleSheet(GSS.menu_widgets_background_std())
        self.gamma_headline.setFont(QFont("Times New Roman", 25))

        self.gamma_info = QLabel(self)
        self.gamma_info.setStyleSheet(GSS.menu_widgets_background_std())
        self.gamma_info.setFont(QFont("Times New Roman", 20))
        self.gamma_info.setAlignment(Qt.AlignVCenter)

        self.gamma_widget = QLabel(self)

        # delta widgets
        self.delta_headline = QLabel(self)
        self.delta_headline.setStyleSheet(GSS.menu_widgets_background_std())
        self.delta_headline.setFont(QFont("Times New Roman", 25))

        self.delta_info = QLabel(self)
        self.delta_info.setStyleSheet(GSS.menu_widgets_background_std())
        self.delta_info.setFont(QFont("Times New Roman", 20))
        self.delta_info.setAlignment(Qt.AlignVCenter)

        self.delta_widget = QLabel(self)

        # Buttons ------------------------------------------------------------------------------------------------------

        self.mbl_alpha_button = QPushButton(self)
        self.mbl_alpha_button.setGeometry(0, 40, 100, 100)
        self.mbl_alpha_button.clicked.connect(self.mbl_alpha_button_pressed)

        self.mbl_beta_button = QPushButton(self)
        self.mbl_beta_button.setGeometry(0, 300, 100, 100)
        self.mbl_beta_button.clicked.connect(self.mbl_beta_button_pressed)

        self.mbl_gamma_button = QPushButton(self)
        self.mbl_gamma_button.setGeometry(0, 420, 100, 100)
        self.mbl_gamma_button.clicked.connect(self.mbl_gamma_button_pressed)

        self.mbl_delta_button = QPushButton(self)
        self.mbl_delta_button.setGeometry(0, 540, 100, 100)
        self.mbl_delta_button.clicked.connect(self.mbl_delta_button_pressed)

        self.mbl_epsilon_button = QPushButton(self)
        self.mbl_epsilon_button.setGeometry(0, 660, 100, 100)
        self.mbl_epsilon_button.clicked.connect(self.mbl_epsilon_button_pressed)

        self.mbl_zeta_button = QPushButton(self)
        self.mbl_zeta_button.setGeometry(0, 880, 100, 100)
        self.mbl_zeta_button.clicked.connect(self.mbl_zeta_button_pressed)

        self.hlm_alpha_button = QPushButton(self)
        self.hlm_alpha_button.setGeometry(1450, 40, 100, 100)
        self.hlm_alpha_button.clicked.connect(self.hlm_alpha_button_pressed)

        self.hlm_beta_button = QPushButton(self)
        self.hlm_beta_button.setGeometry(1550, 40, 100, 100)
        self.hlm_beta_button.clicked.connect(self.hlm_beta_button_pressed)

        self.hlm_gamma_button = QPushButton(self)
        self.hlm_gamma_button.setGeometry(1650, 40, 100, 100)
        self.hlm_gamma_button.clicked.connect(self.hlm_gamma_button_pressed)

        self.sub_alpha_button = QPushButton(self)
        self.sub_alpha_button.setFont(QFont("Times New Roman", 18))
        self.sub_alpha_button.clicked.connect(self.sub_alpha_button_pressed)

        self.sub_beta_button = QPushButton(self)
        self.sub_beta_button.setFont(QFont("Times New Roman", 18))
        self.sub_beta_button.clicked.connect(self.sub_beta_button_pressed)

        self.sub_gamma_button = QPushButton(self)
        self.sub_gamma_button.setFont(QFont("Times New Roman", 18))
        self.sub_gamma_button.clicked.connect(self.sub_gamma_button_pressed)

        self.sub_delta_button = QPushButton(self)
        self.sub_delta_button.setFont(QFont("Times New Roman", 18))
        self.sub_delta_button.clicked.connect(self.sub_delta_button_pressed)

        self.sub_epsilon_button = QPushButton(self)
        self.sub_epsilon_button.setFont(QFont("Times New Roman", 20))
        self.sub_epsilon_button.clicked.connect(self.sub_epsilon_button_pressed)
        """
        self.mbl_eta_button = QPushButton(self)
        self.mbl_eta_button.setGeometry(0, 770, 100, 100)
        self.mbl_eta_button.setStyleSheet(GSS.mbl_alpha_button())

        self.mbl_theta_button = QPushButton(self)
        self.mbl_theta_button.setGeometry(0, 885, 100, 100)
        self.mbl_theta_button.setStyleSheet(GSS.mbl_alpha_button())
        """

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

        self.home_menu()

    #  MENUS ***********************************************************************************************************

    def home_menu(self):
        self.gui_mode = "home_menu"
        self.headline_label.setText("Overview")
        self.mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button(selected=True))
        self.mbl_beta_button.setStyleSheet(GSS.mbl_beta_button())
        self.mbl_gamma_button.setStyleSheet(GSS.mbl_gamma_button())
        self.mbl_delta_button.setStyleSheet(GSS.mbl_delta_button())
        self.mbl_epsilon_button.setStyleSheet(GSS.mbl_epsilon_button())
        self.mbl_zeta_button.setStyleSheet(GSS.mbl_zeta_button())
        self.hlm_alpha_button.setStyleSheet(GSS.hlm_alpha_button())
        self.hlm_beta_button.setStyleSheet(GSS.hlm_beta_button())
        self.hlm_gamma_button.setStyleSheet(GSS.hlm_gamma_button())

    def database_menu(self):
        self.gui_mode = "database_menu"
        self.headline_label.setText("Wikimorph Database")

        self.mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button())
        self.mbl_beta_button.setStyleSheet(GSS.mbl_beta_button(selected=True))
        self.mbl_gamma_button.setStyleSheet(GSS.mbl_gamma_button())
        self.mbl_delta_button.setStyleSheet(GSS.mbl_delta_button())
        self.mbl_epsilon_button.setStyleSheet(GSS.mbl_epsilon_button())
        self.mbl_zeta_button.setStyleSheet(GSS.mbl_zeta_button())
        self.hlm_alpha_button.setStyleSheet(GSS.hlm_alpha_button())
        self.hlm_beta_button.setStyleSheet(GSS.hlm_beta_button())
        self.hlm_gamma_button.setStyleSheet(GSS.hlm_gamma_button())

        # upper widget / status description / log
        self.alpha_label.setGeometry(200, 250, 1500, 100)

        self.alpha_headline.setGeometry(250, 250, 1400, 100)
        self.alpha_headline.setAlignment(Qt.AlignVCenter)
        self.alpha_headline.setText("Database Status: not determined")

        self.sub_alpha_button.setGeometry(1290, 260, 400, 80)
        self.sub_alpha_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=True, var1="green"))
        self.sub_alpha_button.setText("Determine Status")

        # secondary widget / loading bar / options
        self.beta_label.setGeometry(200, 400, 1500, 550)

        self.alpha_widget.setGeometry(220, 450, 350, 50)
        self.beta_widget.setGeometry(590, 450, 350, 50)
        self.gamma_widget.setGeometry(960, 450, 350, 50)
        self.delta_widget.setGeometry(1330, 450, 350, 50)

        if self.database_status == 0:
            self.alpha_widget.setStyleSheet(GSS.loading_bar_widget(ascending="None", green=False, red=False))
            self.beta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="None", green=False, red=False))
            self.gamma_widget.setStyleSheet(GSS.loading_bar_widget(ascending="None", green=False, red=False))
            self.delta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="None", green=False, red=False))
        elif self.database_status == 1:
            self.alpha_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
            self.beta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="None", green=False, red=False))
            self.gamma_widget.setStyleSheet(GSS.loading_bar_widget(ascending="None", green=False, red=False))
            self.delta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="None", green=False, red=False))
        elif self.database_status == 2:
            self.alpha_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
            self.beta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="false", green=True, red=False))
            self.gamma_widget.setStyleSheet(GSS.loading_bar_widget(ascending="None", green=False, red=False))
            self.delta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="None", green=False, red=False))
        elif self.database_status == 3:
            self.alpha_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
            self.beta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="false", green=True, red=False))
            self.gamma_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
            self.delta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="None", green=False, red=False))
        else:
            self.alpha_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
            self.beta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="false", green=True, red=False))
            self.gamma_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
            self.delta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="false", green=True, red=False))
        self.alpha_info.setGeometry(220, 520, 350, 100)
        self.alpha_info.setAlignment(Qt.AlignHCenter)
        self.alpha_info.setText("Path existent")
        self.beta_info.setGeometry(590, 520, 350, 100)
        self.beta_info.setAlignment(Qt.AlignHCenter)
        self.beta_info.setText("Connected to internet")
        self.gamma_info.setGeometry(960, 520, 350, 100)
        self.gamma_info.setAlignment(Qt.AlignHCenter)
        self.gamma_info.setText("Database installed")
        self.delta_info.setGeometry(1330, 520, 350, 100)
        self.delta_info.setAlignment(Qt.AlignHCenter)
        self.delta_info.setText("Database is up to date")

        self.sub_beta_button.setGeometry(220, 640, 350, 80)
        self.sub_beta_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=True, var1="gold"))
        self.sub_beta_button.setText("Configure Path")
        self.sub_gamma_button.setGeometry(590, 640, 350, 80)
        self.sub_gamma_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=True, var1="gold"))
        self.sub_gamma_button.setText("Open Internet Settings")
        self.sub_delta_button.setGeometry(960, 640, 350, 80)
        self.sub_delta_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=False))
        self.sub_delta_button.setText("Reinstall Database")
        self.sub_epsilon_button.setGeometry(1330, 640, 350, 80)
        self.sub_epsilon_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=False))
        self.sub_epsilon_button.setText("Update Database")


        
    def search_menu(self):
        self.gui_mode = "search_menu"
        self.headline_label.setText("Manual Term Search Menu")
        self.mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button())
        self.mbl_beta_button.setStyleSheet(GSS.mbl_beta_button())
        self.mbl_gamma_button.setStyleSheet(GSS.mbl_gamma_button(selected=True))
        self.mbl_delta_button.setStyleSheet(GSS.mbl_delta_button())
        self.mbl_epsilon_button.setStyleSheet(GSS.mbl_epsilon_button())
        self.mbl_zeta_button.setStyleSheet(GSS.mbl_zeta_button())
        self.hlm_alpha_button.setStyleSheet(GSS.hlm_alpha_button())
        self.hlm_beta_button.setStyleSheet(GSS.hlm_beta_button())
        self.hlm_gamma_button.setStyleSheet(GSS.hlm_gamma_button())

    def scan_menu(self):
        self.gui_mode = "scan_menu"
        self.headline_label.setText("Automatic Scan Menu")
        self.mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button())
        self.mbl_beta_button.setStyleSheet(GSS.mbl_beta_button())
        self.mbl_gamma_button.setStyleSheet(GSS.mbl_gamma_button())
        self.mbl_delta_button.setStyleSheet(GSS.mbl_delta_button(selected=True))
        self.mbl_epsilon_button.setStyleSheet(GSS.mbl_epsilon_button())
        self.mbl_zeta_button.setStyleSheet(GSS.mbl_zeta_button())
        self.hlm_alpha_button.setStyleSheet(GSS.hlm_alpha_button())
        self.hlm_beta_button.setStyleSheet(GSS.hlm_beta_button())
        self.hlm_gamma_button.setStyleSheet(GSS.hlm_gamma_button())

    def output_menu(self):
        self.gui_mode = "output_menu"
        self.headline_label.setText("Results")
        self.mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button())
        self.mbl_beta_button.setStyleSheet(GSS.mbl_beta_button())
        self.mbl_gamma_button.setStyleSheet(GSS.mbl_gamma_button())
        self.mbl_delta_button.setStyleSheet(GSS.mbl_delta_button())
        self.mbl_epsilon_button.setStyleSheet(GSS.mbl_epsilon_button(selected=True))
        self.mbl_zeta_button.setStyleSheet(GSS.mbl_zeta_button())
        self.hlm_alpha_button.setStyleSheet(GSS.hlm_alpha_button())
        self.hlm_beta_button.setStyleSheet(GSS.hlm_beta_button())
        self.hlm_gamma_button.setStyleSheet(GSS.hlm_gamma_button())

    def settings_menu(self):
        self.gui_mode = "settings_menu"
        self.headline_label.setText("Settings")
        self.mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button())
        self.mbl_beta_button.setStyleSheet(GSS.mbl_beta_button())
        self.mbl_gamma_button.setStyleSheet(GSS.mbl_gamma_button())
        self.mbl_delta_button.setStyleSheet(GSS.mbl_delta_button())
        self.mbl_epsilon_button.setStyleSheet(GSS.mbl_epsilon_button())
        self.mbl_zeta_button.setStyleSheet(GSS.mbl_zeta_button(selected=True))
        self.hlm_alpha_button.setStyleSheet(GSS.hlm_alpha_button())
        self.hlm_beta_button.setStyleSheet(GSS.hlm_beta_button())
        self.hlm_gamma_button.setStyleSheet(GSS.hlm_gamma_button())

    def account_menu(self):
        self.gui_mode = "account_menu"
        self.headline_label.setText("Account Settings")
        self.mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button())
        self.mbl_beta_button.setStyleSheet(GSS.mbl_beta_button())
        self.mbl_gamma_button.setStyleSheet(GSS.mbl_gamma_button())
        self.mbl_delta_button.setStyleSheet(GSS.mbl_delta_button())
        self.mbl_epsilon_button.setStyleSheet(GSS.mbl_epsilon_button())
        self.mbl_zeta_button.setStyleSheet(GSS.mbl_zeta_button())
        self.hlm_alpha_button.setStyleSheet(GSS.hlm_alpha_button(selected=True))
        self.hlm_beta_button.setStyleSheet(GSS.hlm_beta_button())
        self.hlm_gamma_button.setStyleSheet(GSS.hlm_gamma_button())

    def info_menu(self):
        self.gui_mode = "info_menu"
        self.headline_label.setText("Version Description")
        self.mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button())
        self.mbl_beta_button.setStyleSheet(GSS.mbl_beta_button())
        self.mbl_gamma_button.setStyleSheet(GSS.mbl_gamma_button())
        self.mbl_delta_button.setStyleSheet(GSS.mbl_delta_button())
        self.mbl_epsilon_button.setStyleSheet(GSS.mbl_epsilon_button())
        self.mbl_zeta_button.setStyleSheet(GSS.mbl_zeta_button())
        self.hlm_alpha_button.setStyleSheet(GSS.hlm_alpha_button())
        self.hlm_beta_button.setStyleSheet(GSS.hlm_beta_button(selected=True))
        self.hlm_gamma_button.setStyleSheet(GSS.hlm_gamma_button())

    def help_menu(self):
        self.gui_mode = "help_menu"
        self.headline_label.setText("Help & Instructions")
        self.mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button())
        self.mbl_beta_button.setStyleSheet(GSS.mbl_beta_button())
        self.mbl_gamma_button.setStyleSheet(GSS.mbl_gamma_button())
        self.mbl_delta_button.setStyleSheet(GSS.mbl_delta_button())
        self.mbl_epsilon_button.setStyleSheet(GSS.mbl_epsilon_button())
        self.mbl_zeta_button.setStyleSheet(GSS.mbl_zeta_button())
        self.hlm_alpha_button.setStyleSheet(GSS.hlm_alpha_button())
        self.hlm_beta_button.setStyleSheet(GSS.hlm_beta_button())
        self.hlm_gamma_button.setStyleSheet(GSS.hlm_gamma_button(selected=True))

    # Button Functions
    def mbl_alpha_button_pressed(self):
        if not self.menu_buttons_restricted:
            self.home_menu()

    def mbl_beta_button_pressed(self):
        if not self.menu_buttons_restricted:
            self.database_menu()

    def mbl_gamma_button_pressed(self):
        if not self.menu_buttons_restricted:
            self.search_menu()

    def mbl_delta_button_pressed(self):
        if not self.menu_buttons_restricted:
            self.scan_menu()

    def mbl_epsilon_button_pressed(self):
        if not self.menu_buttons_restricted:
            self.output_menu()

    def mbl_zeta_button_pressed(self):
        if not self.menu_buttons_restricted:
            self.settings_menu()

    def hlm_alpha_button_pressed(self):
        if not self.menu_buttons_restricted:
            self.account_menu()

    def hlm_beta_button_pressed(self):
        if not self.menu_buttons_restricted:
            self.info_menu()

    def hlm_gamma_button_pressed(self):
        if not self.menu_buttons_restricted:
            self.help_menu()

    def sub_alpha_button_pressed(self):
        if self.gui_mode == "database_menu":
            threading.Thread(target=self.check_database_status).start()

    def sub_beta_button_pressed(self):
        pass

    def sub_gamma_button_pressed(self):
        pass

    def sub_delta_button_pressed(self):
        pass

    def sub_epsilon_button_pressed(self):
        pass

    # program functions ################################################################################################
    def check_database_status(self):
        # check paths
        if self.database_status == 0:

            self.alpha_headline.setText("Determining database status...")
            self.sub_alpha_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=False))
            self.sub_beta_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=False))
            self.sub_gamma_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=False))
            self.sub_delta_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=False))
            self.sub_epsilon_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=False))
            self.alpha_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=False, red=True))
            time.sleep(1)
            self.alpha_headline.setText("Searching for path...")
            time.sleep(1)

            if not os.path.exists("src/database"):
                SDM.set_current_size()
                self.alpha_headline.setText("Warning: path folder does not exist!")
                time.sleep(2)
                self.alpha_headline.setText("Solving problem automatically...")
                os.makedirs("src/database")
                time.sleep(3)
                self.alpha_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
                self.alpha_headline.setText('Standard path established: "src/database')
                self.database_status = 1
                time.sleep(3)

            else:
                self.alpha_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
                self.alpha_headline.setText("Standard path existent")
                self.database_status = 1
                time.sleep(2)

        if self.database_status == 1:

            self.beta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=False, red=True))
            self.alpha_headline.setText("Checking internet connection...")
            time.sleep(1)
            try:
                url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
                response = requests.get(url, stream=True)

                self.beta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
                self.alpha_headline.setText("Your device is connected!")

            except NameResolutionError or MaxRetryError:
                self.alpha_headline.setText("Warning: Your device is not connected!")



            """
            try:
                url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
                response = requests.get(url, stream=True)
                remote_size = int(response.headers.get("Content-Length", 0))
                remote_size = int(remote_size / (1024 * 1024))

                os.system('cls')
                print("\n\tWarning: wiki_morph database could not be found on your system!"
                      "\n\tYou are free to download it automatically.")
                if remote_size == 0:
                    print("\tSize of file: unknown")
                else:
                    print("\tSize of file: " + str(remote_size) + "MB")
                print("\tDo you want to download it now? (y/n)")
                answer = input("\n\tanswer: ")

                if answer == "y":

                    SDM.set_download_size(remote_size)

                    normal = CA.download_database(url=url)

                    if normal:
                        current_size = os.path.getsize("data/wiki_morph.json")
                        current_size = int(current_size / (1024 * 1024))
                        SDM.set_current_size(current_size)

                        os.system('cls')
                        print("\n\n\tDownload completed! (" + str(current_size) + " MB)"
                              "\n\n\tDo you wish to search for terms now? (y/n)")
                        answer = input("\n\tanswer: ")
                        if answer == "n":
                            print("\n\tProgram will now terminate.")
                            time.sleep(3)
                            sys.exit(0)
                    else:
                        sys.exit()

                else:
                    CA.print_exit_without_download()
                time.sleep(1)

            except NameResolutionError or MaxRetryError:
                os.system('cls')
                print("\n\tWarning: Database is not installed currently."
                      "\n\n\tThis program offers the possibility to download the database automatically."
                      "\n\tBut for the moment there was no internet connection recognized."
                      "\n\tPlease make sure you are connected and restart the program."
                      "\n\tThe program will now terminate.")
                time.sleep(7)
                sys.exit(0)

        else:
            os.system('cls')
            current_size = os.path.getsize("data/wiki_morph.json")
            current_size = int(current_size / (1024 * 1024))
            soll_size = SDM.get_soll_size()

            if current_size < soll_size:
                print("\n\tWarning: the local database file does not cover the expected amount of information!"
                      "\n\n\t(Expected size: min. " + str(soll_size) + " MB)"
                      "\n\t(Local size: " + str(current_size) + " MB)"
                      "\n\n\tThis may be due to an interruption during the last downloading process."
                      "\n\tTo solve this problem you should reinstall the database by downloading it again."
                      "\n\tDo you want to start the download now? (y/n)")
                answer = input("\n\tanswer: ")

                if answer == "y":

                    SDM.set_current_size()
                    url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
                    response = requests.get(url, stream=True)
                    remote_size = int(response.headers.get("Content-Length", 0))
                    remote_size = int(remote_size / (1024 * 1024))

                    SDM.set_download_size(remote_size)
                    CA.download_database(url=url)

                    current_size = os.path.getsize("data/wiki_morph.json")
                    current_size = int(current_size / (1024 * 1024))
                    SDM.set_current_size(current_size)

                    check_for_updates_necessary = False
                    os.system('cls')
                    print("\n\n\tDownload completed! (" + str(current_size) + " MB)"
                          "\n\n\tDo you wish to search for terms now? (y/n)")
                    answer = input("\n\tanswer: ")
                    if answer == "n":
                        print("\n\tProgramm will now terminate.")
                        time.sleep(3)
                        sys.exit(0)

                else:
                    CA.print_exit_without_download()
            else:
                print("\n\tDatabase installed and available.")
            time.sleep(3)
            """


