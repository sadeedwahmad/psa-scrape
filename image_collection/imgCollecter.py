import csv
import os
import requests


path_of_the_directory= 'E:/psa-scrape/auction_prices_realized/data'

for filename in os.listdir(path_of_the_directory):
    f = os.path.join(path_of_the_directory,filename)
    if os.path.isfile(f):
        print(":::::::::::::::::" + str(f) + ":::::::::::::::::")
        with open(f, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                print(row)
                response = requests.get(row)