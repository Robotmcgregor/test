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
import warnings

warnings.filterwarnings("ignore")


def paddock_fn(row, string_clean_capital_fn):
    """ Extract the paddock name description and reason for site selection information.

            :param row: pandas dataframe row value object.
            :param string_clean_capital_fn: function to remove whitespaces and clean strings.
            :return: establish_list: list object containing three variables: paddock, desc and reason."""

    paddock = str(row['GROUP_SITE_DESC:PADDOCK_NAME'])
    # clean variable
    paddock = string_clean_capital_fn(paddock)

    desc = str(row['GROUP_SITE_DESC:SITE_DESC'])
    if desc == 'other':
        desc = str(row['GROUP_SITE_DESC:SITE_DESC_OTHER'])
    else:
        desc = str(row['GROUP_SITE_DESC:SITE_DESC'])
    # clean variable
    desc = string_clean_capital_fn(desc)

    reason = str(row['GROUP_SITE_DESC:REASON_SITE'])
    # clean variable
    reason = string_clean_capital_fn(reason)

    establish_list = [paddock, desc, reason]

    return establish_list


def landscape_fn(row, string_clean_capitalize_fn):
    """ Extract the landscape information.

            :param row: pandas dataframe row value object.
            :param string_clean_capitalize_fn: function to remove whitespaces and clean strings.
            :return: landscape_list: list object containing two variables: landscape and soil_colour."""

    landscape = str(row['SITE_ESTABLISHMENT:GROUP_SOIL:LANDSCAPE_POS'])
    landscape = string_clean_capitalize_fn(landscape)

    soil_colour = str(row['SITE_ESTABLISHMENT:GROUP_SOIL:SOIL_COLOR'])
    soil_colour = string_clean_capitalize_fn(soil_colour)

    landscape_list = [landscape, soil_colour]
    return landscape_list


def land_system_fn(row, string_clean_capital_fn):
    """ Extract land system information.

            :param row: pandas dataframe row value object.
            :param string_clean_capital_fn: function to remove whitespaces and clean strings.
            :return: land_system_list: list object containing four variables:
                land_system, ls_consistent, land_system_alt, ls_source."""

    ls_consistent = str(row['SITE_ESTABLISHMENT:GROUP_LS:LAND_SYS_CONSIST'])
    land_system = string_clean_capital_fn(str(row['SITE_ESTABLISHMENT:GROUP_LAND_SYSTEM:LAND_SYSTEM1']))
    land_system_alt = string_clean_capital_fn(str(row['SITE_ESTABLISHMENT:ALT_LAND_SYS']))

    if ls_consistent == 'ls_no':
        ls_source = string_clean_capital_fn(str(row['SITE_ESTABLISHMENT:GROUP_ALT_LS:ALT_LS_SOURCE']))

    elif ls_consistent == 'ls_yes':
        ls_consistent = 'Yes'
        ls_source = string_clean_capital_fn(str(row['SITE_ESTABLISHMENT:GROUP_LS:LS_SOURCE']))

    else:
        ls_consistent = 'Not assessed'
        ls_source = string_clean_capital_fn(str(row['SITE_ESTABLISHMENT:GROUP_LS:LS_SOURCE']))

    land_system_list = [land_system, ls_consistent, land_system_alt, ls_source]
    return land_system_list


def water_point_fn(row, string_clean_capital_fn, string_clean_title_fn):
    """ Extract water point information.

            :param row: pandas dataframe row value object.
            :param string_clean_capital_fn: function to remove whitespaces and clean strings.
            :param string_clean_title_fn: function to remove whitespaces and clean strings.
            :return: water_point_list: list object containing four variables:
                water_point, water_point_name, water_dir and water_distance."""

    water_point = string_clean_capital_fn(str(row['GROUP_WATER:WATER_FINAL']))

    water_point_name = string_clean_title_fn(str(row['GROUP_WATER:GROUP_WATER_DIST:NEAR_WATER_NAME']))

    water_dir = string_clean_capital_fn(str(row['GROUP_WATER:GROUP_WATER_DIST:DIRECTION_WATER']))
    water_distance = float(row['GROUP_WATER:GROUP_WATER_DIST:DIST_NEAR_WATER'])

    water_point_list = [water_point, water_point_name, water_dir, water_distance]
    return water_point_list


def estab_track_fn(row, string_clean_capitalize_fn):
    """ Extract establishment track information.

            :param row: pandas dataframe row value object.
            :param string_clean_capitalize_fn: function to remove whitespaces and clean strings.
            :return: water_point_list: list object containing three variables:
                estab_track, estab_track_dist, estab_track_dir."""

    estab_track = string_clean_capitalize_fn(str(row['SITE_ESTABLISHMENT:ESTAB_GROUP_TRACK:DIST_TRACK']))
    estab_track_dist = float(row['SITE_ESTABLISHMENT:ESTAB_GROUP_TRACK:DIST_TRACK'])
    estab_track_dir = string_clean_capitalize_fn(str(row['SITE_ESTABLISHMENT:ESTAB_GROUP_TRACK:DIRECTION_TRACK']))

    estab_track_list = [estab_track, estab_track_dist, estab_track_dir]

    return estab_track_list


def estab_other_infra_fn(row, string_clean_capitalize_fn):
    """ Extract the establishment infrastructure information.

            :param row: pandas dataframe row value object.
            :param string_clean_capitalize_fn: function to remove whitespaces and clean strings.
            :return: water_point_list: list object containing two variables:
                infra_other, infra_other_dist."""

    infra_other = string_clean_capitalize_fn(str(row['SITE_ESTABLISHMENT:ESTAB_GROUP_INFRA:EST_INFRA_FINAL']))

    infra_other_dist = float(row['SITE_ESTABLISHMENT:ESTAB_GROUP_INFRA:GROUP_INFRA_DIST:ESTAB_INFRA_DIST'])

    infrastructure_list = [infra_other, infra_other_dist]

    return infrastructure_list


def revisit_infra_fn(row, string_clean_capital_fn):
    """ Extract the revisit infrastructure information.

            :param row: pandas dataframe row value object.
            :param string_clean_capital_fn: function to remove whitespaces and clean strings.
            :return: water_point_list: list object containing three variables:
                revisit_infra, revisit_infra_dist, revisit_infra_comment."""

    revisit_infra = string_clean_capital_fn(str(row['GROUP_INFRA:INFRA_FINAL']))
    revisit_infra_dist = float(row['GROUP_INFRA:GROUP_OTHER_INFRA_DIST:INFRA_DIST'])
    revisit_infra_comment = string_clean_capital_fn(str(row['GROUP_INFRA:GROUP_OTHER_INFRA_DIST:INFRA_COMMENT']))

    revisit_infra_list = [revisit_infra, revisit_infra_dist, revisit_infra_comment]
    return revisit_infra_list


def revisit_soil_condition(row, string_clean_capitalize_fn):
    """ Extract the soil and atmosphere conditions information.

            :param row: pandas dataframe row value object.
            :param string_clean_capitalize_fn: function to remove whitespaces and clean strings.
            :return: water_point_list: list object containing five variables:
                season_cond, soil_moist, atm_cond, soil_cracks, erodible_soil."""

    season_cond = string_clean_capitalize_fn(str(row['SITE_REVISIT:SEASON_COND']))
    atm_cond = string_clean_capitalize_fn(str(row['SITE_REVISIT:ATM_COND']))
    soil_cracks = string_clean_capitalize_fn(str(row['SOIL_REVISIT:SURF_CRACK']))
    soil_moist = string_clean_capitalize_fn(str(row['SOIL_REVISIT:SOIL_MOIST']))
    erodible_soil = string_clean_capitalize_fn(str(row['SOIL_REVISIT:ERODIBLE_SOIL']))

    revisit_list = [season_cond, soil_moist, atm_cond, soil_cracks, erodible_soil]
    return revisit_list


def main_routine(clean_list, row, string_clean_capital_fn, string_clean_title_fn):
    """Extract site visit and establishment variables from the integrated odk output.

            :param clean_list: ordered list object that contains the processed integrated odk form result
                    variables.
            :param row: pandas dataframe row value object.
            :param string_clean_capital_fn: function that processes string objects (dirty_string -> clean_string)
            :param string_clean_title_fn: function that processes string objects (dirty_string -> clean_string)
            :return: clean_list: ordered list object that contains the processed integrated odk form result
                    variables variables processed within this script extend the list."""

    print('step3_2_integrated_establishment.py INITIATED.')

    # Read in the star transect csv as  a Pandas DataFrame.
    # df = pd.read_csv(integrated_csv)

    # call the site_desc_fn function
    establish_list = paddock_fn(row, string_clean_capital_fn)

    # call the landscape_fn function
    landscape_list = landscape_fn(row, string_clean_capital_fn)
    # print("landscape_fn function complete.")

    # call the land_system_fn function
    land_system_list = land_system_fn(row, string_clean_capital_fn)
    # print("land_system_fn function complete.")

    # call the water_point_fn function
    water_point_list = water_point_fn(row, string_clean_capital_fn, string_clean_title_fn)
    # print("water_point_fn function complete.")

    # call the trackFN function
    estab_track_list = estab_track_fn(row, string_clean_capital_fn)

    # call the estab_other_infra_fn function
    infrastructure_list = estab_other_infra_fn(row, string_clean_capital_fn)

    # call the revisit_infra_fn function
    revisit_infra_list = revisit_infra_fn(row, string_clean_capital_fn)

    # call the revisit_soil_condition function
    revisit_list = revisit_soil_condition(row, string_clean_capital_fn)

    # extend clean_list with the return variables.
    clean_list.extend(establish_list)
    clean_list.extend(landscape_list)
    clean_list.extend(land_system_list)
    clean_list.extend(water_point_list)
    clean_list.extend(estab_track_list)
    clean_list.extend(infrastructure_list)
    clean_list.extend(revisit_infra_list)
    clean_list.extend(revisit_list)

    print('step3_2_integrated_establishment.py COMPLETED')
    print('step3_3_integrated_disturbance.py initiating...........')

    return clean_list


if __name__ == '__main__':
    main_routine()
