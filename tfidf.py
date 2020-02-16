'''
Computes the TF-IDF matrix and the top-n words from the corpus of 187 documents
Requires: subdirectory txt_files containing the text files of the 10-Qs
'''

from retrieve_sentences import makeText
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd 
from yellowbrick.text import TSNEVisualizer
from yellowbrick.datasets import load_hobbies

## words to exclude from the TFIDF matrix 
ENGLISH_STOP_WORDS = [
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves"]



def linksToTxt():
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
Requires: 'docs' is a list of strings, where each string is the plain text of the 10Q

Returns: TFIDF matrix, list of feature names 
'''
def computeTFIDF(docs):
    print('in compute')
    ## prevents numbers from being included in tfidf 
    for i in range(1000):
        ENGLISH_STOP_WORDS.append(str(i))
    print(ENGLISH_STOP_WORDS)
    vectorizer = TfidfVectorizer(max_df=1.0, min_df=1, stop_words=ENGLISH_STOP_WORDS, use_idf=True, norm=None)
    transformed_documents = vectorizer.fit_transform(docs)
    transformed_documents_as_array = transformed_documents.toarray()
    ## save the tfidf matrix 
    pd.DataFrame(transformed_documents_as_array).to_csv("tfidf_mat.csv")
    # compute the top-n tfidf weights 
    return transformed_documents_as_array, vectorizer.get_feature_names()


'''
Requires: 
    tfidf_mat is a numpy array corresponding to the feature matrix
    featureList is a python list of feature names (i.e. unique words)
'''

def topN(tfidf_mat, featureList):
    n = 200
    feature_array = np.array(featureList)
    tfidf_sorting = np.argsort(tfidf_mat).flatten()[::-1]
    top_n = feature_array[tfidf_sorting][:n]
    return top_n




## compute the top-n words 
print(topN(*computeTFIDF(linksToTxt())))




# # Create the visualizer and draw the vectors
# tsne = TSNEVisualizer()
# tsne.fit(transformed_documents)
# tsne.poof()

