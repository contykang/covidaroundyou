# !/usr/bin/python3
# coding = utf-8

import csv
import requests
import sys
import os
from datetime import datetime

def downloadCsv(filename):
        url = 'https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/21304414-1ff1-4243-a5d2-f52778048b29/download/confirmed_cases_table1_location.csv'
        myfile = requests.get(url)

        with open(filename, 'wb') as output_file:
            output_file.write(myfile.content)


def outputCsv(filename, thisDate, thisCount):
    # Export the data to a single CSV file for further process

    with open (filename, 'a') as ocsv:
        addrow = [thisDate, thisCount]
        write = csv.writer(ocsv)
        write.writerow(addrow)


if __name__ == '__main__':

    filename = 'rawcovid.csv'    

    # Check if the rawcovid.csv file exist (mainly for the first time running the script). Create one empty file if not exist then download the latest data.

    if os.path.isfile('rawcovid.csv') is False:
        open(filename, 'w+').close()
        print("Initilizign the data...")
        downloadCsv(filename)


    # Get the last modified date of the file "rawcovid" to see if we need to download a latest version of the file or not.

    time = datetime.fromtimestamp(int(os.path.getmtime(filename))).strftime('%Y-%m-%d')
    now = datetime.now().strftime('%Y-%m-%d')

    if time != now:
        print("Need to download the new data now...\n")
        downloadCsv(filename)
    else:
        print("No new data, keep processing...\n")
    
    # Start importing data from csv file and calculate the total case number at each day.
    with open('rawcovid.csv', newline='') as csvfile:
        datareader = csv.reader(csvfile)

        thisDate = ''
        thisCount = 0

        for row in datareader:
            if len(sys.argv) > 1:
                output = "covidcount_" + sys.argv[1] + ".csv"
                if row[1] == sys.argv[1]:
                    if thisDate != row[0]:
                        if thisDate != '':
                            print(thisDate, thisCount)
                            outputCsv(output, thisDate, thisCount)
                        thisDate = row[0]
                        thisCount = 1
                    else:
                        thisCount += 1
            else:
                output = "covidcount_NSW.csv"
                if thisDate != row[0]:
                    if thisDate != '':
                        print(thisDate, thisCount)
                        outputCsv(output, thisDate, thisCount)
                    thisDate = row[0]
                    thisCount = 1
                else:
                    thisCount += 1




