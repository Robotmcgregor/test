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
import warnings

warnings.filterwarnings("ignore")


def photo_url_extraction_fn(row, site):
    """ extract the seven photograph urls.

         :param row: pandas dataframe row value object.
         :param site: string object containing the cleaned site name.
         :return photo_url_list: list object containing the site names and urls of all site photographs stores in
         odk aggregate."""

    photo_off = str(row['GROUP_SITE_PHOTO:PHOTO_OFF'])
    photo_c = str(row['GROUP_TRAN_PHOTO:PHOTO_C'])
    photo_n = str(row['GROUP_TRAN_PHOTO:PHOTO_N'])
    photo_ne = str(row['GROUP_TRAN_PHOTO:PHOTO_NE'])
    photo_se = str(row['GROUP_TRAN_PHOTO:PHOTO_SE'])
    photo_s = str(row['GROUP_TRAN_PHOTO:PHOTO_S'])
    photo_sw = str(row['GROUP_TRAN_PHOTO:PHOTO_SW'])
    photo_nw = str(row['GROUP_TRAN_PHOTO:PHOTO_NW'])

    photo_url_list = [site, photo_off, photo_c, photo_n, photo_ne, photo_se, photo_s, photo_sw, photo_nw]

    return photo_url_list


def main_routine(row, site):
    """ Extract the site photo urls.

        :param row: pandas dataframe row value object.
        :param site: pandas dataframe row value object.
        :return photo_url_list: list object containing the site names and urls of all site photographs stores in
             odk aggregate."""

    print('step2_4_photo_url_csv.py INITIATED.')

    # call photos function
    photo_url_list = photo_url_extraction_fn(row, site)

    print('step2_4_photo_url_csv.py COMPLETED.')

    return photo_url_list


if __name__ == '__main__':
    main_routine()
