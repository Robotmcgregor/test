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
import pandas as pd
import warnings
import numpy as np
from datetime import datetime

warnings.filterwarnings("ignore")


def string_clean_upper_fn(dirty_string):
    """ Remove whitespaces and clean strings.

            :param dirty_string: string object.
            :return clean_string: processed string object. """

    str1 = dirty_string.replace('_', ' ')
    str2 = str1.replace('-', ' ')
    str3 = str2.upper()
    clean_string = str3.strip()
    return clean_string


def string_clean_capital_fn(dirty_string):
    """ Remove whitespaces and clean strings.

            :param dirty_string: string object.
            :return clean_string: processed string object. """

    str1 = dirty_string.replace('_', ' ')
    str2 = str1.replace('-', ' ')
    str3 = str2.capitalize()
    clean_string = str3.strip()
    return clean_string


def string_clean_title_fn(dirty_string):
    """ Remove whitespaces and clean strings.

            :param dirty_string: string object.
            :return clean_string: processed string object. """

    str1 = dirty_string.replace('_', ' ')
    str2 = str1.replace('-', ' ')
    str3 = str2.title()
    clean_string = str3.strip()
    return clean_string

'''
def date_time_fn(df):
    """ Extract and reformat date and time fields. """

    # extract start date and time
    s_date, s_hms = df.s_date[0], df.s_hms[0]

    # convert date
    s_date2 = s_date[-2:] + '/' + s_date[-5:-3] + '/' + s_date[2:4]

    # convert time
    result = s_hms.rsplit(':', 1)
    s_hm = result[0]
    # convert string to time (datetime - hours and minutes)
    dirty_obs_time = datetime.strptime(s_hm, '%H:%M')

    # convert time to 12 hour clock
    obs_time = dirty_obs_time.strftime("%I:%M %p")
    obs_date_time = s_date2 + ' ' + obs_time

    return obs_date_time'''


def pers_absent_fn(input_list):
    """ Convert 0 or values or np.nan values to 'Absent'.
        :param input_list: list object  containing unknown variables.
        :return output_list: list object containing processed variables."""

    output_list = []
    for i in input_list:

        if i == 0 or '0' or np.nan:
            output_value = 'Absent'
        else:
            i = np.nan
        output_list.extend([output_value])
    return output_list


def percentage_fn(input_list):
    """ remove spaces and add a percentage sign.
        :param input_list: list object  containing unknown variables.
        :return output_list: list object containing processed variables."""

    output_list = []
    for i in input_list:
        space_free = str(i).replace(' ', '')
        final_variable = space_free + '%'

        output_list.extend([final_variable])

    return output_list


def pres_abs_to_true_false_fn(input_list):
    """ #Asign true or false to present absent variables.
            :param input_list: list object containing Present/Absent string variables.
            :return output_list: list object containing processed string variables."""
    output_list = []
    for i in input_list:

        if i == 'Present':
            n = 'True'
        else:
            n = 'False'
        output_list.append(n)

    return output_list


def site_hor_list_variable_fn(ras):
    """ Extract rapid assessment survey (ras) sheet variables as a list of lists.

            :param ras: pandas dataframe object.
            :return ras_hort_list1234567891011121314: list object containing information to be inserted into the
            ras sheet horizontally, including site name, water points, basal density feral animals etc. """

    ras_hor_list1 = [ras.final_prop[0], ras.site[0], ras.date_time[0]]
    ras_hor_list2 = [ras.recorder[0], 'BLANK', 'BLANK']
    ras_hor_list3 = [ras.c_lat[0], ras.c_lon[0], 'PADDOCK_not_collected']
    ras_hor_list4 = [ras.water_name[0], ras.water_point[0], ras.water_dist[0], ras.water_dir[0]]
    ras_hor_list5 = [ras.desc[0], ras.land_system[0]]
    ras_hor_list6 = [ras.bare_soil[0]]
    # call the percentage_fn function to remove spaces and add a '%' character.
    ras_hor_list6 = percentage_fn(ras_hor_list6)

    cover_list = [ras.cover_3p[0], ras.cover_pg[0], ras.cover_ag[0], ras.cover_pf[0]]
    # call the percentage_fn function to remove spaces and add a '%' character.
    cover_list = percentage_fn(cover_list)
    basal_list = [ras.basal[0]]
    density_list = [ras.tree_density[0], ras.shrub_density[0]]
    density_list = pers_absent_fn(density_list)
    erodible_soil = [ras.erod_soil[0]]
    pas_ulil_list = ['pasture util - update']
    weeds_comment_list = ['use existing code']
    feral_list = [ras.camel[0], ras.rabbit[0], ras.donkey[0], ras.horse[0], ras.pig[0],
                  ras.buffalo[0], ras.nat_herb[0]]
    final_feral_list = pres_abs_to_true_false_fn(feral_list)
    condition_list = [ras.condition[0], ras.cond_note[0]]

    ras_hort_list1234567891011121314 = [
        ras_hor_list1, ras_hor_list2, ras_hor_list3, ras_hor_list4, ras_hor_list5, ras_hor_list6, cover_list,
        basal_list, density_list, erodible_soil, pas_ulil_list, weeds_comment_list, final_feral_list, condition_list]
    print('ras_hort_list1234567891011121314: ', ras_hort_list1234567891011121314)
    return ras_hort_list1234567891011121314


def site_vert_list_variable_fn(ras):
    """ Extract rapid assessment survey (ras) sheet variables as a list of lists.

            :param ras: pandas dataframe object.
            :return ras_vert_list123456789101112: list object containing information to be inserted into the
            ras sheet vertically, including botanical lists, fire and erosion variables etc. """

    ras_ver_list1 = [ras.bot_3p_1[0], ras.bot_3p_2[0], ras.bot_3p_3[0], ras.bot_3p_4[0]]
    ras_ver_list2 = [ras.bot_pg_1[0], ras.bot_pg_2[0], ras.bot_pg_3[0], ras.bot_pg_4[0]]
    ras_ver_list3 = [ras.bot_ag_1[0], ras.bot_ag_2[0], ras.bot_ag_3[0], ras.bot_ag_4[0]]
    ras_ver_list4 = [ras.bot_pf_1[0], ras.bot_pf_2[0], ras.bot_pf_3[0], ras.bot_pf_4[0]]
    min_max_list = [ras.max_cover[0], ras.min_cover[0]]  # todo get min max values

    # todo tree and shrub species can be 6
    ras_ver_list5 = [ras.bot_sb_1[0], ras.bot_sb_2[0], ras.bot_sb_3[0], ras.bot_sb_4[0]]
    ras_ver_list6 = [ras.bot_ts_1[0], ras.bot_ts_2[0], ras.bot_ts_3[0],
                     ras.bot_ts_4[0]]
    erod_severity_list = [ras.scald_sev[0], ras.wind_sev[0], ras.water_sheet_sev[0], ras.rill_sev[0], ras.gully_sev[0]]
    erod_stability_list = [ras.scald_stab[0], ras.wind_stab[0], ras.water_sheet_stab[0], ras.rill_stab[0],
                           ras.gully_stab[0]]
    erosion_comment_list = [ras.erosion_com[0]]
    north_fire_list = [ras.north_ff[0], ras.north_fi[0]]
    south_fire_list = [ras.south_ff[0], ras.south_fi[0]]

    ras_vert_list123456789101112 = [
        ras_ver_list1, ras_ver_list2, ras_ver_list3, ras_ver_list4, min_max_list, ras_ver_list5, ras_ver_list6,
        erod_severity_list, erod_stability_list, erosion_comment_list, north_fire_list, south_fire_list]
    print('ras_vert_list123456789101112: ', ras_vert_list123456789101112)
    return ras_vert_list123456789101112


def weeds_comment_fn(ras):
    """ Create a weed comment based on multiple variables.

            :param ras: pandas dataframe object (integrated).
            :return weed_comment_list: list object containing a weed comments derived from multiple fields. """

    # extract weed information.
    weed_list = [ras.weed1[0], ras.weed2[0], ras.weed3[0]]
    size_list = [ras.weed_size1[0], ras.weed_size2[0], ras.weed_size3[0]]
    den_list = [ras.weed_den1[0], ras.weed_den2[0], ras.weed_den3[0]]

    # create an empty list for weed comments
    weed_comment_list = []

    # loop through zipped lists and append comments.
    for weed, size, den in zip(weed_list, size_list, den_list):
        if weed != 'BLANK':
            comment1 = weed + ': ' + 'density(' + str(den) + ') size(' + str(size) + ')'
            # print(comment1)
            weed_comment_list.append(comment1)

    if not weed_comment_list:

        weed_comment_list.append('BLANK')

    return weed_comment_list


def main_routine(ras_csv, site, site_dir):
    print('step8_5_site_ras_data_extraction.py INITIATED.')

    # import the site ras transect csv
    ras = pd.read_csv(ras_csv).fillna('BLANK').replace('Nan', 'BLANK')

    # call the site_hor_list_variable_fn function
    ras_hort_list1234567891011121314 = site_hor_list_variable_fn(ras)

    # call the site_vert_list_variable_fn function
    ras_vert_list123456789101112 = site_vert_list_variable_fn(ras)

    # call the weeds_comment_fn function to extract a list of weed comments.
    weeds_comment_list = weeds_comment_fn(ras)

    # join lists into a string
    weeds_comment = ', '.join(weeds_comment_list)

    # convert comment to one blank if three exist
    """if weeds_comment == 'BLANK, BLANK, BLANK':
        final_weeds_comment = 'BLANK'
    else:
        final_weeds_comment = weeds_comment

        ras_hort_list1234567891011121314 = [
            ras_hor_list1, ras_hor_list2, ras_hor_list3, ras_hor_list4, ras_hor_list5, ras_hor_list6, cover_list,
            basal_list, density_list, erodible_soil, pas_ulil_list, weeds_comment_list, final_feral_list,
            condition_list]
        return ras_hort_list1234567891011121314"""

    # replace the weed comment with the final weed comment.
    ras_hort_list1234567891011121314[12] = [weeds_comment]

    print('step8_5_site_ras_data_extraction.py COMPLETED')

    return ras_hort_list1234567891011121314, ras_vert_list123456789101112

    """ras_hor_list1, ras_hor_list2, ras_hor_list3, ras_hor_list4, ras_hor_list5, ras_hor_list6, cover_list, basal_list, \
           density_list, ras_ver_list1, erodible_soil, pas_ulil_list, [weeds_comment], feral_list, condition_list, \
           ras_ver_list2, ras_ver_list3, ras_ver_list4, min_max_list, ras_ver_list5, ras_ver_list6, erod_severity_list, \
           erod_stability_list, erosion_comment_list, north_fire_list, south_fire_list"""




if __name__ == '__main__':
    main_routine()
