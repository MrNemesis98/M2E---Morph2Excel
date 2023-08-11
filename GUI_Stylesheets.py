# labels ***************************************************************************************************************
def main_background_label():
    return "background-color:black"


def menu_bar_label():
    stylesheet = "background: qlineargradient" \
                 "(x1: 0, y1: 0, x2: 0, y2: 1, " \
                 "stop: 0 rgba(25, 25, 25, 255), stop: 1 rgba(20, 20, 20, 255));"
    return stylesheet


def headline_label():
    stylesheet = "color: white; background: qlineargradient" \
                 "(x1: 0, y1: 0, x2: 1, y2: 0, " \
                 "stop: 0 rgba(0, 0, 0, 255), stop: 1 rgba(25, 25, 25, 255));"
    return stylesheet


def menu_widgets_background_schema():
    stylesheet = "color: white; background: qlineargradient" \
                 "(x1: 0, y1: 0, x2: 20, y2: 20, " \
                 "stop: 0 rgba(30, 30, 30, 255), stop: 1 rgba(255, 0, 0, 255));" \
                 "border-radius: 25px;"
    return stylesheet


def menu_widgets_background_std(textcolor="grey"):
    stylesheet = ""
    if textcolor == "grey":
        stylesheet = "color: grey; background: qlineargradient" \
                     "(x1: 0, y1: 0, x2: 0, y2: 0, " \
                     "stop: 0 rgba(25, 25, 25, 255), stop: 1 rgba(255, 0, 0, 255));" \
                     "border-radius: 25px;"
    elif textcolor == "white":
        stylesheet = "color: white; background: qlineargradient" \
                     "(x1: 0, y1: 0, x2: 0, y2: 0, " \
                     "stop: 0 rgba(25, 25, 25, 255), stop: 1 rgba(255, 0, 0, 255));" \
                     "border-radius: 25px;"
    return stylesheet


def loading_bar_widget(ascending, green=False, red=False):
    if ascending == "false":
        if green:
            stylesheet = "border: 5px solid black; background: qlineargradient" \
                         "(x1: 0, y1: 0, x2: 1, y2: 0, " \
                         "stop: 0 rgba(15, 100, 15, 255), stop: 1 rgba(0, 50, 0, 255));"
        elif red:
            stylesheet = "border: 5px solid black; background: qlineargradient" \
                         "(x1: 0, y1: 0, x2: 1, y2: 0, " \
                         "stop: 0 rgba(100, 15, 15, 255), stop: 1 rgba(50, 0, 0, 255));"
        else:
            stylesheet = "border: 5px solid black; background: qlineargradient" \
                         "(x1: 0, y1: 0, x2: 1, y2: 0, " \
                         "stop: 0 rgba(100, 100, 100, 255), stop: 1 rgba(50, 50, 50, 255));"
    elif ascending == "true":
        if green:
            stylesheet = "border: 5px solid black; background: qlineargradient" \
                         "(x1: 0, y1: 0, x2: 1, y2: 0, " \
                         "stop: 0 rgba(0, 50, 0, 255), stop: 1 rgba(15, 100, 15, 255));"
        elif red:
            stylesheet = "border: 5px solid black; background: qlineargradient" \
                         "(x1: 0, y1: 0, x2: 1, y2: 0, " \
                         "stop: 0 rgba(50, 0, 0, 255), stop: 1 rgba(100, 15, 15, 255));"
        else:
            stylesheet = "border: 5px solid black; background: qlineargradient" \
                         "(x1: 0, y1: 0, x2: 1, y2: 0, " \
                         "stop: 0 rgba(50, 50, 50, 255), stop: 1 rgba(100, 100, 100, 255));"
    else:
        if green:
            stylesheet = "border: 5px solid black; background: qlineargradient" \
                         "(x1: 0, y1: 0, x2: 1, y2: 0, " \
                         "stop: 0 rgba(0, 50, 0, 255), stop: 1 rgba(0, 50, 0, 255));"
        elif red:
            stylesheet = "border: 5px solid black; background: qlineargradient" \
                         "(x1: 0, y1: 0, x2: 1, y2: 0, " \
                         "stop: 0 rgba(50, 0, 0, 255), stop: 1 rgba(50, 0, 0, 255));"
        else:
            stylesheet = "border: 5px solid black; background: qlineargradient" \
                         "(x1: 0, y1: 0, x2: 1, y2: 0, " \
                         "stop: 0 rgba(50, 50, 50, 255), stop: 1 rgba(50, 50, 50, 255));"
    return stylesheet


# buttons **************************************************************************************************************

def image_button_stylesheet(standard_link, hover_link, pressed_link, selected=False, accessable=True):
    if not accessable:
        locked_link_std = "src/data/GUI_img/Locked_Std.png"
        locked_link_sel = "src/data/GUI_img/Locked_Sel.png"
        stylesheet = "QPushButton {" \
                     "border-radius: 40pt;" \
                     "background-image: url(" + standard_link + ");" \
                     "background-repeat: no-repeat;" \
                     "background-position: center;" \
                     "background-color: transparent;}" \
                     "QPushButton:hover {" \
                     "background-image: url(" + locked_link_std + ");}" \
                     "QPushButton:pressed {" \
                     "background-image: url(" + locked_link_sel + ");}"

    elif selected:
        stylesheet = "QPushButton {" \
                     "border-radius: 40pt;" \
                     "background-image: url(" + pressed_link + ");" \
                     "background-repeat: no-repeat;" \
                     "background-position: center;" \
                     "background-color: transparent;}"
    else:
        stylesheet = "QPushButton {" \
         "border-radius: 40pt;"\
         "background-image: url(" + standard_link + ");" \
         "background-repeat: no-repeat;" \
         "background-position: center;" \
         "background-color: transparent;}" \
         "QPushButton:hover {" \
         "background-image: url(" + hover_link + ");}" \
         "QPushButton:pressed {" \
         "background-image: url(" + pressed_link + ");}"
    return stylesheet


def mbl_alpha_button(selected=False, accessable=True):
    standard_link = "src/data/GUI_img/Home_Std.png"
    hover_link = "src/data/GUI_img/Home_Sel.png"
    pressed_link = "src/data/GUI_img/Home_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected, accessable)


def mbl_beta_button(selected=False, accessable=True):
    standard_link = "src/data/GUI_img/Database_Std.png"
    hover_link = "src/data/GUI_img/Database_Sel.png"
    pressed_link = "src/data/GUI_img/Database_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected, accessable)


def mbl_gamma_button(selected=False, accessable=True):
    standard_link = "src/data/GUI_img/Search_Std.png"
    hover_link = "src/data/GUI_img/Search_Sel.png"
    pressed_link = "src/data/GUI_img/Search_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected, accessable)


def mbl_delta_button(selected=False, accessable=True):
    standard_link = "src/data/GUI_img/Scan_Std.png"
    hover_link = "src/data/GUI_img/Scan_Sel.png"
    pressed_link = "src/data/GUI_img/Scan_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected, accessable)


def mbl_epsilon_button(selected=False, accessable=True):
    standard_link = "src/data/GUI_img/Output_Std.png"
    hover_link = "src/data/GUI_img/Output_Sel.png"
    pressed_link = "src/data/GUI_img/Output_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected, accessable)


def mbl_zeta_button(selected=False, accessable=True):
    standard_link = "src/data/GUI_img/Settings_Std.png"
    hover_link = "src/data/GUI_img/Settings_Sel.png"
    pressed_link = "src/data/GUI_img/Settings_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected, accessable)


def hlm_alpha_button(selected=False, accessable=True):
    standard_link = "src/data/GUI_img/Account_Std.png"
    hover_link = "src/data/GUI_img/Account_Sel.png"
    pressed_link = "src/data/GUI_img/Account_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected, accessable)


def hlm_beta_button(selected=False, accessable=True):
    standard_link = "src/data/GUI_img/Info_Std.png"
    hover_link = "src/data/GUI_img/Info_Sel.png"
    pressed_link = "src/data/GUI_img/Info_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected, accessable)


def hlm_gamma_button(selected=False, accessable=True):
    standard_link = "src/data/GUI_img/Help_Std.png"
    hover_link = "src/data/GUI_img/Help_Sel.png"
    pressed_link = "src/data/GUI_img/Help_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected, accessable)


def sub_alpha_button(gm, accessible=True, var1=""):
    stylesheet = ""
    if not accessible:
        stylesheet = "QPushButton{background-color: rgba(25, 25, 25, 255); color: rgba(130, 130, 130, 255);" \
                     "text-align:center;border-radius:25;" \
                     "border-bottom:2px solid rgba(130, 130, 130, 255);border-left:2px solid rgba(130, 130, 130, 255);" \
                     "border-top:2px solid rgba(130, 130, 130, 255);border-right:2px solid rgba(130, 130, 130, 255);}"
        return stylesheet
    else:
        if gm == "database_menu":
            if var1 == "gold":
                stylesheet = "QPushButton{background-color: rgba(25, 25, 25, 255); color: olive;" \
                             "text-align:center;border-radius:25;" \
                             "border-bottom:2px solid olive;border-left:2px solid olive;" \
                             "border-top:2px solid olive;border-right:2px solid olive;}" \
                             "QPushButton::hover{color: gold;" \
                             "border-bottom:2px solid gold;border-left:2px solid gold;" \
                             "border-top:2px solid gold;border-right:2px solid gold;}" \
                             "QPushButton::pressed{background-color:gold; color:black;}"
            elif var1 == "green":
                stylesheet = "QPushButton{background-color: rgba(25, 25, 25, 255); color: green;" \
                             "text-align:center;border-radius:25;" \
                             "border-bottom:2px solid dark green;border-left:2px solid dark green;" \
                             "border-top:2px solid dark green;border-right:2px solid dark green;}" \
                             "QPushButton::hover{color: lime;" \
                             "border-bottom:2px solid lime;border-left:2px solid lime;" \
                             "border-top:2px solid lime;border-right:2px solid lime;}" \
                             "QPushButton::pressed{background-color:lime; color:black;}"
        return stylesheet
