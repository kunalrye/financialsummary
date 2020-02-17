'''
Creates a text file given a 10-q url

For a given url, should output:
    sentences (good_sents [list])
    document (good_doc [string])
Includes minor pre-processing  to remove special chars
'''
import pandas as pd
import re
import random
import nltk
from nltk.collocations import *
from link_scraper import get_10qs, query_api
from html_to_text import *


def makeText(url, index):
    #Retrieve document
    document = html_to_text(url)

    #An example of retrieving sentences
    sentences = nltk.sent_tokenize(document)
    print(len(sentences))
    num_good_sents = 0
    good_sents = []
    def check_for_formatting(string):
        #Ignore sentences with annoying syntax
        #TODO: figure out how to remove backslash and maybe also remove tabs?
        regex = re.compile('[☒_☐@#^&*()<>?/\|}{~:]|\s\s')
        if(regex.search(string) == None):
            return True

    for sentence in sentences:
        if check_for_formatting(sentence):
            num_good_sents = num_good_sents+1
            good_sents.append(sentence)
            # print(sentence)

    print("Total acceptable sentences =",num_good_sents)
    #Converting the sentences to a document
    good_doc = " ".join(good_sents)
    text_file = open("txt_files/" + str(index) + ".txt", "w")
    text_file.write(good_doc)
    text_file.close()



'''
Opens every 10Q text file and reads its contents as a string. 
Returns a list of strings
'''
def txtToStrings():
    all_urls = open('links.txt').read().splitlines()
    all_docs = []
    for i in range(len(all_urls)):
        fname = "txt_files/" + str(i) + ".txt"
        with open(fname) as f:
            print(fname)
            txt_file_as_string = f.read()
        all_docs.append(txt_file_as_string)
    return all_docs




'''
Opens a specific 10Q textfile and reads its contents as a string. 
Returns a single string

Requires: 
    idx is an integer corresponding to the line number on the links.txt text file. 
    Note that idx should be 1-indexed, as 0-indexing is handled internally. 
'''
def txtToString(idx):
    fname = "txt_files/" + str(idx-1) + ".txt"
    with open(fname) as f:
        print(fname)
        txt_file_as_string = f.read()
    return txt_file_as_string




if __name__ == "main":
    random.seed(15)  # set rng seed for reproducibility
                

    #Select random 10-q from list of all
    all_urls = open('links.txt').read().splitlines()
    num_urls = len(all_urls)
    rand_url = random.randint(0, num_urls - 1)
    url = all_urls[rand_url]
    makeText(url, rand_url)





# DOESN'T work yet
# # Taken from https://stackoverflow.com/questions/2452982/how-to-extract-common-significant-phrases-from-a-series-of-text-entries
# bigram_measures = nltk.collocations.BigramAssocMeasures()
# trigram_measures = nltk.collocations.TrigramAssocMeasures()
# finder = TrigramCollocationFinder.from_words(good_doc)
# finder.apply_freq_filter(3)
# print('Best Trigrams')
# print(finder.nbest(trigram_measures.pmi, 10))
# ## For looking at sentences
# # for counter in range(5):
# #     print(sentences[3+counter])


