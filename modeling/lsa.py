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

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

parser = English()

def tokenize(text):
    '''
    takes in a line of text and tokenizes by word
    :param text:
    :return:
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
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma


def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

all_tokens = list()
def do_lda(text, NUM_SENTS):
    '''
    trains an lda model on the text and performs local lda to determine which sentences contain a majority of the topics
    '''
    for line in text:
        all_tokens.append(prepare_text_for_lda(line))
    dictionary = corpora.Dictionary(all_tokens)
    corpus = [dictionary.doc2bow(text) for text in all_tokens]

    pickle.dump(corpus, open('corpus.pkl', 'wb'))
    dictionary.save('dictionary.gensim')
    NUM_TOPICS = 5
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)
    ldamodel.save('model5.gensim')
    topics = ldamodel.print_topics(num_words=4)
    for topic in topics:
        print(topic)

    maxes = list()
    lda_sents = list()
    for line in text:
        new_doc = prepare_text_for_lda(line)
        new_doc_bow = dictionary.doc2bow(new_doc)
        max_sim = np.max([two for one, two in ldamodel.get_document_topics(new_doc_bow)])
        maxes.append(max_sim)
    cutoff = np.sort(maxes)[NUM_SENTS]
    ## This is a really inefficient way to do this, but it works well
    for line in text:
        new_doc = prepare_text_for_lda(line)
        new_doc_bow = dictionary.doc2bow(new_doc)
        max_sim = np.max([two for one, two in ldamodel.get_document_topics(new_doc_bow)])
        if max_sim > cutoff:
            lda_sents.append(line)
    return (lda_sents)