'''
Created on Dec 11, 2020

@author: Mendy
'''

import os

def main(output_dir):
    for f in os.listdir(output_dir):
        print(f)

if __name__ == '__main__':
    output_dir = ''
    main(output_dir)