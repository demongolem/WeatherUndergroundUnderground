'''
Created on Dec 11, 2020

Observe output data from BWI_Fetch and report on which days may have been missed.
Sometimes this is because data does not exist on an existing website.  Other
times this results from incorrect parameters being used when fetching data.
Thirdly, it could arise from temporary network issues which cause a date to
be saved.

We could be interested in reporting 2 separate groups: the first condition above
and then a combination of the second and third conditions into the other group.
It would be a waste of resource to try to get data if the server does not have
it, so these group of numbers would not be further processed.

An alternative way to handle the first group is to try to get the same information
from another server.  Right now, we only support WeatherUnderground, however
we could interact with other sites to try to get the missing data.

@author: Mendy
'''

import os

# prevent things like November 31
# February 29 is a headache
def is_valid_day(m, d, y):
    if m == 4 or m == 6 or m == 9 or m == 11:
        return d >= 1 and d <= 30
    elif m == 2:
        if y % 4 == 0:
            return d >= 1 and d <= 29
        else:
            return d >= 1 and d <= 28            
    else:
        return d >= 1 and d <= 31

def nopad_number(nmb):
    if nmb >= 0 and nmb <= 9:
        return nopad_single_digit(nmb)
    return str(nmb)

def nopad_single_digit(nmb):
    return str(nmb)

def pad_single_digit(nmb):
    nmb_str = str(nmb)
    if len(nmb_str) == 2:
        return nmb_str
    return '0' + nmb_str

# return any day on any year without output file
def find_all_lacking(output_dir):
    all_lacking_list = []
    # upper bound 12 * 31 * 75 = 27900
    for m in range(1, 13):
        for d in range(1, 32):
            for y in range(1945, 2020):
                if not is_valid_day(m, d, y):
                    continue
                filename = os.path.join(output_dir, 'gecko_out_' 
                                        + nopad_number(y) + '-' 
                                        + nopad_number(m) + '-' 
                                        + nopad_number(d) + '.txt')
                print(filename)
                if not os.path.isfile(filename):
                    all_lacking_list.append(filename)
    return all_lacking_list
           
# return any day on any year without output file from months not completely 
# missing data
def find_all_lacking_represented_months():
    pass

# get which lacking are due to data errors on weather underground and which
# are not
def get_lacking_groups():
    pass

# try to find data for the data from an alternate source
def fill_lacking_values_source(source_name):
    pass

def main(output_dir):
    comprehensize_list = find_all_lacking(output_dir)
    print(len(comprehensize_list))

if __name__ == '__main__':
    bwi_output_dir = '../output/bwi_fetch_output'
    main(bwi_output_dir)