from openpyxl.styles import Font, Color


def print_headlines(worksheet, excel_row, output_detail_level):

    blue_color = "0000FF"
    brown_color = "6E2C00"

    term_Hcell = 'A' + str(excel_row)
    filter_Hcell = 'B' + str(excel_row)
    pos_Hcell = 'C' + str(excel_row)
    syll_Hcell = 'D' + str(excel_row)
    def_Hcell = 'E' + str(excel_row)
    worksheet[term_Hcell] = 'Term'
    worksheet[filter_Hcell] = 'Filter'
    worksheet[pos_Hcell] = 'PoS'
    worksheet[syll_Hcell] = 'Syllables'
    worksheet[def_Hcell] = 'Definition'
    worksheet[term_Hcell].font = Font(bold=True)
    worksheet[filter_Hcell].font = Font(bold=True)
    worksheet[pos_Hcell].font = Font(bold=True)
    worksheet[syll_Hcell].font = Font(bold=True)
    worksheet[def_Hcell].font = Font(bold=True)

    if output_detail_level >= 2:
        affix_Hcell = 'F' + str(excel_row)
        lang_Hcell = 'G' + str(excel_row)
        sub_pos_Hcell = 'H' + str(excel_row)
        mean_Hcell = 'I' + str(excel_row)
        worksheet[affix_Hcell] = 'Affix'
        worksheet[lang_Hcell] = 'Language'
        worksheet[sub_pos_Hcell] = 'PoS'
        worksheet[mean_Hcell] = 'Meaning'
        worksheet[affix_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
        worksheet[lang_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
        worksheet[sub_pos_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))
        worksheet[mean_Hcell].font = Font(bold=True, color=Color(rgb=blue_color))

    if output_detail_level == 3:
        sub_affix_Hcell = 'J' + str(excel_row)
        sub_lang_Hcell = 'K' + str(excel_row)
        decoded_Hcell = 'L' + str(excel_row)
        sub_sub_pos_Hcell = 'M' + str(excel_row)
        sub_meaning_Hcell = 'N' + str(excel_row)
        worksheet[sub_affix_Hcell] = 'Affix'
        worksheet[sub_lang_Hcell] = 'Language'
        worksheet[decoded_Hcell] = 'Decoded'
        worksheet[sub_sub_pos_Hcell] = 'PoS'
        worksheet[sub_meaning_Hcell] = 'Meanings'
        worksheet[sub_affix_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))
        worksheet[sub_lang_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))
        worksheet[decoded_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))
        worksheet[sub_sub_pos_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))
        worksheet[sub_meaning_Hcell].font = Font(bold=True, color=Color(rgb=brown_color))

    excel_row += 1
    return worksheet, excel_row


def search_and_output(worksheet, excel_row, pos_filters, term, entries_list,
                      only_found_terms, only_not_found_terms, multiline_output, output_detail_level,
                      headline_printing, hdlp_start, hdlp_doc):

    pos_filters = pos_filters.split(", ")

    # Set the color for blue entries
    blue_color = "0000FF"
    blue_font = Font(color=Color(rgb=blue_color))

    # Set the color for brown entries
    brown_color = "6E2C00"
    brown_font = Font(color=Color(rgb=brown_color))

    # -----------------------------------------------------------------------------
    # PREPARING: functions for printing the values
    # useful to not repeat every cell definition before setting the values
    def set_level_1_cell_data(current_excel_row, pos, syllables, definition):
        pos_cell = "C" + str(current_excel_row)
        syll_cell = "D" + str(current_excel_row)
        def_cell = "E" + str(current_excel_row)

        worksheet[pos_cell] = str(pos)
        worksheet[syll_cell] = str(syllables)
        worksheet[def_cell] = str(definition)

    def set_level_2_cell_data(current_excel_row, affix, language, sub_pos, meaning):

        affix_cell = "F" + str(current_excel_row)
        lang_cell = "G" + str(current_excel_row)
        pos_cell = "H" + str(current_excel_row)
        mean_cell = "I" + str(current_excel_row)

        worksheet[affix_cell].font = blue_font
        worksheet[lang_cell].font = blue_font
        worksheet[pos_cell].font = blue_font
        worksheet[mean_cell].font = blue_font

        worksheet[affix_cell] = str(affix)
        worksheet[lang_cell] = str(language)
        worksheet[pos_cell] = str(sub_pos)
        worksheet[mean_cell] = str(meaning)

    def set_level_3_cell_data(current_excel_row, sub_affix, sub_language, decoded, sub_sub_pos, sub_meaning):

        sub_affix_cell = "J" + str(current_excel_row)
        sub_language_cell = "K" + str(current_excel_row)
        decoded_cell = "L" + str(current_excel_row)
        sub_sub_pos_cell = "M" + str(current_excel_row)
        sub_meaning_cell = "N" + str(current_excel_row)

        worksheet[sub_affix_cell].font = brown_font
        worksheet[sub_language_cell].font = brown_font
        worksheet[decoded_cell].font = brown_font
        worksheet[sub_sub_pos_cell].font = brown_font
        worksheet[sub_meaning_cell].font = brown_font

        worksheet[sub_affix_cell] = str(sub_affix)
        worksheet[sub_language_cell] = str(sub_language)
        worksheet[decoded_cell] = str(decoded)
        worksheet[sub_sub_pos_cell] = str(sub_sub_pos)
        worksheet[sub_meaning_cell] = str(sub_meaning)

    # ----------------------------------------------------------------------------------------------
    # PREPARING: term print and search function
    # only desired terms will be printed (depends on chosen 3 way output option as you can see below)
    def print_term(ER, FE, POS):

        output = ""

        # printing term
        term_cell = "A" + str(ER)
        worksheet[term_cell] = term

        # printing pos filter
        filter_cell = "B" + str(ER)
        if len(POS) == 6:
            worksheet[filter_cell] = "NONE"
        else:
            pos_string = ""                                     # converts list eg. (noun,verb,adjective)
            for z in range(1, len(POS)):                        # into string like "noun, verb, adjective"
                pos_string += str(POS[z])
                if not z == len(POS) - 1:
                    pos_string += ", "
            worksheet[filter_cell] = pos_string

        for x in range(len(FE)):

            entry = FE[x]
            multiline_at_level2_already_executed = False

            keys = list(entry.keys())

            # Data Structure Level 1 ---------------------------------------------------------------------

            pos_value = entry[keys[1]]
            syllables_value = entry[keys[2]]
            definition_value = entry[keys[3]]
            morphemes_value = entry[keys[4]]

            set_level_1_cell_data(
                ER, pos_value, syllables_value, definition_value)

            output += "\n\t" + str(num_found_entries) + ")" + \
                      "\t" + str(keys[1]) + ": " + str(pos_value) + "\n" + \
                      "\t\t" + str(keys[2]) + ": " + str(syllables_value) + "\n" + \
                      "\t\t" + str(keys[3]) + ": " + str(definition_value) + "\n" + \
                      "\t\t" + str(keys[4]) + ": " + str(morphemes_value) + "\n"

            # Data Structure Level 2 ---------------------------------------------------------------------

            if output_detail_level >= 2:

                if morphemes_value is None:
                    set_level_2_cell_data(ER, affix="N/V", language="N/V", sub_pos="N/V", meaning="N/V")
                    ER += 1

                else:
                    for respective_morph_dict in morphemes_value:

                        if multiline_output and not multiline_at_level2_already_executed:
                            ER += 1
                            multiline_at_level2_already_executed = True

                        morphemes_sub_values = list(respective_morph_dict.values())

                        affix_value = morphemes_sub_values[0]
                        language_value = morphemes_sub_values[1]
                        sub_pos_value = morphemes_sub_values[2]
                        meaning_value = morphemes_sub_values[3]
                        etcom_value = morphemes_sub_values[4]

                        set_level_2_cell_data(
                            ER, affix_value, language_value, sub_pos_value, meaning_value)

                        # Data Structure Level 3 -------------------------------------------------------------
                        if output_detail_level == 3:

                            if multiline_output:
                                ER += 1

                            if etcom_value is None:
                                set_level_3_cell_data(ER, sub_affix="N/V", sub_language="N/V", decoded="N/V",
                                                      sub_sub_pos="N/V", sub_meaning="N/V")
                                ER += 1

                            else:

                                sub_affix_values = []
                                sub_language_values = []
                                decoded_values = []
                                sub_sub_pos_values = []
                                sub_meaning_values = []

                                for respective_etcom_dict in etcom_value:
                                    etcom_sub_values = list(respective_etcom_dict.values())

                                    sub_affix_value = etcom_sub_values[0]
                                    sub_language_value = etcom_sub_values[1]
                                    decoded_value = etcom_sub_values[2]
                                    sub_sub_pos_value = etcom_sub_values[3]
                                    sub_meaning_value = etcom_sub_values[4]

                                    sub_affix_values.append(sub_affix_value)
                                    sub_language_values.append(sub_language_value)
                                    decoded_values.append(decoded_value)
                                    sub_sub_pos_values.append(sub_sub_pos_value)
                                    sub_meaning_values.append(sub_meaning_value)

                                # the lists with all collected information are prepared now
                                # next step is to filter out redundant (duplicate) information over all
                                # five information types. so we connect them in a single list:

                                hyper_list = []
                                for v in range(len(sub_affix_values)):
                                    value = str(sub_affix_values[v]) + "[/]"
                                    value += str(sub_language_values[v]) + "[/]"
                                    value += str(decoded_values[v]) + "[/]"
                                    value += str(sub_sub_pos_values[v]) + "[/]"
                                    value += str(sub_meaning_values[v])
                                    hyper_list.append(value)

                                # eliminating duplicates and sorting alphabetical ascending
                                hyper_list = list(set(hyper_list))
                                hyper_list = sorted(hyper_list)

                                # transforming back to separated lists
                                cleaned_sub_affix_values = []
                                cleaned_sub_language_values = []
                                cleaned_decoded_values = []
                                cleaned_sub_sub_pos_values = []
                                cleaned_sub_meaning_values = []

                                for x in range(len(hyper_list)):
                                    values = hyper_list[x].split("[/]")
                                    cleaned_sub_affix_values.append(values[0])
                                    cleaned_sub_language_values.append(values[1])
                                    cleaned_decoded_values.append(values[2])
                                    cleaned_sub_sub_pos_values.append(values[3])
                                    cleaned_sub_meaning_values.append(values[4])

                                for x in range(len(cleaned_sub_affix_values)):

                                    set_level_3_cell_data(
                                        ER, cleaned_sub_affix_values[x], cleaned_sub_language_values[x],
                                        cleaned_decoded_values[x], cleaned_sub_sub_pos_values[x],
                                        cleaned_sub_meaning_values[x])

                                    ER += 1
                        else:
                            ER += 1
            else:
                ER += 1

        return ER

    # ------------------------------------------------------------------------------------
    # TERM PRINT CONTROL and HEADLINE PRINTING MANAGEMENT
    # in dependency of chosen 3 way output option

    num_found_entries = 0
    found_entries = []

    # gather all entries that match with search term and pos filters
    # creates a restricted entry list (found_entries) that will be used for term printing
    for x in range(len(entries_list)):
        entry = entries_list[x]
        if entry["Word"] == term and entry["PoS"] in pos_filters:
            num_found_entries += 1
            found_entries.append(entry)

    # if entries are found and according to tod=1 or tod=3 they shall be printed:
    if num_found_entries != 0 and not only_not_found_terms:
        if headline_printing == 3:                          # if headline for every term ordered
            if not hdlp_start and not hdlp_doc:             # and if no headline came directly before
                worksheet, excel_row = print_headlines(worksheet, excel_row, output_detail_level)
            else:
                hdlp_start = False
                hdlp_doc = False
        excel_row = print_term(ER=excel_row, FE=found_entries, POS=pos_filters)
        if headline_printing == 2:                          # (first) term is printed now, so if headline for every doc:
            hdlp_doc = False                                # unlocking again headline for documents

    # if no entries found and according to tod=2 or tod=3 they shall be printed:
    elif num_found_entries == 0 and not only_found_terms:
        if headline_printing == 3:                          # if headline for every term ordered
            if not hdlp_start and not hdlp_doc:             # and if no headline came directly before
                worksheet, excel_row = print_headlines(worksheet, excel_row, output_detail_level)
            else:
                hdlp_start = False
                hdlp_doc = False
        excel_row = print_term(ER=excel_row, FE=found_entries, POS=pos_filters)
        if headline_printing == 2:                          # (first) term is printed now, so if headline for every doc:
            hdlp_doc = False                                # unlocking again headline for documents

    log_output = "\t------------------------------------------------------------\n\n\tWord: " + term
    final_output = "\t------------------------------------------------------------\n\n\tWord: " + term
    output = ""
    pos_output = ""

    # check
    if num_found_entries == 0 and len(pos_filters) == 6:
        final_output += "\n\tWarning: database has no entry for '" + term + "'."
        log_output += "\n\tWarning: no entry for '" + term + "'."

        if not only_found_terms:
            set_level_1_cell_data(excel_row, pos="N/V", syllables="N/V", definition="N/V")
            if output_detail_level >= 2:
                if multiline_output:
                    excel_row += 1
                set_level_2_cell_data(excel_row, affix="N/V", language="N/V", sub_pos="N/V", meaning="N/V")
            if output_detail_level == 3:
                if multiline_output:
                    excel_row += 1
                set_level_3_cell_data(excel_row, sub_affix="N/V", sub_language="N/V", decoded="N/V",
                                      sub_sub_pos="N/V", sub_meaning="N/V")
            excel_row += 1

    elif num_found_entries == 0 and len(pos_filters) != 6:

        for x in range(len(pos_filters)):
            if x != len(pos_filters) - 1:
                pos_output += pos_filters[x] + ", "
            else:
                pos_output += pos_filters[x]

        final_output += "\n\tWarning: no results found for '" + term + "' with filters '" + \
                        pos_output + "'. \n\tYou can try to extend the filtering."
        log_output += "\n\tWarning: no results for '" + term + "' with filters '" + \
                      pos_output + "'."

        if not only_found_terms:
            set_level_1_cell_data(excel_row, pos="N/V", syllables="N/V", definition="N/V")
            if output_detail_level >= 2:
                set_level_2_cell_data(excel_row, affix="N/V", language="N/V", sub_pos="N/V", meaning="N/V")
            if output_detail_level == 3:
                set_level_3_cell_data(excel_row, sub_affix="N/V", sub_language="N/V", decoded="N/V",
                                      sub_sub_pos="N/V", sub_meaning="N/V")
            excel_row += 1

    else:
        if len(pos_filters) == 6:
            log_output += "\n\tFilters: NONE" + \
                          "\n\tEntries found: " + str(num_found_entries) + "\n"

            final_output += "\n\tFilters: NONE" + \
                            "\n\tEntries found: " + str(num_found_entries) + "\n"
        else:
            for x in range(len(pos_filters)):
                if x != len(pos_filters) - 1:
                    pos_output += " " + pos_filters[x] + ","
                else:
                    pos_output += " " + pos_filters[x]

            log_output += "\n\tFilters:" + str(pos_output) + \
                          "\n\tEntries found: " + str(num_found_entries) + "\n"

            final_output += "\n\tFilters:" + str(pos_output) + \
                            "\n\tEntries found: " + str(num_found_entries) + "\n"
        final_output += output

    return worksheet, excel_row, log_output, hdlp_start, hdlp_doc