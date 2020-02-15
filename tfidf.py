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
    vectorizer = TfidfVectorizer(max_df=1.0, min_df=1, stop_words=["the", "of", "and", "is", "our"], use_idf=True, norm=None)
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