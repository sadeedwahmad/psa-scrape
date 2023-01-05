import csv



with open("E:/psa-scrape/pop_report/data/1999-pokemon-fossil--2023-01-04-191100.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    splitted  = str(row)
    splitted = splitted.replace("[", "")
    splitted = splitted.replace("]", "")
    
    
    splitted = splitted.split(",")
    specID = splitted[0].strip()
    cardName = splitted[1].strip()
    setName = splitted[2].strip()

   
    

    newString = "https://www.psacard.com/auctionprices/tcg-cards/" + setName + "/" + cardName + "/values/" + specID
    #newString = "".join(newString)

    newString = ''.join(i for i in newString if i not in "'")
    f = open("E:/psa-scrape/prepare_setUrls_forAuctionScrape/auctionUrls.txt", "a")
    f.write(newString + "\n")
    f.close()
print("Write complete")