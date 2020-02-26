"""
Test script to explore getting text data from xbrl files

Good reference document: https://www.codeproject.com/Articles/1227765/Parsing-XBRL-with-Python
"""
import requests
from bs4 import BeautifulSoup
import re

# Obtain XBRL text from Disney's xbrl
xbrl_link = "https://www.sec.gov/Archives/edgar/data/1001039/000100103918000235/wf-form4_154544051056009.xml"
xbrl_resp = requests.get(xbrl_link)
xbrl_str = xbrl_resp.text

soup = BeautifulSoup(xbrl_str, 'html.parser')
tag_list = soup.find_all()
#vprint(tag_list) ## can't seem to find anything useful in tag list


# this returns just the relevant text without the nasty tags
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


print(cleanhtml(xbrl_str))

