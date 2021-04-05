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

''' 

Discription.

transectVariables1P.py imports the three odk transect tables whech have been extracted for the previous script aggregateStarTransect1P.py and converts them to three seperate DataFrames, changing the 
varibles ((i.e. bare_ground) to the correct format for the RLM database.
This script exports a list containg three open DataFrames called clean_df_list.

On completion, the script calls step10_2_observation_sheet_formatting.py


Prerequisits

-- .html files contained in the site_dir. These files contain the point(repeat) information collected from the star transect ODK fiel form. These files have been extracted and downloaded fro
from ODK aggregate uin the previous script aggregateStarTransect1P.py.
=========

Variables
=========

above_values: dictionary
Dictionary object containing the naming convention within the ODK Aggregate table and the required naming convention for the Observational sheet for the 'above' feature.

below_values: dictionary
Dictionary object containing the naming convention within the ODK Aggregate table and the required naming convention for the Observational sheet for the 'below' feature.

clean_df_list: list
List object containing the cleaned 'df' DataFrame's containing only the 'ground', 'below', 'above' features with the RM database required terminology for the observational sheet transects pages.

df: DataFrame
DataFrame object housing the cleaned .html table information which is ready for observational sheet insertion.

html_list: list
List object containing all of the .html files within the xxxx directory - .html files contain the transect data collected when undergoing a 100 point transect using the star transect odk form xxxx.

ground_values: dictionary
Dictionary object containing the naming convention within the ODK Aggregate table and the required naming convention for the Observational sheet. for the 'ground' feature.

htmlTable: DataFrame
DataFrame object containing the complete html table derived from ODK Aggregate as a DaftaFrame.

htmlTablePath: str
String object housing the path to a single.html file contained within the html_list.

site_dir: str
String object containing the path to the newly created folder titled (YYYYMMDD_HHMM) within the export_dir directory.

========================================================================================================
'''

# Import modules
import pandas as pd
import glob
import warnings

warnings.filterwarnings("ignore")


def search_html_files_fn(site_dir):
    """ Search for all html files within a directory. """
    # create an empty list
    html_list = []

    for file in glob.glob(site_dir + '//*.html'):
        # append file paths to list
        html_list.append(file)

    return html_list


def table_clean_up_fn(html_list, site_dir):
    """ Filter the DataFrame and rename feature headings."""

    clean_df_list = []

    for htmlTablePath in html_list:
        html_table_list = pd.read_html(htmlTablePath)
        html_table = html_table_list[0]
        df = html_table.iloc[:, 2:5]
        df.columns = ['ground', 'below', 'above']

        # call the variable_renaming_fn function
        df = variable_renaming_fn(df)
        df.to_csv(site_dir + '\\cleanDF.csv')
        clean_df_list.append(df)

    return clean_df_list


def variable_renaming_fn(df):
    """ Rename the feature variables for observational sheet insertion. """

    # Change values in columns to required values for workbook
    ground_values = {'bare': 'BARE GROUND', 'gravel': 'GRAVEL', 'rock': 'ROCK', 'ash': 'ASH', 'litter': 'LITTER',
                     'cryptogram': 'CRYPTOGRAM',
                     'dead_annual_grass': 'DEAD ANNUAL GRASS', 'dead_perennial_grass': 'DEAD PERENNIAL GRASS',
                     'dead_annual_forb':
                         'DEAD ANNUAL FORB / HERB', 'dead_forb': 'DEAD PERENNIAL FORB / HERB',
                     'green_annual_grass': 'GREEN ANNUAL GRASS',
                     'green_perennial_grass': 'GREEN PERENNIAL GRASS', 'green_annual_forb': 'GREEN ANNUAL FORB / HERB',
                     'green_forb':
                         'GREEN PERENNIAL FORB / HERB', 'green_plant': 'GREEN PLANT', 'dead_plant': 'DEAD PLANT'}

    below_values = {'below_green': 'BELOW - GREEN', 'below_brown': 'BELOW - BROWN', 'below_dead': 'BELOW - DEAD',
                    'subshrub': 'SUBSHRUB - GREY', 'none': 'BLANK'}

    above_values = {'above_green': 'ABOVE - GREEN', 'above_brown': 'ABOVE - BROWN', 'above_dead': 'ABOVE - DEAD',
                    'above_in_crown':
                        'ABOVE - IN CROWN', 'not_in_crown': 'BLANK'}

    df['ground'] = df['ground'].replace(ground_values)
    df['below'] = df['below'].replace(below_values)
    df['above'] = df['above'].replace(above_values)

    return df


def main_routine(obs_data_list, ras_data_list, site, site_dir, star):
    """transectVariables1P.py imports the three odk transect tables which have been extracted for the previous script
    aggregateStarTransect1P.py and converts them to three separate DataFrames, changing the
    variables ((i.e. bare_ground) to the correct format for the RLM database.
    This script exports a list containing three open DataFrames called clean_df_list.
        :param obs_data_list:
        :param ras_data_list:
        :param site:
        :param site_dir:
        :param star: """

    print('step10_1_site_observation_sheet_processing_workflow.py INITIATED.')

    # call the search_html_files_fn function
    html_list = search_html_files_fn(site_dir)

    # call the table_clean_up_fn function
    clean_df_list = table_clean_up_fn(html_list, site_dir)

    print('step10_1_site_observation_sheet_processing_workflow.py COMPLETED.')
    print('step10_2_observation_sheet_formatting.py initiating..........')

    # call the step10_2_observation_sheet_formatting.py script.
    import step10_2_observation_sheet_formatting
    color_fill, heading1, heading2, heading3, heading4, heading5, heading6, heading7, heading8, workbook = \
        step10_2_observation_sheet_formatting.main_routine(site, site_dir)

    # call the step10_3_site_create_establishment_sheet.py script.
    import step10_3_site_create_establishment_sheet
    insert_vertical_data_fn, insert_horizontal_data_fn = step10_3_site_create_establishment_sheet.main_routine(
        heading1, heading2, heading3, heading7, workbook, obs_data_list)

    # call the step10_4_create_site_visit_sheet.py script.
    import step10_4_create_site_visit_sheet
    step10_4_create_site_visit_sheet.main_routine(
        heading1, heading2, heading3, heading7, workbook, obs_data_list, insert_vertical_data_fn)

    # call the step10_5_create_site_disturbance_sheet.py script.
    import step10_5_create_site_disturbance_sheet
    step10_5_create_site_disturbance_sheet.main_routine(
        color_fill, heading1, heading2, heading3, heading4, heading5, heading7, workbook, obs_data_list,
        site_dir, insert_vertical_data_fn, insert_horizontal_data_fn)

    # call the step10_6_create_site_transect_sheets.py script.
    import step10_6_create_site_transect_sheets
    step10_6_create_site_transect_sheets.main_routine(
        clean_df_list, color_fill, heading1, heading2, heading4, heading7, workbook, star,
        insert_vertical_data_fn)

    # call the step10_7_create_site_basal_sheet.py script.
    import step10_7_create_site_basal_sheet
    step10_7_create_site_basal_sheet.main_routine(
        color_fill, heading1, heading2, heading4, heading5, heading7, heading8, workbook, obs_data_list,
        insert_vertical_data_fn, insert_horizontal_data_fn)

    # call the step10_8_create_site_juvenile_stem_sheet.py script.
    import step10_8_create_site_juvenile_stem_sheet
    step10_8_create_site_juvenile_stem_sheet.main_routine(
        color_fill, heading1, heading2, heading4, heading5, heading7, heading8, workbook, obs_data_list,
        insert_vertical_data_fn, insert_horizontal_data_fn)

    # call the step10_9_create_site_ground_layer_sheet.py script.
    import step10_9_create_site_ground_layer_sheet
    step10_9_create_site_ground_layer_sheet.main_routine(
        color_fill, heading1, heading4, heading7, workbook, obs_data_list, insert_vertical_data_fn)

    # call the step10_10_create_site_cover_estimates.py script.
    import step10_10_create_site_cover_estimates
    step10_10_create_site_cover_estimates.main_routine(
        color_fill, heading1, heading2, heading3, heading4, heading6, heading7, workbook, obs_data_list,
        insert_vertical_data_fn, insert_horizontal_data_fn)

    # call the step10_11_create_site_condition_sheet.py script.
    import step10_11_create_site_condition_sheet
    step10_11_create_site_condition_sheet.main_routine(
        color_fill, heading1, heading2, heading3, heading4, heading7, workbook, obs_data_list, site,
        insert_vertical_data_fn, insert_horizontal_data_fn)


if __name__ == '__main__':
    main_routine()