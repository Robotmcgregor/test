#!/usr/bin/env python


"""
Copyright 2021 Robert McGregor

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import modules
from __future__ import print_function, division
import pandas as pd
import warnings
import numpy as np

warnings.filterwarnings("ignore")


def extract_botanical_fn(row, string_clean_capital_fn, n):
    """ Extract woody thickening information for the five transects within each site.

             :param row: pandas dataframe row value object.
             :param string_clean_capital_fn: function to clean string objects returning capitalized format.
             :param n: string object passed into the function (i.e str(TS), str(SB)).
             :return list_botanical: list object containing the five botanical names for the input species form.
             within each site."""

    list_botanical = []

    for i in range(10):

        botanical = string_clean_capital_fn(str(row[n + '_SP:' + n + str(i + 1)]))
        if botanical == 'Other1':
            final_botanical = string_clean_capital_fn(str(row[n + '_SP:' + n + '_OTHER1']))
        elif botanical == 'Other2':
            fina_botanical = string_clean_capital_fn(str(row[n + '_SP:' + n + '_OTHER2']))
        elif botanical == 'Other3':
            fina_botanical = string_clean_capital_fn(str(row[n + '_SP:' + n + '_OTHER3']))
        elif botanical == 'Other4':
            final_botanical = string_clean_capital_fn(str(row[n + '_SP:' + n + '_OTHER4']))
        elif botanical == 'Other5':
            final_botanical = string_clean_capital_fn(str(row[n + '_SP:' + n + '_OTHER5']))
        else:
            final_botanical = botanical
        list_botanical.append(final_botanical)

    return list_botanical


def species_extraction_fn(row, string_clean_capital_fn, n):
    """ Extract the botanical names and cover fraction values.

            :param row: pandas dataframe row value object.
            :param n: string object containing the species form code(i.e. 'PG' or 'AG').
            :return botanical_name_list: list object containing 10 botanical names variables.
            :return final_cover_list: list object containing 10 float variables (None -> 9999.0)."""

    botanical_name_list = []
    cover_list = []
    for i in range(10):
        botanical_name = string_clean_capital_fn(str(row[n + '_SP:' + n + str(i + 1) + '_NAME']))
        botanical_name_list.append(botanical_name)

        cover = float(row[n + '_COVER:' + n + '_SP' + str(i + 1) + '_COVER'])
        cover_list.append(cover)

    # convert Nan values to 9999.0 in the cover list
    final_cover_list = [9999.0 if x != x else x for x in cover_list]

    return botanical_name_list, final_cover_list


def botanical_extraction_fn(string_clean_capitalize_fn, match_list, input_name_list, input_cover_list):
    """ Sorts contents of a list into two lists based on matches from a list of variables (cleaned3p_list).

            :param string_clean_capitalize_fn: remove whitespaces and clean strings (dirty_string -> clean_string)
            :param match_list: list object of variables used to match against variables in the input list
            (i.e. input_name_list).
            :param input_name_list: list object containing n botanical names variables (species_extraction_fn)
            :param input_cover_list: list object containing n float variables (None -> 9999.0) (species_extraction_fn).
            :return list_botanical_match: list object of the same size as the input list (n) after
            match (variable -> variable) or no match (variable -> str(Nan)) has been determined.
            :return list_botanical_no_match: list object of the same size as the input list (n) after
            match (variable -> variable) or no match (variable -> str(Nan)) has been determined.
            :return list_cover_match: list object of the same size as the input list (n) after
            match (variable -> variable) or no match (variable -> float(9999.0) has been determined.
            :return list_cover_no_match:list object of the same size as the input list (n) after
            match (variable -> variable) or no match (variable -> float(9999.0) has been determined."""

    list_botanical_match = []
    list_botanical_no_match = []
    list_cover_match = []
    list_cover_no_match = []

    # sort the two lists based on the cover values
    for name, cover in zip(input_name_list, input_cover_list):

        # clean the species name
        clean_name = string_clean_capitalize_fn(name)

        # insert if else statement regarding Whitegrass !!!!!!!!!!#todo whitegrass statement

        if any(clean_name in x for x in match_list):
            # print('Yes')
            list_botanical_match.append(clean_name)
            list_cover_match.append(cover)
            list_botanical_no_match.append('Nan')
            list_cover_no_match.append(9999.0)

        else:
            # print('false')
            list_botanical_no_match.append(clean_name)
            list_cover_no_match.append(cover)
            list_botanical_match.append('Nan')
            list_cover_match.append(9999.0)
    # print(list_botanical_match, list_botanical_no_match, list_cover_match, list_cover_no_match)
    return list_botanical_match, list_botanical_no_match, list_cover_match, list_cover_no_match


def sort_two_lists(species_list, cover_list):
    """ sort the two lists based on cover values and convert 9999.0 back to np.nan

            :param species_list: list object containing species names.
            :param cover_list: list object containing species cover values.
                Species and cover vales correspond to list order.
            :return list_cover_sorted_nan: list object (species_list_fn) that has been sorted in ascending order based on
            count values.
            :return list_species_sorted: list object (cover_list) that has been sorted in ascending order with
            injected values (9999.0 converted to np.nan."""

    # zip species_list_fn with count and sort both lists based on count
    tuple_cover_sorted, tuple_species_sorted = zip(*sorted(zip(cover_list, species_list)))

    # convert tuple to list
    list_cover_sorted = list(tuple_cover_sorted)
    list_species_sorted = list(tuple_species_sorted)

    # convert 9999.0 back to np.nan values
    list_cover_sorted_nan = [np.nan if i == 9999.0 else i for i in list_cover_sorted]

    return list_cover_sorted_nan, list_species_sorted


def main_routine(clean_list, row, string_clean_capital_fn, veg_list_excel):
    """ Extract and clean botanical values and botanical count values from the star transect odk raw output.

            :param veg_list_excel: string object containing the path to an excel document containing the botanical and
                common names of vegetation species.
            :type string_clean_capital_fn: function created step2_1_star_transect_processing_workflow.py - used to
                clean and return capitalize case string variables.
            :param clean_list: list object created under step2_1_star_transect_processing_workflow.py - new variables
                are extended or appended to the end.
            :param row: pandas dataframe row value object.
            :return clean_list: list object with additional variables extended or appended to the end.
            :return veg_list: list object containing extended variable to separate forms into annual and perennial"""

    print('starTransectCleanPgBotanical3P.py INITIATED.')

    # ----------------------------------------------------------------------------------------------------------------
    # read in 3p grass species excel
    # import the 3p list from the final species excel replace all nan values with 'BLANK'
    ppp = pd.read_excel(veg_list_excel, sheet_name='PPP_COMP', header=None).fillna('BLANK').replace('Nan', 'BLANK')

    # convert column 4 of the worksheet to a list
    ppp_list = ppp[3].tolist()

    # remove all 'BLANK values from list
    cleaned3p_list = [x for x in ppp_list if str(x) != 'BLANK']

    # ---------------------------------------------------------------------------------------------------------------
    # read in and annual forb species excel
    # import the annual forb list from the final species excel replace all nan values with 'BLANK'
    forb = pd.read_excel(veg_list_excel, sheet_name='ANNUAL_FORB_COMP', header=None).fillna('BLANK').replace('Nan',
                                                                                                             'BLANK')
    # convert to list
    af_list = forb[5].tolist()

    # remove all 'BLANK values from list
    cleaned_af_list = [x for x in af_list if str(x) != 'BLANK']

    # ----------------------------------------------------------------------------------------------------------------
    # perennial and 3p grass processing and sorting

    botanical_name_list, cover_list = species_extraction_fn(row, string_clean_capital_fn, 'PG')

    # call the botanicalPG function
    list_botanical3p, list_botanical_pg, list3p_cover, list_pg_cover = botanical_extraction_fn(
        string_clean_capital_fn, cleaned3p_list, botanical_name_list, cover_list)

    list3p_cover_sorted_nan, list3p_species_sorted = sort_two_lists(list_botanical3p, list3p_cover)
    print(list3p_cover_sorted_nan, list3p_species_sorted)

    list_pg_cover_sorted_nan, list_pg_species_sorted = sort_two_lists(list_botanical_pg, list_pg_cover)
    print(list_pg_cover_sorted_nan, list_pg_species_sorted)

    # append all values to the cleaned values to the list (clean_list)
    clean_list.extend(list3p_species_sorted)
    clean_list.extend(list3p_cover_sorted_nan)
    clean_list.extend(list_pg_species_sorted)
    clean_list.extend(list_pg_cover_sorted_nan)

    # ---------------------------------------------------------------------------------------------------------------
    # annual grass processing

    # extract botanical names and cover values.
    botanical_name_list, cover_list = species_extraction_fn(row, string_clean_capital_fn, 'AG')
    list_cover_sorted_nan = [np.nan if i == 9999.0 else i for i in cover_list]

    # append all values to the cleaned values to the list (clean_list)
    clean_list.extend(botanical_name_list)
    clean_list.extend(list_cover_sorted_nan)

    # ---------------------------------------------------------------------------------------------------------------
    # forb extraction and sort

    # extract botanical names and cover values.
    botanical_name_list, cover_list = species_extraction_fn(row, string_clean_capital_fn, 'F')

    # call the botanicalPG function
    list_botanical_af, list_botanical_pf, list_af_cover, list_pf_cover = botanical_extraction_fn(
        string_clean_capital_fn, cleaned_af_list, botanical_name_list, cover_list)

    list_af_cover_sorted_nan, list_af_species_sorted = sort_two_lists(list_botanical_af, list_af_cover)
    print(list_af_cover_sorted_nan, list_af_species_sorted)

    list_pf_cover_sorted_nan, list_pf_species_sorted = sort_two_lists(list_botanical_pf, list_pf_cover)
    print(list_pf_cover_sorted_nan, list_pf_species_sorted)

    # append all values to the cleaned values to the list (clean_list)
    clean_list.extend(list_pf_species_sorted)
    clean_list.extend(list_pf_cover_sorted_nan)
    clean_list.extend(list_af_species_sorted)
    clean_list.extend(list_af_cover_sorted_nan)

    print(list_af_cover_sorted_nan)

    veg_list = []
    print('list_af_cover_sorted_nan count np.nan: ', list_af_cover_sorted_nan.count(np.nan))
    print('list_af_cover_sorted_nan count: None', list_af_cover_sorted_nan.count(None))

    represent_veg = str(
        row['SITE_VEG_FRACTIONS:VEG_COVER_ADJUST'])  # TODO check that the values are correct as no representative data
    if list_af_cover_sorted_nan.count(np.nan) > 0 and represent_veg == 'representative':
        print('list_af_cover_sorted_nan: NOT Empty line 161')
        while np.nan in list_af_cover_sorted_nan:
            list_af_cover_sorted_nan.remove(np.nan)

        print(list_af_cover_sorted_nan)

        total = float(0.0)

        # Iterate each element in list
        # and add them in variable total
        for ele in range(0, len(list_af_cover_sorted_nan)):
            total = total + list_af_cover_sorted_nan[ele]

        represent_veg = str(row['SITE_VEG_FRACTIONS:VEG_COVER_ADJUST'])
        print('represent_veg: ', represent_veg)

        rep_veg = 'amended - annual forb'

        adj_perennial = float(row['PG_SUM_PROP'])
        adj_annual = float(row['AG_SUM_PROP'])
        adj_p_forb = (float(row['F_SUM_PROP']) - float(total))
        field_a_forb = float(0.0)
        adj_a_forb = float(total)
        final_a_forb = float(total)
        adj_veg_total = float(row['SITE_COVER_FRACTIONS:TOTAL_COVER'])
        final_veg_total = float(row['SITE_COVER_FRACTIONS:TOTAL_COVER'])

        veg_list = [rep_veg, adj_perennial, adj_perennial, adj_annual, adj_p_forb, field_a_forb, adj_a_forb,
                    final_a_forb, adj_veg_total, final_veg_total]

        """veg_list = [rep_veg, adj_perennial, adj_perennial, adj_annual, adj_p_forb, adj_a_forb, adj_veg_total, 
                    final_veg_total]"""
        # todo why is this list shorter than th else statement?

    else:
        print('list_af_cover_sorted_nan: EMPTY')
        total = float(0.0)
        rep_veg = str(row['SITE_VEG_FRACTIONS:VEG_COVER_ADJUST'])

        adj_perennial = float(row['SITE_VEG_FRACTIONS:PG_TOTAL_ADJUSTED'])
        adj_annual = float(row['SITE_VEG_FRACTIONS:AG_TOTAL_ADJUSTED'])
        adj_p_forb = float(row['SITE_VEG_FRACTIONS:F_TOTAL_ADJUSTED']) - float(total)
        field_a_forb = float(0.0)
        adj_a_forb = float(0.0)
        final_a_forb = float(0.0)
        adj_veg_total = float(row['SITE_VEG_FRACTIONS:VEG_ADJ'])
        final_veg_total = float(row['SITE_VEG_FRACTIONS:VEG_ADJ'])

        veg_list = [rep_veg, adj_perennial, adj_perennial, adj_annual, adj_p_forb, field_a_forb, adj_a_forb,
                    final_a_forb, adj_veg_total, final_veg_total]

    print('step2_3_star_transect_botanical.py COMPLETED')
    print('step_2_4_starTransectCleanAgBotanicalP.py initiating...........')

    return clean_list, veg_list


if __name__ == '__main__':
    main_routine()
