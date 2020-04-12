'''
Computes the TF-IDF matrix and the top-n words from the corpus of 187 documents
Requires: resources directory containing the text files of the 10-Qs
'''

import numpy as np
import pandas as pd 
from wrangling.retrieve_sentences import txtToStrings
from sklearn.feature_extraction.text import TfidfVectorizer

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


def computeTFIDF(docs):
    """
    Computes the TFIDF matrix for all 10Qs
    
    Arguments:
        docs {List<String>} -- each string is the plain text of the 10Q
    
    Returns:
        [2D ndarray, List<String>] -- TFIDF matrix, list of terms in the TFIDF matrix 
    """
    print('in compute')
    ## prevents numbers from being included in tfidf 
    for i in range(1000):
        ENGLISH_STOP_WORDS.append(str(i))
    print(ENGLISH_STOP_WORDS)
    vectorizer = TfidfVectorizer(max_df=1.0, min_df=1, stop_words=ENGLISH_STOP_WORDS, use_idf=True, norm=None)
    transformed_documents = vectorizer.fit_transform(docs)
    transformed_documents_as_array = transformed_documents.toarray()
    ## save the tfidf matrix 
    pd.DataFrame(transformed_documents_as_array).to_csv("resources/tfidf_mat.csv")
    # compute the top-n tfidf weights 
    return transformed_documents_as_array, vectorizer.get_feature_names()


def topN(tfidf_mat, featureList, n):
    """
    Computes the topN words
    
    Arguments:
        tfidf_mat {2D ndarray} -- the TFIDF matrix 
        featureList {List<String>} -- list of the terms in the TFIDF matrix 
        n {int} -- specifies how many words to select 

    Returns:
        List<String> -- top n terms from the TFIDF matrix 
    """
    feature_array = np.array(featureList)
    tfidf_sorting = np.argsort(tfidf_mat).flatten()[::-1]
    top_n = feature_array[tfidf_sorting][:n]
    return top_n


## compute the top-n words 
if __name__ == "__main__":
    print(topN(*computeTFIDF(txtToStrings()), 200))


# # Create the visualizer and draw the vectors
# tsne = TSNEVisualizer()
# tsne.fit(transformed_documents)
# tsne.poof()

