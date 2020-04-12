"""
Assesses the performance of a model by for each file in our validation set, computing the jaccard index
between our manually generated file and
"""
from difflib import SequenceMatcher
from tabulate import tabulate
from statistics import mean, median, stdev
import os
from collections import defaultdict

MODEL_LIST = ["lda", "textrank", "lsa"]
VALIDATION_SET_PATH = "../resources/validation_set"


def set_contains(s, ele):
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
    # intersect = manual_set.intersection(generated_set)
    intersect = intersection(manual_set, generated_set)
    ## jaccard index score between the validation file and the corresponding model file
    return float(len(intersect)) / (len(manual_set) + len(generated_set) - len(intersect))


def assess_models(annotated_fname, manual_set):
    """
    Assess a given manual set of lines
    :param manual_set: a set of sentences that we want the model to extract from the corresponding file
    :param annotated_fname: the filename holding the contents of the manual set
    :return:
    """
    model_results = {}

    ## get a list of all directories in the resource directory
    d = "../resources"
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
            generated_file = open(os.path.join(train_folder, comp_ticker, annotated_fname))
        elif os.path.exists(os.path.join(test_folder, comp_ticker, annotated_fname)):
            # it's in the test directory
            generated_file = open(os.path.join(test_folder, comp_ticker, annotated_fname))
        else:
            print("this shouldn't happen lmao")
            continue

        generated_set = set(generated_file.read().splitlines())
        jac_idx = compute_jaccard_index(manual_set, generated_set)
        model_results[model] = jac_idx
    return model_results



def run_assessment():
    results = {}
    ## loop through each manually annotated file
    for root, dirs, files in os.walk(VALIDATION_SET_PATH):
        for fname in files:
            annotated_file = open(os.path.join(VALIDATION_SET_PATH, fname)).read()
            manual_set = set(annotated_file.splitlines())
            results[fname] = assess_models(fname, manual_set)
    return results



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
        model_scores.insert(0, fname)
        rows.append(model_scores)
        flag = 1

    means = ["mean"]
    medians = ["median"]
    stdevs = ["stdev"]
    for model_name in sorted(per_model):
        means.append(mean(per_model[model_name]))
        medians.append(median(per_model[model_name]))
        stdevs.append(stdev(per_model[model_name]))

    rows.append(["-" for i in range(len(means))]) # spacing
    rows.append(means)
    rows.append(medians)
    rows.append(stdevs)
    table = tabulate(rows, headers)
    print(table)



if __name__ == "__main__":
    results = run_assessment()
    for fname, model_scores in results.items():
        print(fname, model_scores)
    tabulate_results(results)





