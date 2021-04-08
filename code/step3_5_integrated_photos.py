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
    """ extract disturbance indicators, photo_url_extraction_fn urls and bearings.

        :param row: pandas dataframe row value object.
        :param site: string variable containing the site name.
        :return photo_list: list object containing the disturbance category, photo url and bearing information."""

    photo_list = [site]

    for i in range(8):

        dist = str(row['GROUP_PHOTOS:DEST' + str(i + 1)])
        photo_list.extend([dist])
        for n in range(3):

            dist_photo = str(
                row['GROUP_PHOTOS:GROUP_DEST' + str(i + 1) + '_PHOTO:DEST' + str(i + 1) + '_PHOTO' + str(n + 1)])
            dist_bearing = str(row['GROUP_PHOTOS:GROUP_DEST' + str(i + 1) + '_PHOTO:DEST' + str(i + 1) + '_PHOTO' + str(
                n + 1) + '_BEARING'])
            photo_list.append(dist_photo)
            photo_list.append(dist_bearing)

    return photo_list


def main_routine(clean_list, row, site):
    """Extract the disturbance photo urls, and bearings from the raw RMB integrated odk form result.

            :param clean_list: ordered list object that contains the processed integrated odk form result
            variables.
            :param row: pandas dataframe row value object.
            :param site: string variable containing the site name.
            :return: clean_list: ordered list object that contains the processed integrated odk form result
            variables variables processed within this script extend the list.
            :return: final_photo_list: list object containing the disturbance category, photo url and bearing information."""

    print('step3_5_integrated_photos.py INITIATED.')

    photo_list = photo_url_fn(row, site)
    clean_list.extend(photo_list[1:])

    print('step3_5_integrated_photos.py COMPLETED.')

    return clean_list, photo_list


if __name__ == '__main__':
    main_routine()
