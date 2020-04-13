"""
Assesses the performance of a model by for each file in our validation set, computing the jaccard index
between our manually generated file and
"""
from difflib import SequenceMatcher
from tabulate import tabulate
from statistics import mean, median, stdev
import os
from collections import defaultdict
from modeling.lda import *
from gensim.models import LdaModel
import pickle

from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt


MODEL_LIST = ["lda", "textrank", "lsa"]
VALIDATION_SET_PATH = "resources/validation_set"


def set_contains(s, ele):
    """
    Looser equality check to see if a set contains an element
    :param s: the set
    :param ele: the element to check membership
    :return: True/False for membership
    """
    for i in s:

        if i and ele and (ele in i or i in ele or SequenceMatcher(i,ele).ratio() > 0.97):
            print(i)
            print(ele)
            return True
    return False



def intersection(a, b):
    """
    Our own implementation of set intersection since the sentences might not be exact maches
    :return:
    """
    intersect = set()
    for i in a:
        if set_contains(b, i):
            intersect.add(i)
    return intersect



def compute_jaccard_index(manual_set, generated_set):
    """
    Computes the Intersection Over Union score of the manually annotated set and the automatically generated set
    :param manual_set: manually annotated set
    :param generated_set: generated summary set
    :return: jaccard index
    """
    # intersect = manual_set.intersection(generated_set)
    intersect = intersection(manual_set, generated_set)
    ## jaccard index score between the validation file and the corresponding model file
    return float(len(intersect)) / (len(manual_set) + len(generated_set) - len(intersect))


def compute_topic_scores(doc_sents, dictionary, ldamodel):
    """
    Computes a topic specifying how the sentences fall into the 15 topics
    :param doc_sents: sentences of the document
    :param dictionary:
    :param ldamodel:
    :return: the length 15 topic vector
    """
    best_topics = list()
    valid_vectors = list

    doc_topics = np.zeros(15)

    for line in doc_sents:
        new_doc = prepare_text_for_lda(line)
        new_doc_bow = dictionary.doc2bow(new_doc)
        tmax = np.argmax([two for one, two in ldamodel.get_document_topics(new_doc_bow)])
        sent_topic = ldamodel.get_document_topics(new_doc_bow)[tmax][0]
        doc_topics[sent_topic] += 1
    doc_topics = doc_topics / np.linalg.norm(doc_topics)
    return doc_topics



def assess_models(annotated_fname, manual_set, dictionary, ldamodel):
    """
    Assess a given manual set of lines
    :param manual_set: a set of sentences that we want the model to extract from the corresponding file
    :param annotated_fname: the filename holding the contents of the manual set
    :return: two dictionaries: the first maps a validation filename to the jaccard scores for each model
                                the second maps a validation filename to the topic vector for each model
    """
    model_results = {}
    topic_results = {}

    ## get a list of all directories in the resource directory
    d = "resources"
    subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))]

    for model in MODEL_LIST:
        try:
            # corresponding file could be in either the test or train folder, so we have to search both
            train_folder = [sd for sd in subdirs if model in sd and "train" in sd][0]
            test_folder = [sd for sd in subdirs if model in sd and "test" in sd][0]
        except:
            print(model + " does not have output folders!")
            continue

        comp_ticker = annotated_fname.split("_")[0]


        # get the set of sentences that this model generated
        if os.path.exists(os.path.join(train_folder, comp_ticker, annotated_fname)):
            generated_file = open(os.path.join(train_folder, comp_ticker, annotated_fname),encoding='utf-8')
        elif os.path.exists(os.path.join(test_folder, comp_ticker, annotated_fname)):
            # it's in the test directory
            generated_file = open(os.path.join(test_folder, comp_ticker, annotated_fname),encoding='utf-8')
        else:
            print("this shouldn't happen lmao")
            continue

        generated_set = set(generated_file.read().splitlines())
        jac_idx = compute_jaccard_index(manual_set, generated_set)
        model_results[model] = jac_idx

        # compute the topic scores for this model
        # lines = generated_file.read().splitlines()
        # if not lines or len(lines) == 0:
        #     print("waht")
        topic_results[model] = compute_topic_scores(generated_set, dictionary, ldamodel)


    return model_results, topic_results



def run_assessment():
    results = {}
    topic_results = {}

    # set up lda modeling
    # setup for topic modeling
    with open("resources/ALL_TEXT.txt", 'r', encoding='utf-8') as f:
        text = f.read().splitlines()

    all_tokens = list()
    for line in text:
        all_tokens.append(prepare_text_for_lda(line))
    dictionary = corpora.Dictionary(all_tokens)
    NUM_TOPICS = 15
    ldamodel = LdaModel.load('modeling/alltext15.gensim')

    ## loop through each manually annotated file
    for root, dirs, files in os.walk(VALIDATION_SET_PATH):
        for fname in files:
            annotated_file = open(os.path.join(VALIDATION_SET_PATH, fname),encoding='utf-8').read()
            manual_set = set(annotated_file.splitlines())
            model_results, model_topics = assess_models(fname, manual_set, dictionary, ldamodel)
            results[fname] = model_results
            topic_results[fname] = model_topics
    return results, topic_results



def tabulate_results(results):
    # [<filename>, model1score, model2score,...]
    rows = []
    # list of model names
    headers = ["test filename"]
    flag = 0

    # dict that for each model, tracks the scores in a list
    per_model = defaultdict(list)

    # iterate over each file
    for fname, file_dict in results.items():

        model_scores = []
        # creates a list of model scores in alphabetical order based on model name
        for model_name in sorted(file_dict):
            model_scores.append(file_dict[model_name])
            per_model[model_name].append(file_dict[model_name])
            if not flag:
                headers.append(model_name)

        ## find the model name with the highest score for that file
        max_model_name = sorted(file_dict)[model_scores.index(max(model_scores))]
        model_scores.insert(0, fname)
        model_scores.append(max_model_name)
        rows.append(model_scores)
        flag = 1

    means = ["mean"]
    medians = ["median"]
    stdevs = ["stdev"]
    for model_name in sorted(per_model):
        means.append(mean(per_model[model_name]))
        medians.append(median(per_model[model_name]))
        stdevs.append(stdev(per_model[model_name]))


    rows.append(["- " for i in range(len(means))]) # spacing
    rows.append(means)
    rows.append(medians)
    rows.append(stdevs)
    headers.append("file's best model")
    table = tabulate(rows, headers)
    print(table)


def get_manual_topic_vectors():
    """
    Obtains the topic vectors from the manual summmaries of the validation files
    :return: a list of topic vectors for the validation files
    """
    with open("resources/ALL_TEXT.txt", 'r', encoding='utf-8') as f:
        text = f.read().splitlines()

    all_tokens = list()
    for line in text:
        all_tokens.append(prepare_text_for_lda(line))
    dictionary = corpora.Dictionary(all_tokens)
    ldamodel = LdaModel.load('modeling/alltext15.gensim')

    best_topics = list()
    for root, dirs, files in os.walk(VALIDATION_SET_PATH):
        for file in files:
            doc_topics = np.zeros(15)
            with open(os.path.join(VALIDATION_SET_PATH, file), 'r', encoding='utf-8') as f:
                validation_doc = f.read().splitlines()
            for line in validation_doc:
                new_doc = prepare_text_for_lda(line)
                new_doc_bow = dictionary.doc2bow(new_doc)
                tmax = np.argmax([two for one, two in ldamodel.get_document_topics(new_doc_bow)])
                sent_topic = ldamodel.get_document_topics(new_doc_bow)[tmax][0]
                doc_topics[sent_topic] += 1
            print(doc_topics)
            doc_topics = doc_topics / np.linalg.norm(doc_topics)
            best_topics.append(doc_topics)
    return best_topics


if __name__ == "__main__":
    # results, topic_results = run_assessment()h
    # for fname, model_scores in results.items():
    #     print(fname, model_scores)
    # print("\n\n")
    # tabulate_results(results)h
    # print(topic_results)
    #
    # output = open('modeling/autogen_topics.pkl', 'wb')
    # pickle.dump(topic_results, output)
    # output.close()
    best_topics = get_manual_topic_vectors()

    pkl_file = open('modeling/autogen_topics.pkl', 'rb')
    topic_results = pickle.load(pkl_file)
    pkl_file.close()

    autogen_topics = list()
    for root, dirs, files in os.walk(VALIDATION_SET_PATH):
        for file in files:
            autogen_topics.append(topic_results[file]['lda'])

    print(autogen_topics)
    cosine = metrics.pairwise.cosine_similarity(autogen_topics, best_topics)
    sns.heatmap(cosine, cmap="YlGnBu")
    plt.show()







