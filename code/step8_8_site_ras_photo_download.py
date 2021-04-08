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
import pandas as pd
import warnings
import urllib

warnings.filterwarnings("ignore")


def photos_fn(ras):
    """ Extract ras photo url and bearings.

        :param ras: pandas data frame object.
        :return: photo_list: list object containing the photo url.
        :return bearing_list: list of photo bearings."""

    print('read in the file')
    photo_list = [ras.site_photo1.iloc[0], ras.site_photo2.iloc[0], ras.site_photo3.iloc[0]]
    bearing_list = [ras.bearing_photo1.iloc[0], ras.bearing_photo2.iloc[0],
                    ras.bearing_photo3.iloc[0]]

    photo_list2 = [ras.erosion_photo1.iloc[0], ras.erosion_photo2.iloc[0], ras.erosion_photo3.iloc[0]]
    bearing_list2 = [ras.bearing_erosion1.iloc[0], ras.bearing_erosion2.iloc[0],
                     ras.bearing_erosion3.iloc[0]]
    photo_list.extend(photo_list2)
    bearing_list.extend(bearing_list2)
    return photo_list, bearing_list


def save_photo_fn(photo_list, bearing_list, site, site_dir):
    """ Download and save the ras photographs captured in th integrated form.

            :param photo_list: list object containing the photo url.
            :param bearing_list: list object containing the photo bearing.
            :param site: string object containing the site name.
            :param site_dir: string object containing the path to the site directory. """

    photo_dir_list = []

    for photo, bear in zip(photo_list, bearing_list):
        print(photo)
        print(bear)
        if photo != 'BLANK':
            tail = str(photo[-20:]).split('3A')
            print('TAIL: ', tail)
            photo_name = tail[1].replace('PHOTO', '')
            bear2 = round(float(bear[2]), 4)
            bearing = str(bear2).replace('.', '-')
            output_str = (site_dir + '\\' + site + '_' + '_PHOTO' + photo_name + '_' + bearing + '.jpg')
            photo_dir_list.append(output_str)
            urllib.request.urlretrieve(photo, output_str)


def main_routine(photo_ras_url_csv, site, site_dir):
    """ Read in the site_photo_ras_url.csv file sort and download and name the relevant photographs.

            :param photo_ras_url_csv: string object containing the path to the site_photo_ras_url csv file.
            :param site: site: string object containing the site name.
            :param site_dir: string object containing the path to the site directory. """

    print('step8_8_site_ras_photo_download.py INITIATED.')

    ras_photo = pd.read_csv(photo_ras_url_csv, index_col=0).fillna('BLANK').replace('Nan', 'BLANK')
    ras_photo.to_csv(r'Z:\Scratch\Rob\code\draft\test_outputs\odk_outputs\ras_photos.csv')
    # call photos_fn function
    photo_list, bearing_list = photos_fn(ras_photo)
    # print("photos_fn function complete.")

    # call the savePhotos function
    save_photo_fn(photo_list, bearing_list, site, site_dir)

    print('step8_8_site_ras_photo_download.py COMPLETED.')


if __name__ == '__main__':
    main_routine()
