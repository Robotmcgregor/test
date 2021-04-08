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
import glob
import warnings
import urllib

warnings.filterwarnings("ignore")


def globDir(dirPath, searchCriteria):
    """ Search a specified Directory (zonalStats) and concatenate all records to a DataFrame. """

    if glob.glob(dirPath + searchCriteria):
        for file in glob.glob(dirPath + searchCriteria):
            # convert csv to DataFrame
            df = pd.read_csv(file)
    else:
        print('file not exist')
        df = pd.DataFrame()

    return (df)

def string_clean_upper_fn(dirty_string):
    """ Remove whitespaces and clean strings.

            :param dirty_string: string object.
            :return clean_string: processed string object. """

    str1 = dirty_string.replace('_', ' ')
    str2 = str1.replace('-', ' ')
    str3 = str2.upper()
    clean_string = str3.strip()
    return clean_string


def photo_fn(df):
    """ Extract disturbance indicators, photo_url_extraction_fn urls and bearings.

        :param df: pandas data frame object.
        :return: photo_list: list object containing the kind of disturbance, the photo url and the photo bearing. """

    photo_list = []

    for i in range(8):

        dist = df['dist' + str(i + 1)].iloc[0]

        for n in range(3):
            dist_photo = df['dist' + str(i + 1) + '_p' + str(n + 1)].iloc[0]
            dist_bearing = df['dist' + str(i + 1) + '_pb' + str(n + 1)].iloc[0]
            list_a = [dist, dist_photo, dist_bearing]
            photo_list.append(list_a)

    return photo_list


def save_photo_fn(photo_list, site, site_dir):
    """ Download and save the disturbance photographs captured in th integrated form.

            :param photo_list: list object containing the kind of disturbance, the photo url and the photo bearing.
            :param site: string object containing the site name.
            :param site_dir: string object containing the path to the site directory. """

    photo_disturb_list = []

    for dist in photo_list:

        if dist[1] != 'BLANK':
            disturb = string_clean_upper_fn(str(dist[0]))
            photo_url = dist[1]
            bear = round(float(dist[2]), 4)
            bearing = str(bear).replace('.', '-')
            photo_number = str(photo_url[-6:])
            output_str = (
                    site_dir + '\\' + site + '_' + photo_number + '_' + disturb + '_BEARING_' + bearing + '.jpg')  # return date following site
            photo_disturb_list.append(output_str)
            urllib.request.urlretrieve(photo_url, output_str)


def main_routine(photo_int_url_csv, site, site_dir):
    """ Read in the site_photo_integrated_url.csv file sort and download and name the relevant photographs.

            :param photo_int_url_csv: string object containing the path to the site_photo_integrated_url csv file.
            :param site: site: string object containing the site name.
            :param site_dir: string object containing the path to the site directory. """

    print('step8_6_integrated_photo_download.py INITIATED.')

    df = pd.read_csv(photo_int_url_csv, index_col=0).fillna('BLANK').replace('Nan', 'BLANK')
    df.to_csv(r"Z:\Scratch\Rob\code\draft\test_outputs\odk_outputs\int_photo.csv")
    # call photos_fn function
    photo_list = photo_fn(df)

    # call the savePhotos function
    save_photo_fn(photo_list, site, site_dir)

    print('step8_6_integrated_photo_download.py COMPLETED.')

if __name__ == '__main__':
    main_routine()
