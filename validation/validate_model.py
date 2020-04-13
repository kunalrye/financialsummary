"""
Assesses the performance of our models

To be included in the model assessment, the model name must be included in the MODEL_LIST, and it must have corresponding
<model_name>_train_output and <model_name>_test_output folders in the resource directory
"""
from tabulate import tabulate
from statistics import mean, median, stdev
import os
from collections import defaultdict
from validation.precision_recall import compute_jaccard_index



MODEL_LIST = ["lda", "textrank", "lsa", "LexRank"]
VALIDATION_SET_PATH = "resources/validation_set"


def assess_models(annotated_fname, manual_set):
    """
    Assess a given manual set of lines
    :param manual_set: a set of sentences that we want the model to extract from the corresponding file
    :param annotated_fname: the filename holding the contents of the manual set
    :return:
    """
    model_results = {}

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
    return model_results



def run_assessment():
    results = {}
    ## loop through each manually annotated file
    for root, dirs, files in os.walk(VALIDATION_SET_PATH):
        for fname in files:
            annotated_file = open(os.path.join(VALIDATION_SET_PATH, fname),encoding='utf-8').read()
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



if __name__ == "__main__":
    results = run_assessment()
    for fname, model_scores in results.items():
        print(fname, model_scores)
    print("\n\n")
    tabulate_results(results)





