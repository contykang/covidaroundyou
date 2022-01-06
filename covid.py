# !/usr/bin/python3
# coding = utf-8

import csv
import requests
import sys
import os
from datetime import datetime


if __name__ == '__main__':

    
    filename = 'rawcovid.csv'
    time = datetime.fromtimestamp(int(os.path.getmtime(filename))).strftime('%Y-%m-%d')
    now = datetime.now().strftime('%Y-%m-%d')

    if time != now:
        print("Need to download the new data now...\n")
        url = 'https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/21304414-1ff1-4243-a5d2-f52778048b29/download/confirmed_cases_table1_location.csv'
        myfile = requests.get(url)

        with open(filename, 'wb') as output_file:
            output_file.write(myfile.content)
    else:
        print("No new data, keep processing...\n")
        with open('rawcovid.csv', newline='') as csvfile:
            datareader = csv.reader(csvfile)

            thisDate = ''
            thisCount = 0

            for row in datareader:
                if len(sys.argv) > 1:
                    if row[1] == sys.argv[1]:
                        if thisDate != row[0]:
                            if thisDate != '':
                                print(thisDate, thisCount)
                            thisDate = row[0]
                            thisCount = 1
                        else:
                            thisCount += 1
                else:
                    if thisDate != row[0]:
                        if thisDate != '':
                            print(thisDate, thisCount)
                        thisDate = row[0]
                        thisCount = 1
                    else:
                        thisCount += 1

