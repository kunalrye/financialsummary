##########################
# Script to query for 10Q reports for a specific company via cik, 
# then forms a new url to directly access 10Q report 
##########################
import pandas as pd
from wrangling.link_scraper import get_10qs, query_api


#Request timed out at verisign INC
###### QUERY PARAMETERS ######
# specify query dates in form of YYYY-MM-DD
date_from = "2018-01-01"
date_to = "2018-12-31"

# cik of company to look up
#Read the NCT csv
NCTdf = pd.read_csv('resources/TechStocks_NameCIKTicker.csv')
#find total number of stocks
tot_stocks = len(NCTdf.index)
#Set a list of what has been queried
NCTdf['Queried'] = 0
#Set a list of valid companies 1 if valid 0 if not
NCTdf['Valid and Queried']=0

#open links.txt and see what urls we have
prev_links = open('resources/links.txt').read().splitlines()
#Make note of all current companies that are on our list atm.
current_companies = []
#iterate over CIK and add the text to the txt file
for stock_idx in range(tot_stocks):
    #get cik
    print(f"Generating urls for {NCTdf['CompanyName'][stock_idx]} ({stock_idx+1}/{tot_stocks})")
    cik = NCTdf['CIK'][stock_idx]
    #get urls as a set of links if the stock has not been queried
    if  NCTdf['Queried'][stock_idx] == 0:
        NCTdf['Queried'][stock_idx] = 1 #yes, it has been queried
        try: #just incase the api runs out of calls (didnt happen tho)
            links = get_10qs(query_api(cik, date_from, date_to))
            if len(links)>0:
                current_companies.append(NCTdf['CompanyName'][stock_idx])
                with open('links.txt', 'a') as f:
                    NCTdf['Valid and Queried'][stock_idx] = 1 + NCTdf['Valid and Queried'][stock_idx]
                    for link in links:
                        if link not in prev_links:
                            f.write("%s\n" % link)
                        else:
                            print(f"{NCTdf['CompanyName'][stock_idx]} already transcribed!")
        except:
            NCTdf.to_csv('resources/TechStocks_NameCIKTickerQuery.csv')

#save the list of what has been queried
NCTdf.to_csv('resources/TechStocks_NameCIKTickerQuery.csv')