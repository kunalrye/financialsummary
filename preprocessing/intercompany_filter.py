"""
Compare the sentences from a 10Q to the sentences of a company's other 10Qs within the same year

Any sentence with a similarity score above a certain threshold will be removed from the corpus
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
    cleaned_lines = list()
    for line in doc_text.splitlines():
        if len(line) > 3:
            if (not (line[0] == "(" or \
                     sum(1 for c in line if c.isupper()) / len(line) > .5 or \
                     "|" in line or "see accompanying notes" in line.lower())):
                cleaned_lines.append(line)


    # doc_sent = tokenize.sent_tokenize(doc_text)
    # sentences += doc_sent
    # non_empty = [sentence for sentence in sentences if len(sentence) > 0]
    return cleaned_lines



def split_by_quarter(dirpath):
    """
    Splits the files of the companies by the quarter that they were released
    :param dirpath: the path to a directory containing ONLY 10Q excepts from that company
    :return: a dictionary mapping the (year, quarter) to a list of the associated files
    """
    for root, dirs, files in os.walk(dirpath):
        for filename in files:

            comps = filename.split("_")
            date_identifier = comps[2]
            year = date_identifier[:4]
            release_data = date_identifier[4:]









def filter():
    print("loading tf hub")
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"  # @param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
    model = hub.load(module_url)

    logging.set_verbosity(logging.ERROR)


split_by_quarter("../resources/legal_filter/AAPL")

