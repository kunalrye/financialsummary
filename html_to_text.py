import urllib.request
from bs4 import BeautifulSoup


url = "https://www.sec.gov/Archives/edgar/data/320193/000032019318000007/a10-qq1201812302017.htm"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html)
print(soup.get_text())

