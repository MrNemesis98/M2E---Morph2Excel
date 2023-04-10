def headline_label(gui_mode):
    if gui_mode == "main_menu":
        stylesheet = "background-color: black; color: white; border-bottom: 1px solid white;"
        return stylesheet
    elif gui_mode == "results_menu":
        stylesheet = "background-color: black; color: white; border-bottom: 1px solid green;"
        return stylesheet
    elif gui_mode == "settings_menu":
        stylesheet = "background-color: black; color: white; border-bottom: 1px solid orange;"
        return stylesheet


def chapter_label():
    stylesheet = "background-color: black; color: white; border-bottom: 2px solid blue;" \
                 "border-right: 2px solid blue; border-left:2px solid blue;" \
                 "border-bottom-right-radius: 40px; border-bottom-left-radius: 40px"
    return stylesheet


def main_button(gui_mode):
    if gui_mode == "main_menu":
        stylesheet = "QPushButton{background-color: black; color: white; text-align:center;" \
                     "border:4px solid; border-top-color: white;}"
        return stylesheet
    elif gui_mode == "results_menu":
        stylesheet = "QPushButton{background-color: black; color: grey;text-align:center;" \
                     "border:4px solid; border-bottom-color:green; border-top-color:green;" \
                     "border-right-color:green;" \
                     "border-bottom-right-radius: 40;}" \
                     "QPushButton::hover{color: white}" \
                     "QPushButton::pressed{color:white;}"
        return stylesheet
    elif gui_mode == "settings_menu":
        stylesheet = "QPushButton{background-color: black; color: grey;text-align:center;" \
                     "border:4px solid; border-bottom-color:orange; border-top-color:orange;" \
                     "border-left-color:orange;" \
                     "border-bottom-left-radius: 40;}" \
                     "QPushButton::hover{color: white}" \
                     "QPushButton::pressed{color:white;}"
        return stylesheet


def results_button(gui_mode):

    if gui_mode == "main_menu":
        stylesheet = "QPushButton{background-color: black; color: grey;text-align:center;" \
                     "border:4px solid; border-bottom-color:white; border-top-color:white; border-left-color:white;" \
                     "border-bottom-left-radius: 40;}" \
                     "QPushButton::hover{color: green}" \
                     "QPushButton::pressed{color:white;}"
        return stylesheet
    elif gui_mode == "results_menu":
        stylesheet = "QPushButton{background-color: black; color: white; text-align:center;" \
                     "border:4px solid; border-top-color: green;}"
        return stylesheet
    elif gui_mode == "settings_menu":
        stylesheet = "QPushButton{background-color: black; color: grey;text-align:center;" \
                     "border:4px solid; border-bottom-color:orange;border-top-color:orange;}" \
                     "QPushButton::hover{color: white}" \
                     "QPushButton::pressed{color:white;}"
        return stylesheet


def settings_button(gui_mode):
    if gui_mode == "main_menu":
        stylesheet = "QPushButton{background-color: black; color: grey;text-align:center;" \
                     "border:4px solid; border-right-color:white; border-top-color: white; border-bottom-color:white;" \
                     "border-bottom-right-radius: 40;}" \
                     "QPushButton::hover{color: orange}" \
                     "QPushButton::pressed{color:white;}"
        return stylesheet
    elif gui_mode == "results_menu":
        stylesheet = "QPushButton{background-color: black; color: grey;text-align:center;" \
                     "border:4px solid; border-bottom-color:green;border-top-color:green;}" \
                     "QPushButton::hover{color: orange}" \
                     "QPushButton::pressed{color:white;}"
        return stylesheet
    elif gui_mode == "settings_menu":
        stylesheet = "QPushButton{background-color: black; color: white; text-align:center;" \
                     "border:4px solid; border-top-color: orange;}"
        return stylesheet


def search_bar():
    stylesheet = "background-color: black; color: white; font-size:22pt;" \
                 "border-color:olive; border: 1px solid olive;"
    return stylesheet
