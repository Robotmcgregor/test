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

warnings.filterwarnings("ignore")


def woody_list_vertical_fn(woody):
    """ Extract woody thickening observation sheet variables as a list of lists.

            :param woody: pandas dataframe object.
            :return woody_vert_list12345678910: list object containing woody thickening  information to be inserted into the
            observation sheet vertically, including species lists and density values. """

    woody_ver_list1 = ['Yes']
    woody_ver_list2 = [woody.belt_width[0]]

    woody_ver_list3 = [int(woody.tree1[0]), int(woody.shrub1[0]), int(woody.tree1[0]) + int(woody.shrub1[0])]
    woody_ver_list4 = [int(woody.tree2[0]), int(woody.shrub2[0]), int(woody.tree2[0]) + int(woody.shrub2[0])]
    woody_ver_list5 = [int(woody.tree3[0]), int(woody.shrub3[0]), int(woody.tree3[0]) + int(woody.shrub3[0])]
    woody_ver_list6 = [int(woody.tree4[0]), int(woody.shrub4[0]), int(woody.tree4[0]) + int(woody.shrub4[0])]
    woody_ver_list7 = [int(woody.tree5[0]), int(woody.shrub5[0]), int(woody.tree5[0]) + int(woody.shrub5[0])]

    woody_ver_list8 = [int(woody.juv_tree_den[0]), int(woody.juv_shrub_den[0]),
                       (int(woody.juv_tree_den[0]) + int(woody.juv_shrub_den[0]))]

    woody_ver_list9 = [woody.bot_ts1[0], woody.bot_ts2[0], woody.bot_ts3[0], woody.bot_ts4[0],
                       woody.bot_ts5[0]]

    woody_ver_list10 = [woody.bot_sb1[0], woody.bot_sb2[0], woody.bot_sb3[0], woody.bot_sb4[0],
                        woody.bot_sb5[0]]

    woody_vert_list12345678910 = woody_ver_list1, woody_ver_list2, woody_ver_list3, woody_ver_list4, woody_ver_list5, \
                            woody_ver_list6, woody_ver_list7, woody_ver_list8, woody_ver_list9, woody_ver_list10
    return woody_vert_list12345678910


def common_name_extraction_fn(botanical_series, target_list, form):
    """ Extract the common name from the botanical_common_series excel document.

            :param botanical_series: pandas series object containing common and botanical species names.
            :param target_list: List of botanical species defined under basal_list_vertical_fn.
            :param form: string object passed into the function (tree or shrub).
            :return species_list: list object containing list elements [botanical_name, common_name].
            :return form_list: list object containing the form identifier of each species. """

    species_list = []
    form_list = []

    for botanical_name in target_list:
        botanical_name_list = botanical_series.copyBotanical2.tolist()
        if botanical_name in botanical_name_list:

            common_name = botanical_series.loc[botanical_series['copyBotanical2'] == botanical_name, 'copyCommon'].iloc[
                0]

        else:
            common_name = botanical_name

        form_list.append(form)
        species_list.append([botanical_name, common_name])

    return species_list, form_list


def main_routine(woody_csv, site, site_dir, shrub_list_excel):
    """ Extract variables from the current site woody data frame and return ordered lists for observational
    workbook insertion.

            :param woody_csv: sting object containing the file path to the current site woody csv file.
            :param site: string object containing the current site.
            :param site_dir: string object containing the path to the site directory.
            :param shrub_list_excel: string object containing the path to an excel document containing botanical and
                common names.
            :return basal_hor_list1234: list object containing basal information to be inserted into the observation
            sheet horizontally, including factor, basal species and count information.
            :return basal_vert_list123: list object containing basal information to be inserted into the observation
                sheet vertically, including species lists and basal species per ha values. """

    print('step8_4_site_woody_thickening_data_extraction.py INITIATED.')

    # woody = globDir(site_folder_path, '\\*cleanWoodyThickening.csv')
    woody = pd.read_csv(woody_csv).fillna('BLANK').replace('Nan', 'BLANK')

    tree_df = pd.read_excel(shrub_list_excel, sheet_name='CompleteTree')
    # filter out unwanted fields.
    tree_series = tree_df[['copyBotanical2', 'copyCommon']]

    shrub_df = pd.read_excel(shrub_list_excel, sheet_name='CompleteShrub')
    # filter out unwanted fields.
    shrub_series = shrub_df[['copyBotanical2', 'copyCommon']]

    # call the woody_list_vertical_fn function
    woody_vert_list12345678910 = woody_list_vertical_fn(woody)

    # call the commonNameExtraction FN function passing the tree botanical list
    woody_species_list1, woody_ver_list11 = common_name_extraction_fn(
        tree_series, woody_vert_list12345678910[8], 'Tree')
    print(woody_species_list1, woody_ver_list11)

    # call the common_name_extraction_fn function passing the shrub botanical list
    woody_species_list2, woody_ver_list12 = common_name_extraction_fn(
        shrub_series, woody_vert_list12345678910[9], 'Shrub')
    print(woody_species_list2, woody_ver_list12)

    # extend the woody_species_list1 containing all tree and shrub species and replace the list at woodyVerList[1]
    woody_species_list1.extend(woody_species_list2)

    # replace list position 1 in the woodyVerList list of lists.
    woody_vert_list12345678910[8] = woody_species_list1

    # extend formList1 (woody_ver_list11) with formList2 (woody_ver_list12)
    woody_ver_list11.extend(woody_ver_list12)

    # replace woodyVerList[2] with formList1
    woody_vert_list12345678910[9] = woody_ver_list11

    print('script8_4_woody_thickening_data_extraction.py COMPLETED')

    return woody_vert_list12345678910


if __name__ == '__main__':
    main_routine()
