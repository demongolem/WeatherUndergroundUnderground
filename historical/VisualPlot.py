'''
Created on Dec 10, 2020

@author: Mendy
'''

import matplotlib.pyplot as plt
import os
import datetime

#example gecko_out_2019-12-7.txt
def day_of_year(raw_string):
    datemonth = raw_string[:-11]
    mth = int(datemonth.split('-')[0])
    dy = int(datemonth.split('-')[1])
    ly = 2020
    dt = datetime.datetime(ly, mth, dy, 0, 0, 0)
    doy = dt.timetuple().tm_yday
    return doy

def max_min_from_file(output_dir, f):
    with open(os.path.join(output_dir, f)) as fs:
        lines = fs.readlines()
    max_value = float(lines[0][18:].strip())
    min_value = float(lines[1][18:].strip())
    return (max_value, min_value)

def plot_output(output_dir):
    fig, ax = plt.subplots(ncols=2)  # Create a figure containing a single axes.
    files = os.listdir(output_dir)
    x_data = []
    y_max_data = []
    y_min_data = []
    for f in files:
        if 'maxmin' not in f:
            continue
        x_value = day_of_year(f)
        y_values = max_min_from_file(output_dir, f)
        x_data.append(x_value)
        y_max_data.append(y_values[0])
        y_min_data.append(y_values[1])
    x_data, y_max_data, y_min_data = map(list, zip(*sorted(zip(x_data, y_max_data, y_min_data))))        
    ax[0].plot(x_data, y_max_data)
    ax[1].plot(x_data, y_min_data)
    plt.show()

def main():
    output_dir = '../output'
    plot_output(output_dir)

if __name__ == '__main__':
    main()