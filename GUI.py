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
        self.headline_label = None

        self.alpha_label = None
        self.alpha_headline = None
        self.alpha_info = None

        self.beta_label = None

        self.gamma_label = None

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

        # alpha widgets
        self.alpha_label = QLabel(self)
        self.alpha_label.setStyleSheet(GSS.menu_widgets_background_std())

        self.alpha_headline = QLabel(self)
        self.alpha_headline.setStyleSheet(GSS.menu_widgets_background_std())
        self.alpha_headline.setFont(QFont("Times New Roman", 25))

        self.alpha_info = QLabel(self)
        self.alpha_info.setStyleSheet(GSS.menu_widgets_background_std())
        self.alpha_info.setFont(QFont("Times New Roman", 20))
        self.alpha_info.setAlignment(Qt.AlignVCenter)

        # beta widgets
        self.beta_label = QLabel(self)
        self.beta_label.setStyleSheet(GSS.menu_widgets_background_std())

        # gamma widgets
        self.gamma_label = QLabel(self)
        self.gamma_label.setStyleSheet(GSS.menu_widgets_background_std())

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
        self.sub_alpha_button.setFont(QFont("Times New Roman", 20))
        self.sub_alpha_button.clicked.connect(self.sub_alpha_button_pressed)

        self.sub_beta_button = QPushButton(self)
        self.sub_beta_button.clicked.connect(self.sub_beta_button_pressed)

        self.sub_gamma_button = QPushButton(self)
        self.sub_gamma_button.clicked.connect(self.sub_gamma_button_pressed)

        self.sub_delta_button = QPushButton(self)
        self.sub_delta_button.clicked.connect(self.sub_delta_button_pressed)

        self.sub_epsilon_button = QPushButton(self)
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

        self.alpha_label.setGeometry(200, 250, 1500, 100)
        self.alpha_headline.setGeometry(250, 250, 1400, 100)
        self.alpha_headline.setAlignment(Qt.AlignVCenter)
        self.alpha_headline.setText("Database Status: not determined")

        self.sub_alpha_button.setGeometry(1290, 260, 400, 80)
        self.sub_alpha_button.setStyleSheet(GSS.sub_alpha_button(self.gui_mode))
        self.sub_alpha_button.setText("Determine Status")


        self.beta_label.setGeometry(200, 400, 1500, 550)




        
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
        pass

    def sub_beta_button_pressed(self):
        pass

    def sub_gamma_button_pressed(self):
        pass

    def sub_delta_button_pressed(self):
        pass

    def sub_epsilon_button_pressed(self):
        pass




