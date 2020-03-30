"""
Compare the sentences from the 10Qs to a corpus of legal sentences

Any sentences above a certain threshold will be removed, and this
script will return the remaining sentences
"""
from absl import logging
import tensorflow_hub as hub
import numpy as np
import os
from nltk import tokenize
from sklearn import metrics

def file_to_sents(fname):
    """
    Extracts the sentences from a file
    :param fname: must be a well-formed path to the file
    :return: a list of (nonzero length) sentences from the text file
    """
    sentences = []
    doc_text = open(fname).read()
    doc_sent = tokenize.sent_tokenize(doc_text)[:740]
    sentences += doc_sent
    non_empty = [sentence for sentence in sentences if len(sentence) > 0]
    return non_empty

def get_legal_bank():
    legal_text = open(f"../resources/forward_looking.txt").read()
    legal_sents = tokenize.sent_tokenize(legal_text)
    legal_non_empty = [sentence for sentence in legal_sents if len(sentence) > 0]
    return legal_non_empty



def filter(directory):
    print("loading tf hub")
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"  # @param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
    model = hub.load(module_url)

    logging.set_verbosity(logging.ERROR)

    print("tokenizing legal bank")
    legal_vectors = model(get_legal_bank())

    ## iterate over all the files in the directory
    dirpath = os.path.expanduser("../resources/itemized")
    print(dirpath)
    outdir_path = os.path.expanduser("../resources/legal_filter/")
    for subdir, dirs, files in os.walk(dirpath):
        for filename in files:
            if filename.endswith('.txt'):
                fpath = os.path.join(subdir, filename)
                doc_sentences = file_to_sents(fpath)

                if not doc_sentences:
                    ## don't pass empty files through the legal filter
                    print(filename + " is empty!")
                    continue

                doc_vectors = model(doc_sentences) ## generate embeddings from the text file of a 10Q

                cosine = metrics.pairwise.cosine_similarity(doc_vectors, legal_vectors)

                # for each document sentence, obtain the highest similarity score it has
                score_maxes = np.amax(cosine, axis=1)

                percentile = np.percentile(score_maxes, 75)

                good_idcs = np.nonzero(score_maxes < percentile)[0] # find indices of elements less than the threshold

                good_sentences = [doc_sentences[i] for i in good_idcs]

                with open(outdir_path +  filename, 'w') as f:
                    for sent in good_sentences:
                        f.write("%s\n" % sent)

                print("finished processing " + filename)

    # doc_vectors = model(non_empty)



filter("../resources/filtered")









