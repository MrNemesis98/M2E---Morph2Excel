sd = open("src/data/savedata.txt", "r")
data = sd.readlines()
sd.close()

# Sector 1: Manage database update informations ------------------------------------------------------------------------
database_data = data[0]
info_list = database_data.split('/')
info_list.remove(info_list[0])

download_size = int((info_list[0])[3:])
current_size = int((info_list[1])[2:])
soll_size = int((info_list[2])[5:])


def update_database_data():
    global download_size
    global current_size
    global soll_size

    # Save data from other sectors before overwriting
    sd = open("src/data/savedata.txt", "r")
    data = sd.readlines()
    history_data = data[1]
    sd.close()

    # Datei neu beschreiben, nur Datenbank Information updaten
    sd = open("src/data/savedata.txt", "w")
    text = "db:/dl:" + str(download_size) + "/c:" + str(current_size) + "/soll:" + str(soll_size) + "/" \
           + "\n" + system_data + "\n" + history_data
    sd.write(text)
    sd.close()


def get_download_size():
    global download_size
    return download_size


def set_download_size(size=0):
    global download_size
    download_size = size
    update_database_data()


def get_current_size():
    global current_size
    return current_size


def set_current_size(size=0):
    global current_size
    current_size = size
    update_database_data()


def get_soll_size():
    global soll_size
    return soll_size


# Sector 2: Manage system variables for console.py and GUI settings ----------------------------------------------------
system_data = data[1]
variables_list = system_data.split('/')
variables_list.remove(variables_list[0])
# print(variables_list)
auto_update = (variables_list[0].split(":")[1])
term_output_diplomacy = (variables_list[1].split(":")[1])
one_line_output = (variables_list[2].split(":")[1])
headline_printing = (variables_list[3].split(":")[1])
alphabetical_output = variables_list[4].split(":")
auto_scan_filters = variables_list[5].split(":")[1]
output_detail_level = (variables_list[6].split(":")[1])[:-1]


def update_system_data():
    global data
    global auto_update
    global term_output_diplomacy
    global one_line_output
    global headline_printing
    global alphabetical_output
    global auto_scan_filters
    global output_detail_level

    # Save data from other sectors before overwriting
    sd = open("src/data/savedata.txt", "r")
    data = sd.readlines()
    sd.close()

    # Datei neu beschreiben, nur Nutzer-Trainingsdaten updaten
    sd = open("src/data/savedata.txt", "w")
    text = database_data + "sys:" + \
           "/au:" + str(auto_update) + \
           "/tod:" + str(term_output_diplomacy) + \
           "/onel:" + str(one_line_output) + \
           "/hdlp:" + str(headline_printing) + \
           "/" + str(alphabetical_output[0]) + ":" + alphabetical_output[1] + \
           "/asf:" + str(auto_scan_filters) + \
           "/odlvl:" + str(output_detail_level) + "\n" + \
           history_data
    sd.write(text)
    # sd.write(text + "\n" + data[1] + data[2] + data[3] + data[4])
    sd.close()


def get_auto_update():
    global auto_update
    return int(auto_update)


def set_auto_update(au):
    global auto_update
    auto_update = au
    update_system_data()


def get_term_output_diplomacy():
    global term_output_diplomacy
    return int(term_output_diplomacy)


def set_term_output_diplomacy(tod):
    global term_output_diplomacy
    term_output_diplomacy = tod
    update_system_data()


def get_one_line_output():
    global one_line_output
    return True if one_line_output == "1" else False


def set_one_line_output(onel):
    global one_line_output
    one_line_output = "1" if onel else "0"
    update_system_data()


def get_headline_printing():
    global headline_printing
    return int(headline_printing)


def set_headline_printing(hdlp):
    global headline_printing
    headline_printing = hdlp
    update_system_data()


def get_alphabetical_output():
    global alphabetical_output
    alphabetical = False
    ascending = False
    if alphabetical_output[0].split("=")[1] == "1":
        alphabetical = True
    if alphabetical_output[1].split("=")[1] == "1":
        ascending = True
    return alphabetical, ascending


def set_alphabetical_output(abc, asc):
    global alphabetical_output
    alphabetical_output[0] = "abc=1" if abc else "abc=0"
    alphabetical_output[1] = "asc=1" if asc else "asc=0"
    update_system_data()


def get_auto_scan_filters():
    global auto_scan_filters

    if "," in auto_scan_filters:
        return auto_scan_filters.split(",")
    else:
        return list(auto_scan_filters)


def set_auto_scan_filters(asf):
    global auto_scan_filters
    auto_scan_filters = asf
    update_system_data()


def get_output_detail_level():
    global output_detail_level
    return int(output_detail_level)


def set_output_detail_level(odlvl):
    global output_detail_level
    output_detail_level = odlvl
    update_system_data()


# Sector 3: Manage history of search entries ---------------------------------------------------------------------------
history_data = data[2]
entries_list = history_data.split('/')
entries_list.remove(entries_list[0])


def update_history_data():
    global data
    global entries_list

    # Save data from other sectors before overwriting
    sd = open("src/data/savedata.txt", "r")
    data = sd.readlines()
    sd.close()

    # Datei neu beschreiben, nur Nutzer-Trainingsdaten updaten
    sd = open("src/data/savedata.txt", "w")
    text = database_data + system_data + "h:"
    for entry in range(len(entries_list)):
        text += "/" + entries_list[entry]
    sd.write(text)
    # sd.write(text + "\n" + data[1] + data[2] + data[3] + data[4])
    sd.close()


def get_entry_history():
    global entries_list
    return entries_list


def add_entry_to_history(entry):
    global entries_list
    entries_list.insert(0, entry)
    update_history_data()


def delete_entry_history():
    global entries_list
    entries_list = []
    update_history_data()
