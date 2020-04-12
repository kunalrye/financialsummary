'''
Functions to: 
    Retrieve text from url 
    Creates a text file given a 10-q url

For a given url, should output:
    sentences (good_sents [list])
    document (good_doc [string])
Includes minor pre-processing  to remove special chars
'''
import re
import random
import nltk
import urllib.request
from bs4 import BeautifulSoup


def html_to_text(url):
    '''
    :param url: [string] to a sec websites
    :return: document [string], with no processing
    '''
    #Pretty self explanatory, but is easier than remebering this syntax every time
    html = urllib.request.urlopen(url)
    return BeautifulSoup(html,features="html.parser").get_text()


def makeText(url, index):
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
    document = html_to_text(url)

    #An example of retrieving sentences
    sentences = nltk.sent_tokenize(document)
    print(len(sentences))
    num_good_sents = 0
    good_sents = []
    def check_for_formatting(string):
        """Simple format check for sentences 
        
        Arguments:
            string {String} -- the sentence to be checked 
        
        Returns:
            Boolean -- whether the sentence passes the regex test 
        """
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
    text_file = open("resources/filtered/" + str(index - 1) + ".txt", "w",encoding='utf-8')
    text_file.write(good_doc)
    text_file.close()




def txtToStrings():
    """Opens every filtered 10Q text file and reads its contents as a string. 
    
    Returns:
        List<String> -- List of strings, where each string corresopnds to the filtered text of a 10Q
    """
    all_urls = open('resources/links.txt',encoding='utf-8').read().splitlines()
    all_docs = []
    for i in range(len(all_urls)):
        fname = "resources/filtered/" + str(i) + ".txt"
        with open(fname,encoding="utf-8") as f:
            print(fname)
            txt_file_as_string = f.read()
        all_docs.append(txt_file_as_string)
    return all_docs





def txtToString(idx):
    """Opens a specific 10Q textfile and reads its contents as a string. 
    Returns a single string
    
    Arguments:
        idx {int} -- int corresponding to the line number on the links.txt text file. 
        Note that idx should be 1-indexed, as 0-indexing is handled internally. 
    
    Returns:
        [string] -- the contents of the filtered 10Q text file 
    """
    
    fname = "resources/filtered/" + str(idx-1) + ".txt"
    with open(fname,encoding='utf-8') as f:
        print(fname)
        txt_file_as_string = f.read()
    return txt_file_as_string



def unfilteredTxtToStrings():
    """Opens every unfiltered 10Q text file and reads its contents as a string. 
    
    Returns:
        List<String> -- List of strings, where each string corresopnds to the unfiltered text of a 10Q
    """
    all_urls = open('resources/links.txt',encoding='utf-8').read().splitlines()
    all_docs = []
    for i in range(len(all_urls)):
        fname = "resources/unfiltered/" + str(i) + ".txt"
        with open(fname,encoding='utf-8') as f:
            print(fname)
            txt_file_as_string = f.read()
        all_docs.append(txt_file_as_string)
    return all_docs



def unfilteredTxtToString(idx):
    """Opens a specific unfiltered 10Q textfile and reads its contents as a string. 
    Returns a single string
    
    Arguments:
        idx {int} -- int corresponding to the line number on the links.txt text file. 
        Note that idx should be 1-indexed, as 0-indexing is handled internally. 

    Returns:
        [string] -- the contents of the unfiltered 10Q text file 
    """
    
    fname = "resources/unfiltered/" + str(idx-1) + ".txt"
    with open(fname,encoding='utf-8') as f:
        print(fname)
        txt_file_as_string = f.read()
    return txt_file_as_string

if __name__ == "main":
    random.seed(15)  # set rng seed for reproducibility

    #Select random 10-q from list of all
    all_urls = open('resources/links.txt',encoding='utf-8').read().splitlines()
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


