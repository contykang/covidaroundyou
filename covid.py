# !/usr/bin/python3
# coding = utf-8

import csv
import requests
import sys


if __name__ == '__main__':
    #url = 'https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/21304414-1ff1-4243-a5d2-f52778048b29/download/confirmed_cases_table1_location.csv'
    #myfile = requests.get(url)

    #filename = 'rawcovid.csv'
    
    #with open(filename, 'wb') as output_file:
        #output_file.write(myfile.content)

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

