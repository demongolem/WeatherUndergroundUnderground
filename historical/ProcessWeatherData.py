import os

def process(file_directory):

    files = os.listdir(file_directory)
    
    for month in range(1,13):
        for day in range(1,32):
    
            md = str(month) + '-' + str(day)
    
            print('Processing ' + md)
    
            total_max_days = 0
            total_min_days = 0
            running_max = 0
            running_min = 0
        
            output_summary = '../output/' + md + '_maxmin.txt'
        
            for f in files:
                if not f.endswith('-' + md + '.txt'):
                    continue    
                with open(os.path.join(file_directory, f)) as fs:
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
    file_directory = '../output'
    process(file_directory)