'''
Created October, 2020

This fetches min and max values over a certain range of dates from the Weather
Underground website.  Because the API is pay, we have to do web scraping to
get at the data we need.  There needs to be a timeout in place to handle
the Javscript construction of the queried data. 

@author: Mendy
'''

import os
import re
from selenium import webdriver
import sys
import time

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

os.environ['MOZ_HEADLESS'] = '1'

temp_regex = r'\>(\-?[0-9]+)\<'

SLEEP_TIMEOUT = 12

def perform_single_fetch(city, month_date, y):
    driver = webdriver.Firefox(executable_path="C:/Users/hgusi/eclipse-workspace/WeatherUndergroundUnderground/historical/geckodriver")

    city_url = 'https://www.wunderground.com/history/daily/' + city + '/date/' + str(y) + '-' + month_date

    print(city_url)

    while True:
        try:
            driver.get(city_url);
            time.sleep(SLEEP_TIMEOUT)
            break
        except:
            time.sleep(SLEEP_TIMEOUT)
    page_source = driver.page_source
    
    try:
        begin_index = page_source.index('High Temp')
        end_index = page_source.index('Day Average Temp')
        interesting_string = page_source[begin_index:end_index]
 
        match_list = re.findall(temp_regex, interesting_string)
        
        with open('../output/bwi_fetch_output/gecko_out_' + str(y) + '-' + month_date + '.txt', 'w', encoding='utf-8') as fs:
            fs.write(match_list[0] + '\n' + match_list[3])
    except:
        print('No data for that day')
        with open('../output/bwi_fetch_output/gecko_out_' + str(y) + '-' + month_date + '.txt', 'w', encoding='utf-8') as fs:
            fs.write("0" + '\n' + "0") 
    
    driver.close()

def fetch_from_list(city, query_dates):
    for qd in query_dates:        
        date_parts = qd.split('-')
        month_date = date_parts[1] + '-' + date_parts[2][0:-4]
        y = date_parts[0][-4:]
        perform_single_fetch(city, month_date, y)

def fetch_range(city, start_month, end_month, start_day, end_day, start_year, end_year):
    if start_month != end_month:
        print('Multiple months currently not supported')
        return

    for cday in range(start_day, end_day + 1):
        month_date = str(start_month) + '-' + str(cday)
    
        for y in range(start_year, end_year - 1, -1):   
            perform_single_fetch(city, month_date, y)     

if __name__ == '__main__':
    city = 'us/md/baltimore/KBWI'
    start_month = 4
    end_month = 4
    start_day = 1
    end_day = 30
    start_year = 2019
    end_year = 1945
    fetch_range(city, start_month, end_month, start_day, end_day, start_year, end_year)