'''
Created November, 2020

This takes data fetech from BWI_Fetch and extracts the min and max values for
each date in a predicatable fashion.  By iterating over this feteched data,
we are able to calculate the max and min for each day over a course of a 
number of years

@author: Mendy
'''

import os

def process(file_in_directory, file_out_directory):

    files = os.listdir(file_in_directory)
    
    for month in range(1,13):
        for day in range(1,32):
    
            md = str(month) + '-' + str(day)
    
            print('Processing ' + md)
    
            total_max_days = 0
            total_min_days = 0
            running_max = 0
            running_min = 0
        
            output_summary = os.path.join(file_out_directory, md + '_maxmin.txt')
        
            for f in files:
                if not f.endswith('-' + md + '.txt'):
                    continue    
                with open(os.path.join(file_in_directory, f)) as fs:
                    lines = fs.readlines()
                maxt = int(lines[0].strip())
                mint = int(lines[1].strip())
                print(str(maxt) + ',' + str(mint))
                # a value of 0 may indicate missing data for that day
                if maxt != 0:
                    total_max_days += 1
                    running_max += maxt
                if mint != 0:
                    total_min_days += 1
                    running_min += mint

            if total_max_days == 0 and total_min_days == 0:
                continue
                    
            final_max_avg = running_max / total_max_days
            final_min_avg = running_min / total_min_days
        
            with open(output_summary, 'w') as fs:
                fs.write('Final max average ' + str(final_max_avg) + '\n')
                fs.write('Final min average ' + str(final_min_avg) + '\n')

if __name__ == '__main__':
    file_input_directory = '../output/bwi_fetch_output'
    file_output_directory = '../output/process_weather_data_output'
    process(file_input_directory, file_output_directory)