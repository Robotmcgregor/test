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
import pandas as pd
import warnings
from datetime import datetime
import numpy as np
import geopandas as gpd

warnings.filterwarnings("ignore")


def string_clean_upper_fn(dirty_string):
    """ Remove whitespaces and clean strings.

            :param dirty_string: string object.
            :return clean_string: processed string object."""

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


def date_time_fn(row):
    """ Extract and reformat date and time fields.
            :param row: pandas dataframe row value object
        :return date_time_list: list object containing two string variables: s_date2, obs_date_time. """

    s_date, s_time = row['START'].split('T')
    # date clean
    s_date2 = s_date[-2:] + '/' + s_date[-5:-3] + '/' + s_date[2:4]

    # time clean
    s_hms, _ = s_time.split('.')
    s_hm = s_hms[:5]
    if s_hm[:1] == '0':
        s_hm2 = s_hm[1:5]
    else:
        s_hm2 = s_hm[:5]

    dirty_obs_time = datetime.strptime(s_hm2, '%H:%M')

    obs_time = dirty_obs_time.strftime("%I:%M %p")
    obs_date_time = s_date2 + ' ' + obs_time

    date_time_list = [s_date2, obs_date_time]
    return date_time_list


def recorder_fn(row):
    """ Extract recorder information.

            :param row: pandas dataframe row value object.
            :return obs_recorder: string object containing recorder name. """

    recorder = str(row['OFFICER_ONE:RECORDER'])
    # clean and incorporate recorder other
    if recorder == 'other':
        recorder = recorder.replace('other', str((row['OFFICER_ONE:OTHER_RECORDER'])))
    # clean variable, remove white space and possible typos
    recorder = string_clean_title_fn(recorder)
    # print(recorder)
    first, second = recorder.split(' ')
    obs_recorder = second + ', ' + first

    return obs_recorder


def estimator_fn(row):
    """ Extract estimator information.

        :param row: pandas dataframe row value object.
        :return obs_estimator: string object containing estimator name. """

    estimator = str(row['OFFICER_TWO:ESTIMATOR'])
    # clean variable, remove white space and possible typos
    if estimator == 'other':
        estimator = estimator.replace('other', str((row['OFFICER_TWO:OTHER_ESTIMATOR'])))
    estimator = string_clean_title_fn(estimator)
    # print(estimator)
    first, second = estimator.split(' ')
    obs_estimator = second + ', ' + first

    return obs_estimator


def location_fn(row):
    """ extract the district, property and site information.

            :param row: pandas dataframe row value object.
            :return location_list: list object containing five string variables:
            district, listed_property, unlisted_property, final_property and site. """

    # district
    district = string_clean_title_fn(str(row['DISTRICT']))

    listed_property = str(row['PROP:PROPERTY'])

    # property name
    if str(row['PROP:PROPERTY']) in set(
            ('NP_prop_new', 'B_property_outside', 'D_property_outside', 'G_property_outside',
             'K_property_outside', 'NAS_property_outside', 'P_property_outside', 'R_property_outside',
             'SAS_property_outside', 'SP_property_outside', 'TC_property_outside', 'VR_property_outside',
             'NP_property_outside')):

        listed_property = np.nan
        unlisted_property = string_clean_title_fn(str(row['PROP:NOT_PASTORAL_NAME2']))
        final_property = string_clean_title_fn(str(row['PROP:NOT_PASTORAL_NAME2']))
    else:
        listed_property = string_clean_title_fn(str(row['PROP:PROPERTY']))
        unlisted_property = np.nan
        final_property = string_clean_title_fn(str(row['PROP:PROPERTY']))

    site1 = str(row['GROUP_SITE:SITE_FINAL'])

    # call the stringCleanFN function
    site = string_clean_upper_fn(site1)
    location_list = [district, listed_property, unlisted_property, final_property, site]
    return location_list


def meta_data_fn(row):
    """ Extract and clean the form key information.

            :param row: pandas dataframe row value object.
            :return meta_key: string object containing the odk form identifier key.
            :return clean_meta_key: string object containing the cleaned odk form identifier key.
            :return form_name: string object containing the odk form identifier key. """

    meta_key = str(row['meta:instanceID'])
    clean_meta_key = meta_key[5:]
    form_name = str(row['meta:instanceName'])

    meta_data_list = [meta_key, clean_meta_key, form_name]
    return meta_data_list


def gps_points_fn(row):
    """ Extract the coordinate information.

            :param row: pandas dataframe row value object.
            :return gps: string object containing the gps device information.
            :return c_lat: float object containing the center point latitude information.
            :return c_lon: float object containing the center point longitude information.
            :return c_acc: float object containing the center point accuracy information (mobile device only).
            :return off_direct: string object containing the offset direction information.
            :return o_lat: float object containing the offset point latitude information.
            :return o_lon: float object containing the offset point longitude information.
            :return o_acc: float object containing the center point accuracy information."""

    gps = str(row['GPS_SELECT'])

    if gps == 'now_device':
        c_lat = float(row['GPS1:Latitude'])
        c_lon = float(row['GPS1:Longitude'])
        c_acc = float(row['GPS1:Accuracy'])

    elif gps == 'later_device':
        c_lat = float(row['GPS3:Latitude'])
        c_lon = float(row['GPS3:Longitude'])
        c_acc = float(row['GPS3:Accuracy'])

    elif gps == 'now_gps':
        c_lat = float(row['GPS2:GPS2_LAT2'])
        c_lon = float(row['GPS2:GPS2_LONG2'])
        c_acc = np.nan

    else:  # later_gps
        c_lat = float(row['GPS4:GPS4_LAT'])
        c_lon = float(row['GPS4:GPS4_LONG'])
        c_acc = np.nan

    lat_lon_list = [gps, c_lat, c_lon, c_acc]
    return lat_lon_list


def main_routine(file_path, temp_dir):
    """ Control the integrated data extraction workflow producing two outputs.

            :param file_path: string object containing the dir_path concatenated with search_criteria.
            :param temp_dir: string object path to the created output directory (date_time).
            :return clean_integrated.csv: clean csv file output to the command argument export directory.
            :return photo_integrated_url.csv:  csv file containing photo url information to the command argument export
            directory. """

    print('step3_1_integrated_processing_workflow.py INITIATED.')

    # Read in the star transect csv as  a Pandas DataFrame.
    df = pd.read_csv(file_path)

    final_clean_list = []
    final_photo_url_list = []

    # from datetime import datetime
    for index, row in df.iterrows():
        # call the date_time_fn function to extract date and time information.
        date_time_list = date_time_fn(row)

        # call the recorder_fn function to extract the recorder information.
        obs_recorder = recorder_fn(row)

        # call the location_fn function to extract the district, property and site information.
        location_list = location_fn(row)

        # call the gps_points_fn function to extract the longitude and latitude information.
        lat_lon_list = gps_points_fn(row)
        # print("gpsPoints function complete.")

        # call the meta_date_fn function to extract the unique identifier information for each form record.
        meta_data_list = meta_data_fn(row)

        # extract the site variable from the location list
        site = location_list[4:][0]

        # create a clean list and append/extend output lists and variables
        clean_list = [site]
        clean_list.extend(date_time_list)
        clean_list.append(obs_recorder)
        clean_list.extend(location_list[:4])
        clean_list.extend(lat_lon_list)

        print('step3_1_integrated_processing_workflow.py COMPLETED')
        print('step3_2_integrated_establishment.py initiating...........')

        # call the step3_2_integrated_establishment.py script.
        import step3_2_integrated_establishment
        clean_list = step3_2_integrated_establishment.main_routine(
            clean_list, row, string_clean_capital_fn, string_clean_title_fn)

        # call the step3_3_integrated_disturbance.py script.
        import step3_3_integrated_disturbance
        clean_list = step3_3_integrated_disturbance.main_routine(
            clean_list, row, string_clean_capital_fn)

        # call the step3_4_integrated_disturbance2.py script.
        import step3_4_integrated_disturbance2
        clean_list = step3_4_integrated_disturbance2.main_routine(
            clean_list, row, string_clean_capital_fn)

        # call the step3_5_integrated_photos.py script.
        import step3_5_integrated_photos
        clean_list, photo_url_list = step3_5_integrated_photos.main_routine(
            clean_list, row, site)

        clean_list.extend(meta_data_list)
        final_clean_list.append(clean_list)
        final_photo_url_list.append(photo_url_list)

    # print(final_int_clean_list)

    integrated_df = pd.DataFrame(final_clean_list)
    integrated_df.columns = [
        'site', 'date', 'date_time', 'recorder', 'district', 'prop', 'unlist_prop', 'final_prop', 'gps', 'c_lat',
        'c_lon', 'c_acc', 'paddock', 'desc', 'reason', 'landscape', 'soil_colour',
        'land_system', 'ls_consist', 'ls_alt', 'ls_source', 'water_point', 'water_name', 'water_dir', 'water_dist',
        'est_track', 'est_track_dist', 'est_track_dir', 'est_inf_oth', 'est_inf_oth_dist', 'rev_inf', 'rev_inf_dist',
        'rev_inf_comm', 'season_cond', 'soil_moist', 'atm_cond', 'soil_cracks', 'erod_soil', 'clearing', 'cyclone',
        'dieback', 'clear_age', 'clear_type', 'clear_pdk', 'land_use', 'cyc_comm', 'die_comm', 'camel', 'rabbit',
        'donkey', 'horse', 'pig', 'buffalo', 'nat_herb', 'other_feral', 'feral_comm', 'north_ff', 'north_fi',
        'south_ff', 'south_fi', 'weed1', 'weed_size1', 'weed_den1', 'weed_comm1', 'weed2', 'weed_size2', 'weed_den2',
        'weed_comm2', 'weed3', 'weed_size3', 'weed_den3', 'weed_comm3', 'scald_sev', 'scald_stab', 'wind_sev',
        'wind_stab', 'water_sheet_sev', 'water_sheet_stab', 'rill_sev', 'rill_stab', 'gully_sev', 'gully_stab',
        'erosion_comm', 'cattle_pad', 'cattle_tramp', 'greenness', 'green_comm', 'abundance', 'abund_comm', 'past_util',
        'past_util_comm', 'condition', 'cond_note', 'dev_note',
        'dist1', 'dist1_p1', 'dist1_pb1', 'dist1_p2',
        'dist1_pb2', 'dist1_p3', 'dist1_pb3', 'dist2', 'dist2_p1', 'dist2_pb1', 'dist2_p2', 'dist2_pb2', 'dist2_p3',
        'dist2_pb3', 'dist3', 'dist3_p1', 'dist3_pb1', 'dist3_p2', 'dist3_pb2', 'dist3_p3', 'dist3_pb3', 'dist4',
        'dist4_p1', 'dist4_pb1', 'dist4_p2', 'dist4_pb2', 'dist4_p3', 'dist4_pb3', 'dist5', 'dist5_p1', 'dist5_pb1',
        'dist5_p2', 'dist5_pb2', 'dist5_p3', 'dist5_pb3', 'dist6', 'dist6_p1', 'dist6_pb1', 'dist6_p2', 'dist6_pb2',
        'dist6_p3', 'dist6_pb3', 'dist7', 'dist7_p1', 'dist7_pb1', 'dist7_p2', 'dist7_pb2', 'dist7_p3', 'dist7_pb3',
        'dist8', 'dist8_p1', 'dist8_pb1', 'dist8_p2', 'dist8_pb2', 'dist8_p3', 'dist8_pb3', 'meta_key',
        'clean_meta_key', 'form', ]

    integrated_df2 = integrated_df.replace('Nan', 'nan')

    csv_output = (temp_dir + '\\clean_integrated.csv')
    integrated_df2.to_csv(csv_output)

    print('------------------------------------------------------------')
    print('The following outputs have been created:')
    print('-', csv_output)

    # create a geoDataFrame
    integrated_gdf = gpd.GeoDataFrame(integrated_df2,
                                      geometry=gpd.points_from_xy(integrated_df.c_lon, integrated_df.c_lat),
                                      crs="EPSG:4326")
    shp_output = (temp_dir + '\\clean_integrated.shp')

    # Export shapefile
    integrated_gdf.to_file(shp_output, driver='ESRI Shapefile')

    print('-', shp_output)

    photo_list_df = pd.DataFrame(final_photo_url_list)
    photo_list_df.columns = [
        'site', 'dist1', 'dist1_p1', 'dist1_pb1', 'dist1_p2', 'dist1_pb2', 'dist1_p3', 'dist1_pb3',
        'dist2', 'dist2_p1', 'dist2_pb1', 'dist2_p2', 'dist2_pb2', 'dist2_p3', 'dist2_pb3',
        'dist3', 'dist3_p1', 'dist3_pb1', 'dist3_p2', 'dist3_pb2', 'dist3_p3', 'dist3_pb3',
        'dist4', 'dist4_p1', 'dist4_pb1', 'dist4_p2', 'dist4_pb2', 'dist4_p3', 'dist4_pb3',
        'dist5', 'dist5_p1', 'dist5_pb1', 'dist5_p2', 'dist5_pb2', 'dist5_p3', 'dist5_pb3',
        'dist6', 'dist6_p1', 'dist6_pb1', 'dist6_p2', 'dist6_pb2', 'dist6_p3', 'dist6_pb3',
        'dist7', 'dist7_p1', 'dist7_pb1', 'dist7_p2', 'dist7_pb2', 'dist7_p3', 'dist7_pb3',
        'dist8', 'dist8_p1', 'dist8_pb1', 'dist8_p2', 'dist8_pb2', 'dist8_p3', 'dist8_pb3']
    # starTransectDF.set_index('site', inplace=True)
    csv_output = (temp_dir + '\\photo_integrated_url.csv')
    photo_list_df.to_csv(csv_output)
    print('-', csv_output)

    print('The Integrated ODK Aggregate csv file has been processed.........')


if __name__ == '__main__':
    main_routine()
