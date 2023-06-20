# labels ***************************************************************************************************************
def main_background_label():
    return "background-color:black"


def menu_bar_label():
    stylesheet = "background: qlineargradient" \
                 "(x1: 0, y1: 0, x2: 0, y2: 1, " \
                 "stop: 0 rgba(50, 50, 50, 255), stop: 1 rgba(40, 40, 40, 255));"
    return stylesheet


# buttons **************************************************************************************************************

def image_button_stylesheet(standard_link, hover_link, pressed_link, selected=False):
    if selected:
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


def mbl_alpha_button(selected=False):
    standard_link = "data/GUI_img/Home_Std.png"
    hover_link = "data/GUI_img/Home_Sel.png"
    pressed_link = "data/GUI_img/Home_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected)


def mbl_beta_button(selected=False):
    standard_link = "data/GUI_img/Database_Std.png"
    hover_link = "data/GUI_img/Database_Sel.png"
    pressed_link = "data/GUI_img/Database_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected)


def mbl_gamma_button(selected=False):
    standard_link = "data/GUI_img/Search_Std.png"
    hover_link = "data/GUI_img/Search_Sel.png"
    pressed_link = "data/GUI_img/Search_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected)


def mbl_delta_button(selected=False):
    standard_link = "data/GUI_img/Scan_Std.png"
    hover_link = "data/GUI_img/Scan_Sel.png"
    pressed_link = "data/GUI_img/Scan_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected)


def mbl_epsilon_button(selected=False):
    standard_link = "data/GUI_img/Output_Std.png"
    hover_link = "data/GUI_img/Output_Sel.png"
    pressed_link = "data/GUI_img/Output_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected)


def mbl_zeta_button(selected=False):
    standard_link = "data/GUI_img/Settings_Std.png"
    hover_link = "data/GUI_img/Settings_Sel.png"
    pressed_link = "data/GUI_img/Settings_Sel.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link, selected)
