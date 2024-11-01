"""
Copyright © MrNemesis98, GitHub, 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software. The software is provided “as is”, without warranty of any kind, express or implied, including but not
limited to the warranties of merchantability, fitness for a particular purpose and noninfringement.
In no event shall the author(s) or copyright holder(s) be liable for any claim, damages or other liability, whether
in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or
other dealings in the software.

This software accesses the A.I. generated wiki_morph database, introduced in
Yarbro, J.T., Olney, A.M. (2021). WikiMorph: Learning to Decompose
Words into Morphological Structures. In: Roll, I., McNamara, D.,
Sosnovsky, S., Luckin, R., Dimitrova, V. (eds) Artificial Intelligence in Education.
AIED 2021. Lecture Notes in Computer Science(), vol 12749. Springer,
Cham. https://doi.org/10.1007/978-3-030-78270-2_72
Copyright © 2021 Springer Nature Switzerland AG

The software as well as its handbook should be cited as follows:

Preidt, Till, Böker, S., Engel, J., Petri, A., Plock, L.-K., Sloykowski, C. & Arndt-Lappe, S.
(2024, September 30). M2E - Morph2Excel. Retrieved from osf.io/jrdn3

DOI 10.17605/OSF.IO/JRDN3
"""

sd = open("src/data/savedata.txt", "r")
data = sd.readlines()
sd.close()

# Sector 1: Manage database update information -------------------------------------------------------------------------
database_data = data[0]
database_data_list = database_data.split('/')
database_data_list.remove(database_data_list[0])

download_size = int((database_data_list[0])[3:])
current_size = int((database_data_list[1])[2:])
soll_size = int((database_data_list[2])[5:])
database_version_date = (database_data_list[3].split(":")[1])
database_version_description = (database_data_list[4].split(":")[1])
manual_file_path = (database_data_list[5].split(":")[1])


def update_database_data():
    global download_size
    global current_size
    global soll_size
    global database_version_date
    global database_version_description
    global manual_file_path

    # Save data from other sectors before overwriting
    sd = open("src/data/savedata.txt", "r")
    data = sd.readlines()
    system_data = data[1]
    sd.close()

    # write savedata.txt, update database data only
    sd = open("src/data/savedata.txt", "w")
    text = ("db:/dl:" + str(download_size) +
            "/c:" + str(current_size) +
            "/soll:" + str(soll_size) +
            "/date:" + str(database_version_date) +
            "/scritto:" + str(database_version_description) +
            "/manpath:" + str(manual_file_path) +
            "/\n" +
            system_data)
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


def get_database_version_date():
    global database_version_date
    return database_version_date


def set_database_version_date(date_as_string):
    global database_version_date
    database_version_date = date_as_string
    update_database_data()


def get_database_version_description():
    global database_version_description
    return database_version_description


def set_database_version_description(description):
    global database_version_description
    database_version_description = description
    update_database_data()


def get_database_version_as_text():
    global database_version_date
    if database_version_date == "":
        return "\t1) Wikimorph Version:\t\tno installation found"
    else:
        return "\t1) Wikimorph Version:\t\tversion from " + database_version_date


def get_manpath():
    global manual_file_path
    return str(manual_file_path)


# Sector 2: Manage system variables for console.py ---------------------------------------------------------------------
system_data = data[1]
variables_list = system_data.split('/')
variables_list.remove(variables_list[0])
first_start = (variables_list[0].split(":")[1])
term_output_policy = (variables_list[1].split(":")[1])
one_line_output = (variables_list[2].split(":")[1])
headline_printing = (variables_list[3].split(":")[1])
alphabetical_output = variables_list[4].split(":")
auto_scan_filters = variables_list[5].split(":")[1]
output_detail_level = (variables_list[6].split(":")[1])
system_sound_level = (variables_list[7].split(":")[1])
request_error = (variables_list[8].split(":")[1])


def update_system_data():
    global data
    global first_start
    global term_output_policy
    global one_line_output
    global headline_printing
    global alphabetical_output
    global auto_scan_filters
    global output_detail_level
    global system_sound_level
    global request_error

    # Save data from other sectors before overwriting
    sd = open("src/data/savedata.txt", "r")
    data = sd.readlines()
    sd.close()

    # write savedata.txt, update system data only
    sd = open("src/data/savedata.txt", "w")
    text = ((database_data + "sys:" +
             "/fs:" + str(first_start) +
             "/top:" + str(term_output_policy) +
             "/onel:" + str(one_line_output) +
             "/hdlp:" + str(headline_printing) +
             "/" + str(alphabetical_output[0]) + ":" + str(alphabetical_output[1]) +
             "/asf:" + str(auto_scan_filters) +
             "/odlvl:" + str(output_detail_level) +
             "/ssl:" + str(system_sound_level) +
             "/re:" + str(request_error) +
             "/\n"))
    sd.write(text)
    sd.close()


def get_first_start():
    global first_start
    return True if first_start == "1" else False


def set_first_start(fs=False):
    global first_start
    first_start = "1" if fs else "0"
    update_system_data()


def get_term_output_policy():
    global term_output_policy
    return int(term_output_policy)


def get_term_output_policy_as_text():
    global term_output_policy
    if term_output_policy == "1":
        return "\t2) Term Output Policy:\t\tonly found terms"
    elif term_output_policy == "2":
        return "\t2) Term Output Policy:\t\tonly not found terms"
    else:
        return "\t2) Term Output Policy:\t\tall terms"


def set_term_output_policy(top):
    global term_output_policy
    term_output_policy = top
    update_system_data()


def get_one_line_output():
    global one_line_output
    return True if one_line_output == "1" else False


def get_one_line_output_as_text():
    global one_line_output
    if one_line_output == "1":
        return "\t3) Output Format:\t\tone-line"
    else:
        return "\t3) Output Format:\t\tmulti-line"


def set_one_line_output(onel):
    global one_line_output
    one_line_output = "1" if onel else "0"
    update_system_data()


def get_headline_printing():
    global headline_printing
    return int(headline_printing)


def get_headline_printing_as_text():
    global headline_printing
    if headline_printing == "1":
        return "\t4) Headline Printing:\t\tonly at top of excel"
    elif headline_printing == "2":
        return "\t4) Headline Printing:\t\tfor every new document scanned in"
    else:
        return "\t4) Headline Printing:\t\tfor every new term printed"


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


def get_alphabetical_output_as_text():
    abc, asc = get_alphabetical_output()

    if abc and asc:
        return "\t5) Alphabetical Output:\t\talphabetical, ascending"
    elif abc and not asc:
        return "\t5) Alphabetical Output:\t\talphabetical, descending"
    else:
        return "\t5) Alphabetical Output:\t\tnon-alphabetical"


def set_alphabetical_output(abc, asc):
    global alphabetical_output
    alphabetical_output[0] = "abc=1" if abc else "abc=0"
    alphabetical_output[1] = "asc=1" if asc else "asc=0"
    update_system_data()


def get_auto_scan_filters():
    global auto_scan_filters
    return auto_scan_filters


def get_auto_scan_filters_as_text():
    global auto_scan_filters

    if auto_scan_filters == "Noun":
        return "\t6) Auto Scan PoS Filters:\tnouns only"
    elif auto_scan_filters == "Verb":
        return "\t6) Auto Scan PoS Filters:\tverbs only"
    elif auto_scan_filters == "Adjective":
        return "\t6) Auto Scan PoS Filters:\tadjectives only"
    elif auto_scan_filters == "Adverb":
        return "\t6) Auto Scan PoS Filters:\tadverbs only"
    elif auto_scan_filters == "Preposition":
        return "\t6) Auto Scan PoS Filters:\tprepositions only"
    elif auto_scan_filters == "Phrase":
        return "\t6) Auto Scan PoS Filters:\tphrases only"
    elif auto_scan_filters == "Noun, Verb, Adjective, Adverb, Preposition, Phrase":
        return "\t6) Auto Scan PoS Filters:\tall pos types, no restrictions"
    else:
        return "\t6) Auto Scan PoS Filters:\t" + str(auto_scan_filters)


def set_auto_scan_filters(asf):
    global auto_scan_filters
    auto_scan_filters = asf
    update_system_data()


def get_output_detail_level():
    global output_detail_level
    return int(output_detail_level)


def get_output_detail_level_as_text():
    global output_detail_level

    if output_detail_level == "1":
        return "\t7) Output Detail Level:\t\tlevel 1, term data"
    elif output_detail_level == "2":
        return "\t7) Output Detail Level:\t\tlevel 2, morph data"
    else:
        return "\t7) Output Detail Level:\t\tlevel 3, all data"


def set_output_detail_level(odlvl):
    global output_detail_level
    output_detail_level = odlvl
    update_system_data()


def get_system_sound_level():
    global system_sound_level
    return int(system_sound_level)


def get_system_sound_level_as_text():
    global system_sound_level
    if system_sound_level == "1":
        return "\t8) System Sound Level:\t\tlevel 1, no sounds"
    elif system_sound_level == "2":
        return "\t8) System Sound Level:\t\tlevel 2, notifications only"
    else:
        return "\t8) System Sound Level:\t\tlevel 3, all sounds"


def set_system_sound_level(ssl):
    global system_sound_level
    system_sound_level = ssl
    update_system_data()


def get_request_error():
    global request_error
    return int(request_error)


def set_request_error(error_code):
    global request_error
    request_error = str(error_code)
    update_system_data()
