##########################
# Script to query for 10Q reports for a specific company via cik, 
# then forms a new url to directly access 10Q report 
##########################

from link_scraper import get_10qs, query_api

###### QUERY PARAMETERS ######
# cik of compay to look up
cik = 320193 
# dates in form of YYYY-MM-DD
date_from = "2018-01-01"
date_to = "2018-12-31"
links = get_10qs(query_api(cik, date_from, date_to))

## write the links to a txt file, separated by newlines 
with open('links.txt', 'w') as f:
  for link in links:
      f.write("%s\n" % link)






