# !/usr/bin/python3
# coding = utf-8
# Created by Conty Kang
# License: MIT

import csv
import requests
import sys
import os
from datetime import datetime


def download_csv(file_name):
    url = 'https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/21304414-1ff1-4243-a5d2' \
          '-f52778048b29/download/confirmed_cases_table1_location.csv '
    my_file = requests.get(url)

    with open(file_name, 'wb') as output_file:
        output_file.write(my_file.content)


def output_csv(file_name, date, count):
    # Export the data to a single CSV file for further process

    with open(file_name, 'a') as out_csv:
        add_row = [date, count]
        write = csv.writer(out_csv)
        write.writerow(add_row)


def main(postcode):
    filename = 'raw_covid.csv'
    # Check if the raw_covid.csv file exist (mainly for the first time running the script). Create one empty file if not
    # exist then download the latest data.

    if os.path.isfile('raw_covid.csv') is False:
        open(filename, 'w+').close()
        print("Initializing the data...")
        download_csv(filename)

    # Get the last modified date of the file "rawcovid" to see if we need to download the latest version of the file or
    # not.

    time = datetime.fromtimestamp(int(os.path.getmtime(filename))).strftime('%Y-%m-%d')
    now = datetime.now().strftime('%Y-%m-%d')

    if time != now:
        print("Need to download the new data now...")
        download_csv(filename)
    else:
        print("No new data, keep processing...")

    # Start importing data from csv file and calculate the total case number at each day.
    with open('raw_covid.csv', newline='') as csvfile:
        datareader = csv.reader(csvfile)

        thisDate = ''
        thisCount = 0

        # Create a new output file every time before writing the new data into the file.
        if len(sys.argv) > 1:
            output = "covidcount_" + sys.argv[1] + ".csv"
            open(output, 'w+').close()
        else:
            output = "covidcount_NSW.csv"
            open(output, 'w+').close()

        # Start parsing the data
        for row in datareader:
            if len(sys.argv) > 1:
                if row[1] == sys.argv[1]:
                    if this_date != row[0]:
                        if this_date != '':
                            print(this_date, this_count)
                            output_csv(output, this_date, this_count)
                        this_date = row[0]
                        this_count = 1
                    else:
                        thisCount += 1
            else:
                if thisDate != row[0]:
                    if thisDate != '':
                        print(thisDate, thisCount)
                        output_csv(output, this_date, this_count)
                    this_date = row[0]
                    this_count = 1
                else:
                    this_count += 1


if __name__ == '__main__':
    postcode = sys.argv[1]
    main(postcode)
