import spacy
# spacy.load('en')
from spacy.lang.en import English

import nltk
import gensim

nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import pickle
from gensim import corpora
import numpy as np
from modeling.run_model import summarize_train_docs, summarize_test_docs

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

parser = English()

def tokenize(text):
    '''
    takes in a line of text and tokenizes by word
    :param text: a line of text
    :return: a list of tokens
    '''
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens




def get_lemma(word):
    """
    The lemmas corresponding to a word
    :param word: a single word from the dictionary
    :return: the lemma
    """
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma


def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

def prepare_text_for_lda(text):
    """
    Basic token filtering for the text to filter out lines that result in empty token lists
    :param text: the line of text to be prepared
    :return: the tokens
    """
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    for token in tokens:
        if len(get_lemma(token)) == 0:
            print('empty token')

    tokens = [get_lemma(token) for token in tokens]
    return tokens


def do_lda(doc_text, NUM_SENTS):
    '''
    trains an lda model on the text and performs local lda to determine which sentences contain a majority of the topics
    '''
    text= doc_text.splitlines()
    if(len(text) < NUM_SENTS):
        return(text)
    else:
        all_tokens = list()
        for line in text:
            all_tokens.append(prepare_text_for_lda(line))
        dictionary = corpora.Dictionary(all_tokens)
        corpus = [dictionary.doc2bow(text) for text in all_tokens]

        # pickle.dump(corpus, open('corpus.pkl', 'wb'))
        # dictionary.save('dictionary.gensim')
        NUM_TOPICS = 5
        if len(corpus[0]) == 0:
            return([])
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)

        ldamodel.save('model5.gensim')
        topics = ldamodel.print_topics(num_words=4)
        maxes = list()
        lda_sents = list()
        for line in text:
            new_doc = prepare_text_for_lda(line)
            new_doc_bow = dictionary.doc2bow(new_doc)
            max_sim = np.max([two for one, two in ldamodel.get_document_topics(new_doc_bow)])
            maxes.append(max_sim)
        cutoff = np.sort(maxes)[NUM_SENTS-1]
        ## This is a really inefficient way to do this, but it works well
        for line in text:
            new_doc = prepare_text_for_lda(line)
            new_doc_bow = dictionary.doc2bow(new_doc)
            max_sim = np.max([two for one, two in ldamodel.get_document_topics(new_doc_bow)])
            if max_sim > cutoff:
                lda_sents.append(line)
        return (lda_sents)

## Example Code
if __name__ == '__main__':
    summarize_train_docs(do_lda, "lda", True)
    summarize_test_docs(do_lda, "lda", True)


