import csv
import os
import requests


import urllib.request

from PIL import Image



path_of_the_directory= "/Users/sadeedahmad/Desktop/psa-scrape/data"

for filename in os.listdir(path_of_the_directory):
    f = os.path.join(path_of_the_directory,filename)
    if os.path.isfile(f):
        print(":::::::::::::::::" + str(f) + ":::::::::::::::::")
        with open(f, 'r') as file:
            csvreader = csv.reader(file)
            counter =0
            for row in csvreader:
                #print(row)
                #print(type(row))
                #print(row[0])
                row = row[0]
                #print(row)
                #print(type(row)) TYPE String
                if row != "img_url":
                    res = requests.get(row).content
                    if counter<10:
                        of_p  = "/Users/sadeedahmad/Desktop/psa-scrape/image_collection/imgs/img_" + str(counter) + ".jpg"
                        
                        with open(of_p, "wb") as of:
                            of.write(res)
                            counter +=1
                
print("Image collector done")
                