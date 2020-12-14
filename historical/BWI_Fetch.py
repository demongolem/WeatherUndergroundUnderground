import os
import re
from selenium import webdriver
import sys
import time

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

os.environ['MOZ_HEADLESS'] = '1'

temp_regex = r'\>(\-?[0-9]+)\<'

def main(city, start_month, end_month, start_day, end_day, start_year, end_year):
    if start_month != end_month:
        print('Multiple months currently not supported')
        return

    for cday in range(start_day, end_day + 1):
        month_date = str(start_month) + '-' + str(cday)
    
        for y in range(start_year, end_year - 1, -1):        
            driver = webdriver.Firefox(executable_path="C:/Users/hgusi/eclipse-workspace/WeatherUndergroundUnderground/historical/geckodriver")
        
            city_url = 'https://www.wunderground.com/history/daily/' + city + '/date/' + str(y) + '-' + month_date
    
            print(city_url)
    
            while True:
                try:
                    driver.get(city_url);
                    time.sleep(12)
                    break
                except:
                    time.sleep(12)
            page_source = driver.page_source
            
            begin_index = page_source.index('High Temp')
            end_index = page_source.index('Day Average Temp')
            interesting_string = page_source[begin_index:end_index]
     
            match_list = re.findall(temp_regex, interesting_string)
            
            with open('../output/gecko_out_' + str(y) + '-' + month_date + '.txt', 'w', encoding='utf-8') as fs:
                fs.write(match_list[0] + '\n' + match_list[3])
            
            driver.close()

if __name__ == '__main__':
    city = 'us/md/baltimore/KBWI'
    start_month = 1
    end_month = 1
    start_day = 24
    end_day = 31
    start_year = 2019
    end_year = 1945
    main(city, start_month, end_month, start_day, end_day, start_year, end_year)