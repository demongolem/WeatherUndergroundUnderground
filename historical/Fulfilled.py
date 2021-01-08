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

import math
import os
import pandas as pd

import BWI_Fetch
import TextMaxMin

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
                if not os.path.isfile(filename):
                    all_lacking_list.append(filename)
    return all_lacking_list
           
# return any day on any year without output file from months not completely 
# missing data
def find_all_lacking_represented_months(output_dir):
    empty_month_set = set()
    all_lacking_list = []
    
    for m in range(1, 13):
        try:
            for d in range(1, 32):
                for y in range(1945, 2020):
                    filename = os.path.join(output_dir, 'gecko_out_' 
                                        + nopad_number(y) + '-' 
                                        + nopad_number(m) + '-' 
                                        + nopad_number(d) + '.txt')
                    if os.path.isfile(filename):
                        raise ValueError
            empty_month_set.add(m)
        except ValueError:
            pass
    
    print(str(empty_month_set) + ' are the months that have not been processed')
    
    # upper bound 12 * 31 * 75 = 27900
    for m in range(1, 13):
        if m in empty_month_set:
            continue
        for d in range(1, 32):
            for y in range(1945, 2020):
                if not is_valid_day(m, d, y):
                    continue
                filename = os.path.join(output_dir, 'gecko_out_' 
                                        + nopad_number(y) + '-' 
                                        + nopad_number(m) + '-' 
                                        + nopad_number(d) + '.txt')
                if not os.path.isfile(filename):
                    all_lacking_list.append(filename)
    return all_lacking_list

# get lacking values (i.e. data not available)
def get_lacking_values(output_dir):
    lacking_list = []
    for m in range(1, 13):
        for d in range(1, 32):
            for y in range(1945, 2020):
                filename = os.path.join(output_dir, 'gecko_out_' 
                                    + nopad_number(y) + '-' 
                                    + nopad_number(m) + '-' 
                                    + nopad_number(d) + '.txt')
                if os.path.isfile(filename):
                    with open(filename) as fs:
                        lines = fs.readlines()
                    max_t = int(float(lines[0].strip()))
                    min_t = int(float(lines[1].strip()))
                    if max_t == 0 or min_t == 0:
                        lacking_list.append(filename)                  
    return lacking_list
                            
# try to find data for the data from an alternate source
def fill_lacking_values_source(list_of_records, source_name):
    if source_name == 'ncei':
        df = pd.read_csv('../data/USW00013701.csv')
        df = df[['DATE', 'TMAX', 'TMIN']]
    for rec in list_of_records:
        parts = rec.split('-')
        year = parts[0][-4:]
        month = parts[1]
        day = parts[2].split('.')[0]
        if source_name == 'weather.gov':
            rest_url = 'https://api.weather.gov/products/ec3872ba-f57e-49b2-91ca-d5e1c04f4046'
        elif source_name == 'ncei':
            date_record = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
            row = df.loc[df['DATE'] == date_record]
            if row.empty:
                print(date_record + ' has no data')
                continue
            min_temp = 1.8 * float(row['TMIN'].iloc[0]) / 10.0 + 32.0
            max_temp = 1.8 * float(row['TMAX'].iloc[0]) / 10.0 + 32.0
            if math.isnan(min_temp) or math.isnan(max_temp):
                print(date_record + ' has nan data')
                continue
            month_date = month + '-' + day            
            with open('../output/bwi_fetch_output/gecko_out_' + str(year) + '-' + month_date + '.txt', 'w', encoding='utf-8') as fs:
                fs.write(str(int(max_temp)) + '\n' + str(int(min_temp)))
        else:
            raise ValueError('Unknown Source ' + source_name)
 
def main(output_dir):
    comprehensize_list = find_all_lacking(output_dir)
    print(len(comprehensize_list))
    
    alive_list = find_all_lacking_represented_months(output_dir)
    print(len(alive_list))
    #BWI_Fetch.fetch_from_list('us/md/baltimore/KBWI', alive_list)

    lacking_list = get_lacking_values(output_dir)
    print(len(lacking_list))
    with open(os.path.join('..', 'diagnostic', 'days_with_zero.txt'), 'w') as fs:
        for ll in lacking_list:
            fs.write(ll + '\n')

    fill_lacking_values_source(lacking_list, 'ncei')

if __name__ == '__main__':
    bwi_output_dir = '../output/bwi_fetch_output'
    main(bwi_output_dir)