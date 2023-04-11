sd = open("data/savedata.txt", "r")
data = sd.readlines()
sd.close()

# Sector 1: Manage history of search entries ---------------------------------------------------------------------------
history_data = data[0]
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
