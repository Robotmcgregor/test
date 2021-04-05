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
import warnings

warnings.filterwarnings("ignore")


def photo_url_fn(row, site):
    """ extract site photo url string and bearings.

        :param row: pandas dataframe row value object.
        :param site: string variable containing the site name.
        :return photo_list: list object containing the disturbance category, photo url and bearing information."""

    photo_list = [site]
    if str(row['GPS_SELECT']) == 'now_gps' or str(row['GPS_SELECT']) == 'now_device':

        for i in range(3):
            site_photo = str(row['GROUP_SITE_PHOTO2:SITE_PHOTO' + str(i+1) + '_' + str(i+1)])
            photo_bearing = str(row['GROUP_SITE_PHOTO2:SITE_PHOTO' + str(i+1) + '_' + str(i+1) + '_BEARING'])

            list_a = [site_photo, photo_bearing]
            photo_list.extend(list_a)

    else:

        for i in range(3):
            site_photo = str(row['GROUP_SITE_PHOTO:SITE_PHOTO' + str(i+1)])
            photo_bearing = str(row['GROUP_SITE_PHOTO:SITE_PHOTO' + str(i+1) + '_BEARING'])

            list_a = [site_photo, photo_bearing]
            photo_list.extend(list_a)

    return photo_list


def erosion_photo_url_fn(row):
    """ extract site photo url string and bearings.

        :param row: pandas dataframe row value object.
        :return photo_list: list object containing the erosion category, photo url and bearing information."""

    photo_list = []

    for i in range(3):
        site_photo = str(row['DISTURBANCE_EROSION:GROUP_EROSION_PHOTO:EROSION_PHOTO' + str(i+1)])
        photo_bearing = str(row['DISTURBANCE_EROSION:GROUP_EROSION_PHOTO:EROSION_PHOTO' + str(i+1) + '_BEARING'])

        list_a = [site_photo, photo_bearing]
        photo_list.extend(list_a)

    return photo_list


def main_routine(clean_list, row, site):
    """ Extract the disturbance photo urls.

            :param clean_list: list object containing processed variables.
            :param row: pandas dataframe row value object.
            :param site: pandas dataframe row value object.
            :return photo_url_list: list object containing the site names and urls of all site photographs stores in
              odk aggregate."""

    print('step_22_ras_photos_pipeline.py INITIATED.')

    # call photos function
    photo_url_list = photo_url_fn(row, site)

    erosion_photo_url_list = erosion_photo_url_fn(row)
    # extend results to the photo_url_list
    photo_url_list.extend(erosion_photo_url_list)

    # extend the photo_url_list to the clean_list excluding the site variable [1:]
    clean_list.extend(photo_url_list[1:])
    print('clean_list: ', clean_list)

    print('step6_6_ras_photos.py COMPLETED.')

    return clean_list, photo_url_list


if __name__ == '__main__':
    main_routine()
