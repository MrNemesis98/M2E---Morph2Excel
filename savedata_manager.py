sd = open("data/savedata.txt", "r")
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
    sd = open("data/savedata.txt", "r")
    data = sd.readlines()
    history_data = data[1]
    sd.close()

    # Datei neu beschreiben, nur Datenbank Information updaten
    sd = open("data/savedata.txt", "w")
    text = "db:/dl:" + str(download_size) + "/c:" + str(current_size) + "/soll:" + str(soll_size) + "/" \
           + "\n" + history_data
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


# Sector 2: Manage history of search entries ---------------------------------------------------------------------------
history_data = data[1]
entries_list = history_data.split('/')
entries_list.remove(entries_list[0])


def update_history_data():
    global data
    global entries_list

    # Save data from other sectors before overwriting
    sd = open("data/savedata.txt", "r")
    data = sd.readlines()
    sd.close()

    # Datei neu beschreiben, nur Nutzer-Trainingsdaten updaten
    sd = open("data/savedata.txt", "w")
    text = "h:"
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
