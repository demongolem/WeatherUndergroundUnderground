'''
Created on Dec 10, 2020

Fetch the max and min extremes from data created by ProcessWeatherData

@author: Mendy
'''

import datetime
import os

def file_date(raw_string):
    return raw_string[:-11]

def max_min_from_file(output_dir, f):
    if f is None:
        with open(output_dir) as fs:
            lines = fs.readlines()
    elif output_dir is None:
        with open(f) as fs:
            lines = fs.readlines()
    else:
        with open(os.path.join(output_dir, f)) as fs:
            lines = fs.readlines()
    max_value = float(lines[0][18:].strip())
    min_value = float(lines[1][18:].strip())
    return (max_value, min_value)

def fetch_extremes(output_dir):
    max_max_temp = -1000
    max_max_date = 'Never'
    min_max_temp = 1000
    min_max_date = 'Never'
    max_min_temp = -1000
    max_min_date = 'Never'
    min_min_temp = 1000
    min_min_date = 'Never'
    
    for f in os.listdir(output_dir):
        if 'maxmin' not in f:
            continue
        x_value = file_date(f)
        y_values = max_min_from_file(output_dir, f)
        
        this_max_value = y_values[0]
        this_min_value = y_values[1]
        
        if this_max_value > max_max_temp:
            max_max_date = x_value
            max_max_temp = this_max_value

        if this_max_value < min_max_temp:
            min_max_date = x_value
            min_max_temp = this_max_value
        
        if this_min_value < min_min_temp:
            min_min_date = x_value
            min_min_temp = this_min_value           

        if this_min_value > max_min_temp:
            max_min_date = x_value
            max_min_temp = this_min_value           

    return ((min_min_date, min_min_temp),(max_min_date, max_min_temp),(min_max_date, min_max_temp), (max_max_date, max_max_temp))
 
def main():
    output_dir = '../output/process_weather_data_output'
    (min_min_values, max_min_values, min_max_values, max_max_values) = fetch_extremes(output_dir)
    min_min_date = min_min_values[0]
    min_min_temp = min_min_values[1]
    max_min_date = max_min_values[0]
    max_min_temp = max_min_values[1]
    min_max_date = min_max_values[0]
    min_max_temp = min_max_values[1]
    max_max_date = max_max_values[0]
    max_max_temp = max_max_values[1]

    dt = datetime.datetime.now()
    today_date= f'{dt.month}-{dt.day}-{dt.year}'
    relevant_file = '-'.join(today_date.split('-')[0:2]) + '_maxmin.txt'
    (max_today_temp, min_today_temp) = max_min_from_file(output_dir, relevant_file)

    print('Coldest')
    print(str(min_min_date) + ' : ' + str(min_min_temp))
    print(str(min_max_date) + ' : ' + str(min_max_temp))
    print('Warmest')
    print(str(max_min_date) + ' : ' + str(max_min_temp))
    print(str(max_max_date) + ' : ' + str(max_max_temp))
    print('Today')
    print(str(today_date) + ' : ' + str(max_today_temp))
    print(str(today_date) + ' : ' + str(min_today_temp))

if __name__ == '__main__':
    main()