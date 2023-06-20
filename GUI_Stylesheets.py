# labels ***************************************************************************************************************
def main_background_label():
    return "background-color:black"


def menu_bar_label():
    stylesheet = "background: qlineargradient" \
                 "(x1: 0, y1: 0, x2: 0, y2: 1, " \
                 "stop: 0 rgba(60, 60, 60, 255), stop: 1 rgba(55, 55, 55, 255));"
    return stylesheet


# buttons **************************************************************************************************************

def image_button_stylesheet(standard_link, hover_link, pressed_link):
    stylesheet = "QPushButton {" \
                 "background-image: url(" + standard_link + ");" \
                 "background-repeat: no-repeat;" \
                 "background-position: center;" \
                 "background-color: transparent;""}" \
                 "QPushButton:hover {" \
                 "background-image: url(" + hover_link + ");""}" \
                 "QPushButton:pressed {" \
                 "background-image: url(" + pressed_link + ");""}"
    return stylesheet


def mbl_alpha_button():
    standard_link = "data/GUI_img/check_S.png"
    hover_link = "data/GUI_img/check_M.png"
    pressed_link = "data/GUI_img/check_L.png"
    return image_button_stylesheet(standard_link, hover_link, pressed_link)
