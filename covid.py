# !/usr/bin/python3
# coding = utf-8
# Created by Conty Kang
# License: MIT

import csv
import requests
import sys
import os
import re
from datetime import datetime


def download_csv(file_name):
    """
    This function will download the raw data file form NSW Health website.

    :param file_name: The output file name to save the raw data
    :return: None
    """
    url = 'https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/' \
              '5d63b527-e2b8-4c42-ad6f-677f14433520/download/confirmed_cases_table1_location_agg.csv'
    my_file = requests.get(url)

    with open(file_name, 'wb') as output_file:
        output_file.write(my_file.content)


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
        data_reader = csv.reader(csvfile)
        result = dict()
        for row in data_reader:
            if row[0] == 'notification_date':
                continue
            if postcode == 0:
                # Need to process all data for the whole state
                if row[0] not in result:
                    result[row[0]] = 0
                result[row[0]] += int(row[7])
            else:
                if postcode in row[1]:
                    if row[0] not in result:
                        result[row[0]] = 0
                    result[row[0]] += int(row[7])
    return result


if __name__ == '__main__':
    postcode_pattern = re.compile(r'^2\d{3}$')

    if len(sys.argv) == 1:
        # No postcode, export all result for whole NSW
        output = 'covidcount_NSW.csv'
        res = main(0)
    elif len(sys.argv) == 2 and re.findall(postcode_pattern, sys.argv[1]):
        # Postcode provided
        print(f'Now processing the data for {re.findall(postcode_pattern, sys.argv[1])[0]}.')
        output = 'covidcount_' + sys.argv[1] + '.csv'
        res = main(sys.argv[1])
    else:
        print("Too many arguments! The argument should be a valid postcode (4 digis beginning with 2)")
        sys.exit(0)

    with open(output, 'w') as file:
        pass

    for date in res:
        add_row = [date, res[date]]
        with open(output, 'a+') as out:
            write = csv.writer(out)
            write.writerow(add_row)
