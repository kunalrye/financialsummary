"""
Library of functions that compute the topic coverage scores of a model-generated summary when compared
to topic coverage of the manually generated summaries of the validation set. 
"""


from modeling.lda import *
from gensim.models import LdaModel
import pickle
import os
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt

VALIDATION_SET_PATH = "resources/validation_set"
TRAINING_SET_PATH = "resources/training_set"


class TopicCoverageValidation:

    def __init__(self):

        with open("resources/ALL_TEXT.txt", 'r', encoding='utf-8') as f:
            text = f.read().splitlines()
        all_tokens = list()
        for line in text:
            all_tokens.append(prepare_text_for_lda(line))

        self.dictionary = corpora.Dictionary(all_tokens)
        self.NUM_TOPICS = 15
        self.ldamodel = LdaModel.load('validation/alltext15.gensim')
        self.manual_vecs = self.get_manual_doc_topic_vectors()



    def get_sent_topics(self, doc_sents):
        '''
        :param doc_sents: list of sentences to calculate the topics of
        :return: the list of topics for each sentence
        '''

        sent_topics = list()
        if not doc_sents:
            return []
        for line in doc_sents:
            doc_topics = np.zeros(15)
            new_doc = prepare_text_for_lda(line)
            if not new_doc:
                continue
            new_doc_bow = self.dictionary.doc2bow(new_doc)
            for one, two in self.ldamodel.get_document_topics(new_doc_bow):
                doc_topics[one] = two
            sent_topics.append(doc_topics)
        return sent_topics


    def get_training_sent_topic_vectors(self):
        """
        Obtains the topic vectors for sentence from the manual summmaries of the training files 
        :return: a list of topic vectors for the validation files
        """

        best_topics = list()
        for root, dirs, files in os.walk(TRAINING_SET_PATH):
            for file in files:
                with open(os.path.join(TRAINING_SET_PATH, file), 'r', encoding='utf-8') as f:
                    validation_doc = f.read().splitlines()
                    best_topics.extend(self.get_sent_topics(validation_doc))	

        return best_topics





    def get_manual_doc_topic_vectors(self):
        """
        Obtains the topic vectors from the manual summmaries of the validation files
        :return: a list of topic vectors for the validation files
        """

        best_topics = list()
        for root, dirs, files in os.walk(VALIDATION_SET_PATH):
            for file in files:
                doc_topics = np.zeros(15)
                with open(os.path.join(VALIDATION_SET_PATH, file), 'r', encoding='utf-8') as f:
                    validation_doc = f.read().splitlines()
                for line in validation_doc:
                    new_doc = prepare_text_for_lda(line)
                    if not new_doc:
                        continue
                    new_doc_bow = self.dictionary.doc2bow(new_doc)
                    tmax = np.argmax([two for one, two in self.ldamodel.get_document_topics(new_doc_bow)])
                    try:
                        sent_topic = self.ldamodel.get_document_topics(new_doc_bow)[tmax][0]
                        doc_topics[sent_topic] += 1
                    except:
                        continue
                # print(doc_topics)
                doc_topics = doc_topics / np.linalg.norm(doc_topics)
                best_topics.append(doc_topics)
        return best_topics



    def compute_topic_scores(self, doc_sents):
        """
        Computes a topic specifying how the sentences fall into the 15 topics
        :param doc_sents: sentences of the document
        :param dictionary:
        :param ldamodel:
        :return: the length 15 topic vector
        """
        # compute the topic vector for this document
        doc_topics = np.zeros(15)
        if not doc_sents:
            return 0.0
        for line in doc_sents:
            new_doc = prepare_text_for_lda(line)
            if not new_doc:
                continue
            new_doc_bow = self.dictionary.doc2bow(new_doc)
            tmax = np.argmax([two for one, two in self.ldamodel.get_document_topics(new_doc_bow)])

            # print(tmax)
            try:
                sent_topic = self.ldamodel.get_document_topics(new_doc_bow)[tmax][0]
                doc_topics[sent_topic] += 1
            except:
                continue
        doc_topics = doc_topics / np.linalg.norm(doc_topics)

        # compare this document's topic vector with each one of the manually generated topic vectors, and choose the highest score
        best_score = max([np.dot(doc_topics, v) for v in self.manual_vecs])
        return best_score




    # def plot_topic_vecs(self):
        
    #     # run if the autogen_topics.pkl file does not exist in the current directory (or if it needs to be regenerated)
    #     # output = open('modeling/autogen_topics.pkl', 'wb')
    #     # pickle.dump(topic_results, output)
    #     # output.close()
    #     best_topics = self.get_manual_topic_vectors()

    #     # load the topic vectors for the autogenerated summaries 
    #     pkl_file = open('modeling/autogen_topics.pkl', 'rb')
    #     topic_results = pickle.load(pkl_file)
    #     pkl_file.close()

    #     autogen_topics = list()
    #     for root, dirs, files in os.walk(VALIDATION_SET_PATH):
    #         for file in files:
    #             autogen_topics.append(topic_results[file]['lda'])

    #     print(autogen_topics)
    #     cosine = metrics.pairwise.cosine_similarity(autogen_topics, best_topics)
    #     sns.heatmap(cosine, cmap="YlGnBu")
    #     plt.show()






