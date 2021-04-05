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

from __future__ import print_function, division
import pandas as pd
import glob
import os
import warnings

warnings.filterwarnings("ignore")


def glob_dir_fn(dir_path, search_wild_card):
    """ Create a list of file paths based on search variable.

            :param dir_path: string object containing directory path.
            :param search_wild_card: string object containing the search wildcard information.
            :return csv_list: list object containing a list oc csv paths.
            :return df_list: list object containing open pandas data frames."""

    # create two empty lists
    csv_list = []
    df_list = []

    for file in glob.glob(dir_path + '\\' + search_wild_card):
        csv_list.append(file)

        df = pd.read_csv(file)
        df_list.append(df)

    return csv_list, df_list


def export_site_csv_fn(csv_list, temp_dir):
    """ Filter csv by site name and export csv.

            :param temp_dir: string object containing directory path.
            :param csv_list: list object containing a list oc csv paths, defined under glob_dir_fn function.
            :return df_list: list object containing open pandas data frames.
            :return dir_path: string object containing the path to a new directory called site_outputs.
            :return all_site_list: list object containing a unique list of sites.
            :return site_folder_path: string object containing the path to the current site folder within the dir_path
            directory called site_outputs."""

    # create empty lists
    complete_site_list = []
    complete_site_dir_list = []
    # create directory string variable
    dir_path = (temp_dir + '\\site_outputs')
    # create a new folder called site_outputs
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    for i in csv_list:
        # iterate through csv_list and create a pandas data frame for string path object (i)
        df = pd.read_csv(i)
        # create a list of unique site names from the pandas dataframe (df)
        unique_site_list = df.site.unique().tolist()
        for unique_site in unique_site_list:
            # iterate through the list of unique site names.
            complete_site_list.append(unique_site)

            site_folder_path = (dir_path + '\\' + str(unique_site))
            complete_site_dir_list.append(site_folder_path)

            # create a folder in the dir_path with the site name
            if not os.path.exists(site_folder_path):
                os.mkdir(site_folder_path)
            # separate the filename including the .csv extension from the path
            file_name = i.rsplit('\\', 1)[1]

            # create and export a site csv
            site_df = df[df['site'] == unique_site]
            site_df.to_csv(site_folder_path + '//' + str(unique_site) + '_' + file_name)
    else:
        site_folder_path = ""

    # remove duplicates from siteList
    all_site_list = list(dict.fromkeys(complete_site_list))

    # print(complete_site_dir_list)
    return dir_path, all_site_list, site_folder_path


def list_of_directories_fn(dir_path):
    """ Create list of site directory paths.

            :param dir_path: string object containing directory path defined under export_site_csv.
            :return site_dir_path_list: list object containing all site folder paths ans string variables."""

    site_dir_path_list = []

    for root, dirs, files in os.walk(dir_path, topdown=False):

        for name in dirs:
            # iterate through all directories within dir_path
            # join the root and the directory as a path
            site_dir_path = os.path.join(root, name)
            # append path to list
            site_dir_path_list.append(site_dir_path)

    return site_dir_path_list


def data_extraction_workflow_fn(directory_odk, site_dir_path_list, remote_desktop, veg_list_excel, shrub_list_excel):
    """ create list of site directory paths.


            :param directory_odk: string object containing the directory path to the raw odk result csv
            (cmd_args_fn defined).
            :param site_dir_path_list: list object containing all site folder paths ans string variables
            (list_of_directories_fn defined)
            :param remote_desktop: Boolean object - working on the PGB-BAS14 server (cmd_args_fn defined).
            :param veg_list_excel: string object containing the file path to the odk vegetation excel file
            (cmd_args_fn defined).
            :param shrub_list_excel: string object containing the file path to a second odk vegetation excel file
            (cmd_args_fn defined).
            :return site_dir_path_list: list object containing all site folder paths ans string variables.
            :return obs_data_list: list object containing list elements - each list contains the input variables for the
            observation spreadsheet, one list per page.
            :return ras_data_list: list object containing the input variables for the ras spreadsheet, one list per page.
            :return site: string variable containing the current site name.
            :return site_dir: string variable containing the current site directory path.
            :return star_csv: string object containing the path to the clean_star_transect.csv file created under
            step2_1_star_transect_processing_workflow. """

    for site_dir in site_dir_path_list:
        # iterate through site_dir_path_list
        _, site = site_dir.rsplit('\\', 1)
        integrated_csv = os.path.join(site_dir, site + '_clean_integrated.csv')
        # print(integrated_csv)
        if os.path.isfile(integrated_csv):

            print('clean_integrated.csv exists.')
            import step8_1_site_integrated_data_extraction
            establish_list2456, visit_vert_list2, disturb_vert_list12345678, dist_hor_list12345, cond_vert_list12, \
            cond_hor_list1, = step8_1_site_integrated_data_extraction.main_routine(integrated_csv, site_dir)

        else:

            establish_list2456 = [[], [], [], []]
            disturb_vert_list12345678 = [[], [], [], [], [], [], [], []]
            dist_hor_list12345 = [[], [], [], [], []]
            visit_vert_list2 = []
            cond_vert_list12 = [[], []]
            cond_hor_list1 = []

        star_csv = os.path.join(site_dir, site + '_clean_star_transect.csv')
        # print(star_csv)
        if os.path.isfile(star_csv):
            print('clean_star_transect.csv exists.')
            import step8_2_site_star_data_extraction
            estab_vert_list13, visit_vert_list1, ground_vert_list12345, estimates_hor_list12345, estimates_veg_list\
                = step8_2_site_star_data_extraction.main_routine(star_csv, site, site_dir, shrub_list_excel)

        else:
            estab_vert_list13 = [[], []]
            ground_vert_list12345 = [[], [], [], [], []]
            estimates_hor_list12345 = [[], [], [], [], []]
            estimates_veg_list = [[], [], [], [], [], [], [], [], [], [], []]

            visit_ver_list1 = []


            cond_hor_list1 = []


        basalCsv = os.path.join(site_dir, site + '_clean_basal.csv')
        print(basalCsv)
        if os.path.isfile(basalCsv):

            print('clean_basal.csv exists.')
            # call the step8_3_site_basal_sweep_data_extraction.py script.
            import step8_3_site_basal_sweep_data_extraction
            basal_hor_list1234, basal_vert_list123 = step8_3_site_basal_sweep_data_extraction.main_routine(
                basalCsv, site, site_dir, shrub_list_excel)

        else:

            basal_hor_list1234 = [[], [], [], []]
            basal_vert_list123 = [[], [], []]

        woody_csv = os.path.join(site_dir, site + '_clean_woody_thick.csv')
        # print(woody_csv)
        if os.path.isfile(woody_csv):

            print('clean_woody_thick.csv exists.')
            # run cleanIntData.
            import step8_4_site_woody_thickening_data_extraction
            woody_vert_list12345678910 = step8_4_site_woody_thickening_data_extraction.main_routine(
                woody_csv, site, site_dir, shrub_list_excel)

        else:
            woody_vert_list12345678910 = [[], [], [], [], [], [], [], [], [], []]


        # TODO turn this field back on when back at the office
        """
        photo_int_url_csv = os.path.join(site_dir, site + 'photo_IntUrl.csv')
        # print(photo_int_url_csv)
        if os.path.isfile(photo_int_url_csv):
            print('photoIntUrl.csv exists.')
            # run cleanIntData.
            import step8_6_site_integrated_photo_download
            photo_disturb_list = step8_6_site_integrated_photo_download.main_routine(photo_int_url_csv, site, site_dir)

        photo_star_url_csv = os.path.join(site_dir, site + '_photo_star_url.csv')
        # print(photo_star_url_csv)
        if os.path.isfile(photo_star_url_csv):
            print('photoStarUrl.csv exists.')
            # run cleanIntData.
            import step8_7_site_star_photo_download
            step8_7_site_star_photo_download.main_routine(photo_star_url_csv, site, site_dir)
        """
        ras_csv = os.path.join(site_dir, site + '_clean_ras.csv')
        # print(ras_csv)
        if os.path.isfile(ras_csv):

            print('cleanRas.csv exists.')
            # run cleanIntData.
            ras_data_list = []

            print('Ras.csv exists.')
            # run stepX_ras_basic.
            import step8_5_site_ras_data_extraction
            ras_hor_list1, ras_hor_list2, ras_hor_list3, ras_hor_list4, ras_hor_list5, ras_hor_list6, cover_list, basal_list, \
            density_list, ras_ver_list1, erodible_soil, pas_ulil_list, weeds_comment_list, feral_list, condition_list, \
            ras_ver_list2, ras_ver_list3, ras_ver_list4, min_max_list, ras_ver_list5, ras_ver_list6, erod_severity_list, \
            erod_stability_list, erosion_comment_list, north_fire_list, south_fire_list = \
                step8_5_site_ras_data_extraction.main_routine(ras_csv, site, site_dir)




        else:
            ras_hor_list1 = []
            ras_hor_list2 = []
            ras_hor_list3 = []
            ras_hor_list4 = []
            ras_hor_list5 = []
            ras_hor_list6 = []
            cover_list = []
            basal_list = []
            density_list = []
            erodible_soil = []
            pas_ulil_list = []
            weeds_comment_list = []
            feral_list = []
            condition_list = []
            ras_ver_list1 = []
            ras_ver_list2 = []
            ras_ver_list3 = []
            ras_ver_list4 = []
            min_max_list = []
            ras_ver_list5 = []
            ras_ver_list6 = []
            erod_severity_list = []
            erod_stability_list = []
            erosion_comment_list = []
            north_fire_list = []
            south_fire_list = []

        # Sort observation sheet data into page items.
        establish_data_list = [estab_vert_list13[0], establish_list2456[0], estab_vert_list13[1], establish_list2456[1],
                             establish_list2456[2], establish_list2456[3]]

        visit_data_list = [visit_vert_list1, visit_vert_list2]

        # create disturbance list of lists
        disturbance_data_list = [
            disturb_vert_list12345678[0], disturb_vert_list12345678[1], disturb_vert_list12345678[2],
            disturb_vert_list12345678[3], dist_hor_list12345[0], dist_hor_list12345[1], dist_hor_list12345[2],
            dist_hor_list12345[3], dist_hor_list12345[4], disturb_vert_list12345678[4], disturb_vert_list12345678[5],
            disturb_vert_list12345678[6], disturb_vert_list12345678[7]]

        basal_data_list = basal_hor_list1234[0], basal_hor_list1234[1], basal_hor_list1234[2], basal_hor_list1234[3], \
                          basal_vert_list123[0], basal_vert_list123[1], basal_vert_list123[2]

        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$', basal_data_list)
        woody_data_list = woody_vert_list12345678910

        ground_data_list = ground_vert_list12345

        estimates_data_list = estimates_hor_list12345

        estimates_veg_data_list = estimates_veg_list

        condition_data_list = [cond_vert_list12[0], cond_hor_list1, cond_vert_list12[1]]

        ras_data_list = [ras_hor_list1, ras_hor_list2, ras_hor_list3, ras_hor_list4, ras_hor_list5, ras_hor_list6,
                         cover_list, ras_ver_list1,
                         ras_ver_list2, ras_ver_list3, ras_ver_list4, min_max_list, basal_list, density_list,
                         ras_ver_list5, ras_ver_list6, erodible_soil, erod_severity_list, erod_stability_list,
                         erosion_comment_list,
                         pas_ulil_list, weeds_comment_list, feral_list, ['DO THIS'], north_fire_list, south_fire_list,
                         condition_list]

        obsDataList = [establish_data_list, visit_data_list, disturbance_data_list, basal_data_list, woody_data_list,
                       ground_data_list, estimates_data_list, estimates_veg_data_list, condition_data_list]

        # create paths to the required sit csv files

        ras_csv = os.path.join(site_dir, site + '_clean_ras.csv')

        star_csv = os.path.join(site_dir, site + '_clean_star_transect.csv')

        if remote_desktop == 'Yes':
            if os.path.isfile(star_csv):
                star = pd.read_csv(star_csv).fillna('BLANK').replace('Nan', 'BLANK')
                print('step9_2_aggregate_transect_extraction_remote_desktop.py initiating..........')
                # call the step9_2_aggregate_transect_extraction_remote_desktop.py script.
                import step9_2_aggregate_transect_extraction_remote_desktop
                step9_2_aggregate_transect_extraction_remote_desktop.main_routine(
                    obsDataList, ras_data_list, site, site_dir, star)

            elif os.path.isfile(ras_csv):
                ras = pd.read_csv(ras_csv).fillna('BLANK').replace('Nan', 'BLANK')

                # call the step11_1_site_ras_processing_workflow.py script.
                print('step11_1_site_ras_processing_workflow.py initiating..........')
                import step11_1_site_ras_processing_workflow
                step11_1_site_ras_processing_workflow.main_routine(
                    ras_data_list, site, site_dir, ras)

            else:
                print(site, ' observational/ras sheet will NOT be produced')

        else:

            # if star transect for the site exists -- create an observational sheet and populate.
            star_csv = os.path.join(site_dir, site + '_clean_star_transect.csv')
            # print(star_csv)
            if os.path.isfile(star_csv):
                star = pd.read_csv(star_csv).fillna('BLANK').replace('Nan', 'BLANK')
                print('step9_1_aggregate_transect_bypass_not_remote_desktop.py initiating..........')
                # call the step9_1_aggregate_transect_bypass_not_remote_desktop.py script.
                import step9_1_aggregate_transect_bypass_not_remote_desktop
                step9_1_aggregate_transect_bypass_not_remote_desktop.main_routine(directory_odk, obsDataList,
                                                                                  ras_data_list,
                                                                                  site, site_dir, star)
            elif os.path.isfile(ras_csv):
                ras = pd.read_csv(ras_csv).fillna('BLANK').replace('Nan', 'BLANK')

                print('step11_1_site_ras_processing_workflow.py initiating..........')
                import step11_1_site_ras_processing_workflow
                step11_1_site_ras_processing_workflow.main_routine(
                    ras_data_list, site, site_dir, ras)

    return obsDataList, ras_data_list, site, site_dir, star_csv


""" ---------------------------------------------------------------------------------------------"""


def main_routine(directory_odk, file_path, remote_desktop, temp_dir, veg_list_excel, shrub_list_excel):
    print('step7_site_processing_workflow.py INITIATED.')

    # call the globDir function
    csv_list, df_list = glob_dir_fn(temp_dir, '*.csv')

    # call the export SiteCsv function
    dir_path, all_site_list, site_folder_path = export_site_csv_fn(csv_list, temp_dir)

    # call the listOfDirectoriesFN function
    site_dir_path_list = list_of_directories_fn(dir_path)

    obs_data_list, ras_data_list, site, site_dir, star_csv = data_extraction_workflow_fn(directory_odk,
                                                                                         site_dir_path_list,
                                                                                         remote_desktop, veg_list_excel,
                                                                                         shrub_list_excel)

    print('step7_site_processing_workflow.py COMPLETE.')


if __name__ == "__main__":
    main_routine()
