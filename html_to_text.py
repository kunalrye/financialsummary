'''
This script extracts plaintext from an external html document
Inputs:
    url [string] to a sec websites
Returns:
    document [string], with no processing
'''
import urllib.request
from bs4 import BeautifulSoup
import random



def html_to_text(url):
    '''
    :param url: [string] to a sec websites
    :return: document [string], with no processing
    '''
    #Pretty self explanatory, but is easier than remebering this syntax every time
    html = urllib.request.urlopen(url)
    return BeautifulSoup(html,features="html.parser").get_text()


