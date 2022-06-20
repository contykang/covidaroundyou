# covidhere

This is a Python3 script to calculate the local COVID-19 case number for NSW Australia by postcode.

Usage:

python3 covid.py <POST_CODE>

For example: python3 covid.py 2000

If no post code given, all the cases in NSW will be shown.

~~Source is from NSW Health website:~~

~~https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/21304414-1ff1-4243-a5d2-f52778048b29/download/confirmed_cases_table1_location.csv~~

~~This datasource will not be used anymore for the script.~~

Since 2022-01-25, a new aggregated data source provided by NSW Health as below:

https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/5d63b527-e2b8-4c42-ad6f-677f14433520/download/confirmed_cases_table1_location_agg.csv

Since 2022-01-20, the everyday records have been divided into two groups: "Confirmed by RAT" and "Confirmed by PCR".

Result will be saved to a local CSV file:
 - If no postcode provided, file name would be "covidcount_NSW.csv"
 - If postcode provided, file name would be "covidcount_<POST_CODE>.csv"