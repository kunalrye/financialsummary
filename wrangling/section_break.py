''' 
Functions to extract the sections from a 10Q report, such as "Management's Discussion and Analysis of Financial Condition and Results of Operations", 
"Controls and Procedures", etc. 
'''

from wrangling.retrieve_sentences import unfilteredTxtToStrings, html_to_text
import re


section_headers = [
    r"Item(\s{0,3})1(\..{0,30}\s*|:\s*)Financial Statements",
    r"ITEM 2\.\s*MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS",
    r"ITEM 3\.\s*QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK",
    r"ITEM 4\.\s*CONTROLS AND PROCEDURES",
    r"ITEM 1\.\s*LEGAL PROCEEDINGS",
    r"ITEM 1A\.\s*RISK FACTORS",
    r"ITEM 2\.\s*UNREGISTERED SALES OF EQUITY SECURITIES AND USE OF PROCEEDS",
    r"ITEM 6\.\s*EXHIBITS"
]


### TESTING FUNCTION MODIFICATIONS ####

def check_for_formatting(string):
    """Simple format check for sentences 
    
    Arguments:
        string {String} -- the sentence to be checked 
    
    Returns:
        Boolean -- whether the sentence passes the regex test 
    """
    #Ignore sentences with annoying syntax
    #TODO: figure out how to remove backslash and maybe also remove tabs?
    regex = re.compile(r'[☒_☐@#^&*()<>?/\|}{~:]|\s\s')
    if(regex.search(string) == None):
        return True

def unfilteredText(url, index):
    """
    Gets the text from a specified url, does basic sentence processing 
    to remove malformed sentences, and writes the contents to a 
    text file 
    
    Arguments:
        url {string} -- web url to 10Q
        index {} -- 1-indexed index of url in the links.txt file 
    
    Returns:
        Nothing -> writes to a text file 
    """
    #Retrieve document
    doc = html_to_text(url)
    doc = doc.replace(u'\xa0', u' ')
    doc = doc.replace(u'\u2019', u'\u0027')
    text_file = open("resources/unfiltered/" + str(index) + ".txt", "w")
    text_file.write(doc)
    text_file.close()



def allUnfilteredText():
    all_urls = open('links.txt').read().splitlines()
    for i, url in enumerate(all_urls):
        print(i)
        unfilteredText(url, i) ## 1 for 1-indexed function argument requirement 
    

def checkHeader(pattern, doc, idx, header_num):
    res = re.findall(pattern, doc, re.IGNORECASE)
    if len(res) < 1:
        print("doc " + str(idx+1) + " has " + str(len(res)) + " matches")
        return False
    return True



if __name__ == "__main__":

    # getText("https://www.sec.gov/Archives/edgar/data/749251/000074925118000008/a03312018-10q.htm", 99)
    # getText("https://www.sec.gov/Archives/edgar/data/1262039/000126203918000019/ftnt-0331201810xq.htm", 75)    

    # pattern = section_headers[1]
    # print(pattern)
    # print(str(re.findall(pattern, doc, re.IGNORECASE)))


    all_docs = unfilteredTxtToStrings()
    num_match = 0
    for i in range(187):
        for num, header in enumerate(section_headers[1:2]):
            print(header)
            num_match =  num_match + 1 if checkHeader(header, all_docs[i], i, num) else num_match

    print(num_match)
    