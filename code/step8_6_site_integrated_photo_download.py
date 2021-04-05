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


def photo_fn(row):
    """ extract disturbance indicators, photo_url_extraction_fn urls and bearings.
        :param clean_list: ordered list object that contains the processed integrated odk form result
        variables.
        :param row: pandas dataframe row value object.
        :param site: string variable containing the site name.
        :return: clean_list: ordered list object that contains the processed integrated odk form result
        variables variables processed within this script extend the list.
        :return photo_list: list object containing the disturbance category, photo url and bearing information."""

    photo_list = []

    for i in range(8):

        dist_list = []

        str(i + 1)
        dist = str(row['dist' + str(i + 1)])
        for n in range(3):
            dist_photo = str(row['dist' + str(i + 1) + 'P' + str(i + 1)])
            dist_bearing = str(row['dist' + str(i + 1) + 'PB' + str(i + 1)])
            dist_list.append(dist)
            dist_list.append(dist_photo)
            dist_list.append(dist_bearing)
        photo_list.append(dist_list)
    print('Photo_list: ', photo_list)
    return photo_list


def save_photo_fn(dist_photo_list, site, site_dir):
    """Download and save the seven transect photos_fn."""

    photo_disturb_list = []

    for distList in dist_photo_list:
        disturb = str(distList[0])
        # print('disturb: ', disturb)
        photo_url = str(distList[1])
        # print('photo_url: ', photo_url)

        if photo_url != 'nan':
            # should be 'nan' due to str
            bear = str(distList[2])
            bearing = bear.replace('.', '-')

            # tail = str(i[-20:]).split('3A')
            # photoName = tail[1].replace('PHOTO', '')
            output_str = (
                    site_dir + '\\' + site + '_' + '_PHOTO_' + disturb + '_bearing_' + bearing + '.jpg')  # return date following site
            photo_disturb_list.append(output_str)
            urllib.request.urlretrieve(photo_url, output_str)

    return photo_disturb_list


def mainRoutine(photo_int_url_csv, site, site_dir):

    print('siteIntPhotoExtractionP.py INITIATED.')

    df = pd.read_csv(photo_int_url_csv)

    # call photos_fn function
    dist_photo_list = photo_fn(df)

    # call the savePhotos function
    photo_disturb_list = save_photo_fn(dist_photo_list, site, site_dir)

    return photo_disturb_list


if __name__ == '__main__':
    mainRoutine()
