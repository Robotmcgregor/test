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
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import modules
from __future__ import print_function, division
import os
from datetime import datetime
import argparse
import shutil
import sys
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def cmd_args_fn():
    p = argparse.ArgumentParser(
        description='''Process raw RMB odk outputs -> csv, shapefiles observational sheets, and Ras sheets.''')

    p.add_argument('-d', '--directory_odk', help='The directory containing ODK csv files.',
                   default=r'C:\Users\robot\new_z_drive\20210325_0640\20210323_1308')
    p.add_argument('-x', '--export_dir', help='Directory path for outputs.',
                   default=r'Z:\Scratch\Rob\chrome\chromedriver.exe')
    p.add_argument('-c', '--chrome_driver', help='File path for the chrome extension driver.',
                   default=r"Z:\Scratch\Rob\chrome\20201117\chromedriver.exe")
    p.add_argument('-r', '--remote_desktop', help='Working on the remote_desktop? - Enter yes or No.',
                   default="Yes")
    p.add_argument('-v', '--veg_list_excel', help='Odk veg list Excel file path.',
                   default=r"C:\Users\robot\new_z_drive\20210325_0640\20210323_1308\odk_veg_list_final.xlsx")
    p.add_argument('-s', '--shrub_list_excel', help='Odk shrub list Excel file path.',
                   default=r"C:\Users\robot\new_z_drive\20210325_0640\20210323_1308\dominantVegSplitDistricts2.xlsx")
    p.add_argument('-p', '--pastoral_estate', help='File path to the pastoral estate shapefile.',
                   default=r"C:\Users\Rob\PycharmProjects\rmb_aggregate_processing\shapefiles\pastoral_estate.shp")

    cmd_args = p.parse_args()

    if cmd_args.directory_odk is None:
        p.print_help()

        sys.exit()

    return cmd_args


def temporary_dir(export_dir):
    """ Create a temporary directory 'date_time'.
    :param export_dir: string object path to an existing directory where an output folder will be created.
    """
    # create file name based on date and time.
    date_time_replace = str(datetime.now()).replace('-', '')
    date_time_list = date_time_replace.split(' ')
    date_time_list_split = date_time_list[1].split(':')
    temp_dir = export_dir + '\\' + str(date_time_list[0]) + '_' \
               + str(date_time_list_split[0]) + str(date_time_list_split[1])
    # check if the folder already exists - if False = create directory, if True = return error message zzzz.
    try:
        shutil.rmtree(temp_dir)

    except:
        print('The following directory did not exist: ', temp_dir)

    # create folder a temporary folder titled (titled 'tempFolder'
    os.makedirs(temp_dir)

    return temp_dir


def raw_odk_output_workflow_fn(file_path, search_criteria, temp_dir, veg_list_excel, pastoral_estate):
    """ Defines the script pathway depending on what raw ODK files are contained in the directory.

            :param file_path: string object containing the dir_path concatenated with search_criteria.
            :param search_criteria: string object containing the raw odk file name and type.
            :param temp_dir: string object path to the created output directory (date_time).
            :param veg_list_excel: string object path to the odk veglist excel file (botanical and common names).
            :param pastoral_estate: string object containing the file path to the pastoral estate shapefile. """

    print("Searching for ODK outputs..........")
    print(file_path)

    if search_criteria == 'RM_Star_Transect_results.csv':

        # call the step2_1_star_transect_processing_workflow.py script.
        import step2_1_star_transect_processing_workflow
        step2_1_star_transect_processing_workflow.main_routine(file_path, temp_dir, veg_list_excel)

    elif search_criteria == 'RMB_Integrated_Site_results.csv':

        # call the step3_1_integrated_processing_workflow.py script.

        import step3_1_integrated_processing_workflow
        step3_1_integrated_processing_workflow.main_routine(file_path, temp_dir)

    elif search_criteria == 'RMB_Basal_Sweep_results.csv':

        # call the step4_1_basal_processing_workflow.py script.
        import step4_1_basal_processing_workflow
        step4_1_basal_processing_workflow.main_routine(file_path, temp_dir)

    elif search_criteria == 'RMB_Woody_Thickening_results.csv':

        # call the step5_1_woody_processing_workflow.py script.
        import step5_1_woody_processing_workflow
        step5_1_woody_processing_workflow.main_routine(file_path, temp_dir)

    elif search_criteria == 'RMB_Rapid_Assessment_RAS_results.csv':

        print('RAS not completed')
        # call the step6_1_ras_processing_workflow.py script.
        import step6_1_ras_processing_workflow
        step6_1_ras_processing_workflow.main_routine(file_path, temp_dir, veg_list_excel, pastoral_estate)


def odk_export_csv_checker_fn(dir_path, located_list, search_criteria, temp_dir, veg_list_excel, shrub_list_excel,
                              pastoral_estate):
    """ Search for a specific odk csv output.

        :param located_list:
        :param dir_path: string object containing the raw odk output csv files.
        :param search_criteria: string object containing the raw odk file name and type.
        :param temp_dir: string object path to the created output directory (date_time).
        :param veg_list_excel: string object path to the odk veglist excel file (containing botanical and common names).
        :param shrub_list_excel: string object path to the odk veglist excel file (containing a 3P grass list).
        :param pastoral_estate: string object containing the file path to the pastoral estate shapefile. """

    file_path = (dir_path + '\\' + search_criteria)

    if not os.path.exists(file_path):
        print(search_criteria, ' not located.')
        df = pd.DataFrame()
        located = False
    else:
        print(search_criteria, ' located, initiating script..........')
        # call the import_script_fn function.
        raw_odk_output_workflow_fn(file_path, search_criteria, temp_dir, veg_list_excel, pastoral_estate)

        located = True
    located_list.append(located)

    return file_path


def main_routine():
    """ This pipeline searches through a directory for the Rangelends Monitoring Branch raw odk outputs.
            :param directory_odk: (command argument) directory_odk
            :param export_dir: (command argument) cmd_args.export_dir
            :param chrome_driver: (command argument) cmd_args.chrome_driver
            :param remote_desktop: (command argument) cmd_args.remote_desktop
            :param veg_list_excel: (command argument) cmd_args.veg_list_excel
            :param shrub_list_excel: (command argument) cmd_args.shrub_list_excel
            :param pastoral_estate: (command argument) cmd_args.pastoral_estate
            :return observation spreadsheet (one per site)
            :return ras spreadsheet (one per site)
            :return

            inputs must include raw odk csv with the name unchanged from the aggregate download.
            Additional inputs are required if running the pipeline outside of the remote desktop (PG-BAS14) and
            processing included integrated data.
            Additional inputs:
     - 3 x .html outputs named of the star transect tables (3 per site)
        naming convention applies (i.e. 'BKE23A_Transect1_.html')

    If running from the remote desktop all downloads are automated.

    """
    print('createFormatObservationXlsx.py INITIATED.')

    # read in the command arguments
    cmd_args = cmd_args_fn()
    directory_odk = cmd_args.directory_odk
    export_dir = cmd_args.export_dir
    chrome_driver = cmd_args.chrome_driver
    remote_desktop = cmd_args.remote_desktop
    veg_list_excel = cmd_args.veg_list_excel
    shrub_list_excel = cmd_args.shrub_list_excel
    pastoral_estate = cmd_args.pastoral_estate

    # create an empty list
    located_list = []

    # call the temporary_dir function.
    temp_dir = temporary_dir(export_dir)

    # call the odk_export_csv_checker_fn function - search for star transect outputs
    file_path = odk_export_csv_checker_fn(directory_odk, located_list, 'RM_Star_Transect_results.csv',
                              temp_dir,
                              veg_list_excel, shrub_list_excel, pastoral_estate)

    # call the odk_export_csv_checker_fn function - search for star integrated outputs
    file_path = odk_export_csv_checker_fn(directory_odk, located_list, 'RMB_Integrated_Site_results.csv',
                              temp_dir,
                              veg_list_excel, shrub_list_excel, pastoral_estate)

    # call the odk_export_csv_checker_fn function - search for basal sweep outputs
    file_path = odk_export_csv_checker_fn(directory_odk, located_list, 'RMB_Basal_Sweep_results.csv', temp_dir,
                              veg_list_excel, shrub_list_excel, pastoral_estate)

    # call the odk_export_csv_checker_fn function - search for woody thickening outputs
    file_path = odk_export_csv_checker_fn(directory_odk, located_list, 'RMB_Woody_Thickening_results.csv',
                              temp_dir,
                              veg_list_excel, shrub_list_excel, pastoral_estate)

    # call the odk_export_csv_checker_fn function - search for ras outputs
    file_path = odk_export_csv_checker_fn(directory_odk, located_list, 'RMB_Rapid_Assessment_RAS_results.csv',
                              temp_dir,
                              veg_list_excel, shrub_list_excel, pastoral_estate)

    print('''====================================================''')

    # Verify if an odk file was created and call step18_completeOdkOutputs2.
    if True in located_list:
        print('True')
        # call the step7_site_processing_workflow.py script.
        print('step7_site_processing_workflow.py initiating..........')
        import step7_site_processing_workflow
        step7_site_processing_workflow.main_routine(directory_odk, file_path, remote_desktop,
                                                    temp_dir, veg_list_excel, shrub_list_excel)

    else:
        print('No observational/RAS sheets will be produced')


if __name__ == '__main__':
    main_routine()
