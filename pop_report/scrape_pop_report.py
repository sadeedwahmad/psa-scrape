import os
import sys
import time
import math
import requests
import pandas as pd

PAGE_MAX = 300
POP_URL_BASE = "https://www.psacard.com/Pop/GetSetItems"
EXAMPLE_URL = "https://www.psacard.com/pop/baseball-cards/2018/topps-update/161401"



class PsaPopReport:
    def __init__(self, pop_url, set_name):
        self.pop_url = pop_url
        self.set_name = set_name

    def scrape(self):
        print("collecting data for {}".format(self.set_name))

        # Pull the set ID off the input url
        try:
            set_id = int(self.pop_url.split("/")[-1])
        except:
            print("Input URL should end in a numeric value, it should look like this: {}".format(EXAMPLE_URL))
            return None

        # Get json data for input set
        sess = requests.Session()
        sess.mount("https://", requests.adapters.HTTPAdapter(max_retries=5))
        form_data = {
            "headingID": str(set_id),
            "categoryID": "20019",
            "draw": 1,
            "start": 0,
            "length": 500,
            "isPSADNA": "false"
        }

        try:
            json_data = self.post_to_url(sess, form_data)
        except Exception as err:
            print("Error pulling data for {}, with error: {}".format(self.set_name, err))
        cards = json_data["data"]
    
        
        # If there's more than PAGE_MAX results, keep calling the scrape url until we have all of the card records
        total_cards = json_data["recordsTotal"]
        if total_cards > PAGE_MAX:
            additional_pages = math.ceil((total_cards - PAGE_MAX) / PAGE_MAX)
            for i in range(additional_pages):
                curr_page = i + 1
                form_data = {
                    "headingID": str(set_id),
                    "categoryID": "20019",
                    "draw": curr_page + 2,
                    "start": PAGE_MAX * curr_page,
                    "length": PAGE_MAX,
                    "isPSADNA": "false"
                }

                json_data = self.post_to_url(sess, form_data)
                cards += json_data["data"]
        

       

        #dictCards = cards
        #print("dictcards type")
        #print(type(dictCards))
        
        for crds in cards:
            del crds['SortOrder']
            del crds['Variety']
        
            del crds[ 'CardNumber' ]
            del crds['CardNumberSort'  ]

            del crds['GradeN0']
            del crds['Grade1Q'  ]
            del crds[  'Grade1']
            del crds[ 'Grade1_5Q' ]
            del crds[ 'Grade1_5' ]
            del crds[  'Grade2Q']

            del crds['Grade2'  ]
            del crds[ 'Grade2_5' ]
            del crds[  'Grade3Q']
            del crds[ 'Grade3' ]
            del crds[ 'Grade3_5']
            del crds[ 'Grade4Q' ]


            del crds[ 'Grade4' ]
            del crds[ 'Grade4_5' ]
            del crds[ 'Grade5Q' ]
            del crds[ 'Grade5' ]
            del crds[ 'Grade5_5' ]
            del crds[ 'Grade6Q'  ]
            del crds[  'Grade6']
            del crds[  'Grade6_5']
            
            del crds[  'Grade7Q']
            del crds[ 'Grade7' ]
            del crds[ 'Grade7_5' ]
            del crds[  'Grade8Q']

            del crds[  'Grade8']
            del crds[ 'Grade8_5' ]
            del crds[ 'Grade9Q' ]
            del crds[ 'Grade9' ]
            del crds[ 'Grade10' ]
            del crds[ 'Total' ]

            del crds[ 'GradeTotal' ]
            del crds[ 'HalfGradeTotal' ]
            del crds[ 'QualifiedGradeTotal' ]
            crds['SetName'] = set_name
            print(crds)
        
        #    print("type element in cards")
        #    print(type(x))
            #print(x['SubjectName'])
            #print(x['SpecID'])
            #print(set_name)
        #    tmp  = {'SubjectName':x['SubjectName'],
       #            'SpecID': x['SpecID'],
       #           'SetName' : set_name }
           
            #tmp = [x['SubjectName'], x['SpecID'],set_name]
        #    dictCards += tmp
        #    print(tmp)
        #    print("type element of tmp")
        #    print(type(tmp))
        #    #print(type(tmpDict)) 
            

        # Create a dataframe
        df = pd.DataFrame(cards[1:])
        #df = pd.DataFrame(dictCards[1:])
        #df = pd.DataFrame(dictCards)
        # Write to csv
        df.to_csv(self.get_file_name(), index = False)

    def post_to_url(self, session, form_data):
        r = session.post(POP_URL_BASE, data=form_data)
        r.raise_for_status()
        json_data = r.json()
        time.sleep(3)
        return json_data

    def get_file_name(self):
        f_name = "{}--{}".format(self.set_name.replace(" ", "-"), str(time.strftime("%Y-%m-%d-%H%M%S")))
        return "{}.csv".format(os.path.join("data", f_name))

if __name__ == '__main__':
    # Input validation
    try:
        input_url = [sys.argv[1]]
        if not input_url or not isinstance(input_url, str):
            raise ValueError("input must be a url string with base '{}'".format(POP_URL_BASE))
    except IndexError:
        # If no input url provided, read in urls from urls.txt
        if not os.path.exists("urls.txt"):
            raise ValueError("no input url passed and 'urls.txt' not found")
        with open("urls.txt") as f:
            urls_raw = [n for n in f.read().split("\n") if n]

    urls = {}
    for line in urls_raw:
        elems = [n.strip() for n in line.split("|")]
        if len(elems) == 2:
            urls[elems[0]] = elems[1]
        elif len(elems) == 1:
            urls[elems[0]] = elems[0]
        else:
            raise ValueError("Malformed txt line:\n{}\nLines should be two pipe-separated elements, like this:\n" \
                             "2018 Topps Update baseball | https://www.psacard.com/pop/baseball-cards/2018/topps-update/161401")

    # If psa-scrape/data doesn't exist, create it
    if not os.path.exists("data"):
        os.makedirs("data")

    # Iterate over all urls
    for set_name, url in urls.items():
        # Initialize class and execute web scraping
        ppr = PsaPopReport(url, set_name)
        ppr.scrape()

print("Code Completed :: " + str(set_name))