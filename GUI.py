import sys
import urllib.request, urllib.error

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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)

        self.progress_bar = None

        self.create_window()

    # System Variables -------------------------------------------------------------------------------------------------

    closed = pyqtSignal()

    gui_mode = None
    menu_buttons_restricted = False
    entries_history = None
    database_status = 0
    database_download_accessable = False

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
        self.alpha_headline.setStyleSheet(GSS.menu_widgets_background_std("white"))
        self.alpha_headline.setFont(QFont("Times New Roman", 25))

        self.alpha_info = QLabel(self)
        self.alpha_info.setStyleSheet(GSS.menu_widgets_background_std())
        self.alpha_info.setFont(QFont("Times New Roman", 20))
        self.alpha_info.setAlignment(Qt.AlignVCenter)

        self.alpha_widget = QLabel(self)

        # beta widgets
        self.beta_headline = GSI.SpecialLabel(self)
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

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

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
        self.alpha_info.setStyleSheet(GSS.menu_widgets_background_std())
        self.alpha_info.setText("Path existent")
        self.beta_info.setGeometry(590, 520, 350, 100)
        self.beta_info.setAlignment(Qt.AlignHCenter)
        self.beta_info.setStyleSheet(GSS.menu_widgets_background_std())
        self.beta_info.setText("Connected to internet")
        self.gamma_info.setGeometry(960, 520, 350, 100)
        self.gamma_info.setAlignment(Qt.AlignHCenter)
        self.gamma_info.setStyleSheet(GSS.menu_widgets_background_std())
        self.gamma_info.setText("Database installed")
        self.delta_info.setGeometry(1330, 520, 350, 100)
        self.delta_info.setAlignment(Qt.AlignHCenter)
        self.delta_info.setStyleSheet(GSS.menu_widgets_background_std())
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

        self.beta_headline.setGeometry(230, 780, 1460, 100)
        self.beta_headline.setStyleSheet(GSS.menu_widgets_background_std("white"))


        
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
        if self.gui_mode == "database_menu" and self.database_download_accessable:
            self.menu_buttons_restricted = True
            threading.Thread(target=self.download_database).start()

    def sub_epsilon_button_pressed(self):
        pass

    # program functions ################################################################################################

    def proof_selected_menu_button(self):
        if self.gui_mode == "home_menu":
            self.mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button(selected=True, accessable=False))
        elif self.gui_mode == "database_menu":
            self.mbl_beta_button.setStyleSheet(GSS.mbl_beta_button(selected=True, accessable=False))
        elif self.gui_mode == "search_menu":
            self.mbl_gamma_button.setStyleSheet(GSS.mbl_gamma_button(selected=True, accessable=False))
        elif self.gui_mode == "scan_menu":
            self.mbl_delta_button.setStyleSheet(GSS.mbl_delta_button(selected=True, accessable=False))
        elif self.gui_mode == "output_menu":
            self.mbl_epsilon_button.setStyleSheet(GSS.mbl_epsilon_button(selected=True, accessable=False))
        elif self.gui_mode == "settings_menu":
            self.mbl_zeta_button.setStyleSheet(GSS.mbl_zeta_button(selected=True, accessable=False))
        elif self.gui_mode == "account_menu":
            self.hlm_alpha_button.setStyleSheet(GSS.hlm_alpha_button(selected=True, accessable=False))
        elif self.gui_mode == "info_menu":
            self.hlm_beta_button.setStyleSheet(GSS.hlm_beta_button(selected=True, accessable=False))
        elif self.gui_mode == "help_menu":
            self.hlm_gamma_button.setStyleSheet(GSS.hlm_gamma_button(selected=True, accessable=False))

    def set_menu_buttons_restricted_access(self, engage=True):
        if engage:
            self.menu_buttons_restricted = True
            self.mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button(selected=False, accessable=False))
            self.mbl_beta_button.setStyleSheet(GSS.mbl_beta_button(selected=False, accessable=False))
            self.mbl_gamma_button.setStyleSheet(GSS.mbl_gamma_button(selected=False, accessable=False))
            self.mbl_delta_button.setStyleSheet(GSS.mbl_delta_button(selected=False, accessable=False))
            self.mbl_epsilon_button.setStyleSheet(GSS.mbl_epsilon_button(selected=False, accessable=False))
            self.mbl_zeta_button.setStyleSheet(GSS.mbl_zeta_button(selected=False, accessable=False))
            self.hlm_alpha_button.setStyleSheet(GSS.hlm_alpha_button(selected=False, accessable=False))
            self.hlm_beta_button.setStyleSheet(GSS.hlm_beta_button(selected=False, accessable=False))
            self.hlm_gamma_button.setStyleSheet(GSS.hlm_gamma_button(selected=False, accessable=False))
            self.proof_selected_menu_button()
        else:
            self.menu_buttons_restricted = False
            self.mbl_alpha_button.setStyleSheet(GSS.mbl_alpha_button(selected=False, accessable=True))
            self.mbl_beta_button.setStyleSheet(GSS.mbl_beta_button(selected=False, accessable=True))
            self.mbl_gamma_button.setStyleSheet(GSS.mbl_gamma_button(selected=False, accessable=True))
            self.mbl_delta_button.setStyleSheet(GSS.mbl_delta_button(selected=False, accessable=True))
            self.mbl_epsilon_button.setStyleSheet(GSS.mbl_epsilon_button(selected=False, accessable=True))
            self.mbl_zeta_button.setStyleSheet(GSS.mbl_zeta_button(selected=False, accessable=True))
            self.hlm_alpha_button.setStyleSheet(GSS.hlm_alpha_button(selected=False, accessable=True))
            self.hlm_beta_button.setStyleSheet(GSS.hlm_beta_button(selected=False, accessable=True))
            self.hlm_gamma_button.setStyleSheet(GSS.hlm_gamma_button(selected=False, accessable=True))
            self.proof_selected_menu_button()

    def update_progress(self):
        # Update the progress value (e.g., read it from a download operation)
        self.current_progress += 10

        # Update the progress bar value
        self.progress_bar.setValue(self.current_progress)

        # Adjust the progress bar color based on the progress
        if self.current_progress < self.total_size / 3:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
        elif self.current_progress < 2 * self.total_size / 3:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: yellow; }")
        else:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")

        # Check if the progress is complete and stop the timer
        if self.current_progress >= self.total_size:
            self.timer.stop()

    def check_database_status(self):
        self.set_menu_buttons_restricted_access()

        # check paths ------------------------
        if self.database_status == 0:

            self.alpha_headline.setText("Determining database status...")
            self.sub_alpha_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=False))
            self.sub_beta_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=False))
            self.sub_gamma_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=False))
            self.sub_delta_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=False))
            self.sub_epsilon_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, accessible=False))
            self.alpha_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=False, red=True))
            self.alpha_info.setStyleSheet(GSS.menu_widgets_background_std(textcolor="white"))
            time.sleep(1)
            self.alpha_headline.setText("Searching for path...")
            time.sleep(1)

            if not os.path.exists("src/database"):
                self.alpha_headline.setText("Warning: path folder does not exist!")
                time.sleep(2)
                self.alpha_headline.setText("Solving problem automatically...")
                os.makedirs("src/database")
                time.sleep(3)
                self.alpha_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
                self.alpha_headline.setText('Standard path established: "src/database/..."')
                self.database_status = 1
                time.sleep(3)

            else:
                self.alpha_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
                self.alpha_headline.setText("Standard path existent")
                self.sub_beta_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, True, "gold"))
                self.database_status = 1
                time.sleep(2)

        # check internet ----------------------------
        if self.database_status == 1:

            self.alpha_headline.setText("Checking internet connection...")
            self.beta_info.setStyleSheet(GSS.menu_widgets_background_std(textcolor="white"))
            self.beta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=False, red=True))
            self.sub_beta_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, False))
            self.sub_gamma_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, False))
            self.sub_gamma_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, False))
            time.sleep(1)
            try:
                url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
                response = requests.get(url, stream=True)

                self.alpha_headline.setText("Your device is connected!")
                self.beta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
                self.sub_beta_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, True, "gold"))
                self.sub_gamma_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, True, "gold"))
                self.database_status = 2
                time.sleep(2)

            except NameResolutionError or MaxRetryError:
                self.alpha_headline.setText("Warning: Your device is not connected!")
                time.sleep(1)
                self.beta_headline.setText("Please connect your device and restart the procedure!")

        # check database installation -------------------------------
        if self.database_status == 2:

            self.alpha_headline.setText("Checking database installation...")
            self.gamma_info.setStyleSheet(GSS.menu_widgets_background_std(textcolor="white"))
            self.gamma_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=False, red=True))
            time.sleep(2)

            if not os.path.exists("src/database/wiki_morph.json"):
                SDM.set_current_size()
                self.gamma_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=False, red=True))
                self.alpha_headline.setText("Warning: No installation found!")
                time.sleep(1)
                self.sub_delta_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, True, var1="green"))
                self.sub_delta_button.setText("Download Database")
                self.beta_headline.setText("Please download the database to continue.")
                self.database_download_accessable = True
            else:
                current_size = os.path.getsize("src/database/wiki_morph.json")
                current_size = int(current_size / (1024 * 1024))
                soll_size = SDM.get_soll_size()

                if current_size < soll_size:
                    self.gamma_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=False, red=True))
                    self.alpha_headline.setText("Warning: Installation error detected!")
                    self.beta_headline.setText("The local database was installed incompletely!")
                    time.sleep(5)
                    self.beta_headline.setText("Expected size: min. " + str(soll_size) +
                                               " MB\t\tLocal size: " + str(current_size) + " MB")
                    time.sleep(5)
                    self.beta_headline.setText("This may be due to an interruption during the last downloading process.")
                    time.sleep(5)
                    self.beta_headline.setText("Please reinstall the database to solve the problem.")
                    self.sub_delta_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode, True, "green"))
                    self.database_download_accessable = True
                else:
                    self.gamma_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
                    self.alpha_headline.setText("Installation found!")
                    self.database_status = 3
                    time.sleep(2)

        # check for updates ----------------------------
        if self.database_status == 3:

            self.alpha_headline.setText("Checking for Updates...")
            self.delta_info.setStyleSheet(GSS.menu_widgets_background_std(textcolor="white"))
            self.delta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=False, red=True))
            time.sleep(2)

            url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"
            current_size = SDM.get_current_size()

            try:
                response = requests.get(url, stream=True)
                remote_size = int(response.headers.get("Content-Length", 0))
                remote_size = int(remote_size / (1024 * 1024))

                if remote_size == 0:
                    self.alpha_headline.setText("Update check not possible!")
                    self.beta_headline.setText("The server does not provide the required information.")
                    time.sleep(4)
                    self.beta_headline.setText("You can just use the last recent locally installed version.")
                    time.sleep(5)
                else:
                    if current_size < remote_size:
                        self.beta_headline.setText("There is a new version of wikimorph database!")
                        time.sleep(4)
                        self.beta_headline.setText("You can either download the update or use the installed version.")
                        time.sleep(4)
                        self.beta_headline.setText("Update-size: " + str(remote_size) + " MB")
                    else:
                        self.delta_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
                        self.alpha_headline.setText("Installation is up to date!")
                        self.beta_headline.setText("You are using the newest version of wikimorph.")
                        time.sleep(3)
                        self.database_status = 4
            except NameResolutionError or MaxRetryError:
                self.alpha_headline.setText("Update check not possible!")
                self.beta_headline.setText("The internet connection was interrupted!")
                time.sleep(5)
                self.beta_headline.setText("Please recheck internet connection or use the installed wikimorph version.")

        self.set_menu_buttons_restricted_access(False)

    def download_database(self):

        self.progress_bar.setGeometry(230, 900, 1440, 25)

        def progress(count, block_size, total_size):
            self.progress_bar.setMaximum(total_size)
            self.progress_bar.setValue(count * block_size)

        url = "https://zenodo.org/record/5172857/files/wiki_morph.json?download=1"

        try:
            self.progress_bar.setValue(0)  # Reset the progress bar
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")
            self.progress_bar.show()  # Show the progress bar

            self.alpha_headline.setText("Status: Downloading wikimorph...")
            self.beta_headline.setText("Download in progress:")

            response = requests.get(url, stream=True)
            remote_size = int(response.headers.get("Content-Length", 0))
            remote_size = int(remote_size / (1024 * 1024))
            SDM.set_download_size(remote_size)

            urllib.request.urlretrieve(url, "src/database/wiki_morph.json", reporthook=progress)

            # Download completed
            self.progress_bar.setValue(self.progress_bar.maximum())  # Set progress to 100%
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
            self.gamma_widget.setStyleSheet(GSS.loading_bar_widget(ascending="true", green=True, red=False))
            self.alpha_headline.setText("Status: Download completed!")
            self.beta_headline.setText("Database is now installed.")
            time.sleep(3)
            self.beta_headline.setText("The search functions are now available.")

        except (urllib.error.URLError, urllib.error.HTTPError):
            self.alpha_headline.setText("Download failed!")

        # Hide the progress bar and reset system variables after the download
        self.progress_bar.hide()
        self.database_download_accessable = False


