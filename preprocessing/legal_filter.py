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
from preprocessing.train_test_split import get_train_test

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
                     "|" in line or "see accompanying notes" in line.lower())) and ("." in line):
                cleaned_lines.append(line)


    # doc_sent = tokenize.sent_tokenize(doc_text)
    # sentences += doc_sent
    # non_empty = [sentence for sentence in sentences if len(sentence) > 0]
    return cleaned_lines

def get_legal_bank():
    legal_text = open(f"../resources/forward_looking.txt").read()
    legal_sents = tokenize.sent_tokenize(legal_text)
    legal_non_empty = [sentence for sentence in legal_sents if len(sentence) > 0]
    return legal_non_empty



def filter():
    print("loading tf hub")
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"  # @param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]
    model = hub.load(module_url)

    logging.set_verbosity(logging.ERROR)

    print("tokenizing legal bank")
    legal_vectors = model(get_legal_bank())

    ## iterate over all the files in the directory
    input_dirpath = os.path.expanduser("../resources/itemized")
    output_train_dirpath = os.path.expanduser("../resources/legal_filter_train/")
    output_test_dirpath = os.path.expanduser("../resources/legal_filter_test/")

    train_comps, test_comps = get_train_test()

    for root, dirs, files in os.walk(input_dirpath):
        for comp_name in dirs:
            ## output directory name of the company
            out_comp_dirpath = ""
            if comp_name in train_comps:
                out_comp_dirpath = os.path.join(output_train_dirpath, comp_name)
            else:
                out_comp_dirpath = os.path.join(output_test_dirpath, comp_name)

            in_comp_dirpath = os.path.join(input_dirpath, comp_name)
            if not os.path.exists(out_comp_dirpath):
                os.makedirs(out_comp_dirpath)

            for root2, dirs2, files2 in os.walk(in_comp_dirpath):
                for filename in files2:

                    if filename.endswith('.txt'):
                        doc_sentences = file_to_sents(os.path.join(in_comp_dirpath, filename))

                        if not doc_sentences:
                            ## don't pass empty files through the legal filter
                            print(filename + " is empty!")
                            continue

                        doc_vectors = model(doc_sentences) ## generate embeddings from the text file of a 10Q

                        cosine = metrics.pairwise.cosine_similarity(doc_vectors, legal_vectors)

                        # for each document sentence, obtain the highest similarity score it has
                        score_maxes = np.amax(cosine, axis=1)

                        upper_percentile = np.percentile(score_maxes, 75)

                        lower_percentile = np.percentile(score_maxes, 10)

                        # find indices of elements less than the upper threshold and
                        good_idcs = np.nonzero(np.logical_and(score_maxes < upper_percentile, score_maxes > lower_percentile))[0]

                        good_sentences = [doc_sentences[i] for i in good_idcs]

                        with open(os.path.join(out_comp_dirpath, filename), 'w') as f:
                            for sent in good_sentences:
                                f.write("%s\n" % sent)

                        print("finished processing " + filename)


if __name__ == "__main__":
    filter()

