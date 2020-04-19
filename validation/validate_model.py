"""
Assesses the performance of our models

To be included in the model assessment, the model name must be included in the MODEL_LIST, and it must have corresponding
<model_name>_train_output and <model_name>_test_output folders in the resource directory
"""
from tabulate import tabulate
from statistics import mean, median, stdev
import os
from collections import defaultdict
from validation.precision_recall import compute_precision, compute_recall, compute_f1

# removed LSA from MODEL_LIST
MODEL_LIST = ["lda",  "textrank", "luhn", "LSA",  "SumBasic", "Reduction", "KL", "Random", "LexRank", "semisup_topic"]
VALIDATION_SET_PATH = "resources/validation_set"


global topic_validator 


def assess_models(annotated_fname, manual_set):
    """
    Assess a given manual set of lines
    :param manual_set: a set of sentences that we want the model to extract from the corresponding file
    :param annotated_fname: the filename holding the contents of the manual set
    :return: two dictionaries: the first maps a validation filename to the jaccard scores for each model
                                the second maps a validation filename to the topic vector for each model
    """
    recall_results = {}
    precision_results = {}
    f1_results = {}
    jaccard_results = {}
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

        # compute the precision, recall, and f1_scores for this model
        precision_results[model] = compute_precision(manual_set, generated_set)
        recall_results[model] = compute_recall(manual_set, generated_set)
        f1_results[model] = compute_f1(manual_set, generated_set)
        # compute the jaccard index scores for this model
        # jaccard_results[model] = compute_jaccard_index(manual_set, generated_set)
        # compute the topic scores for this model
        # topic_results[model] = topic_validator.compute_topic_scores(generated_set)

    print("assessed models against " + annotated_fname)
    return precision_results, recall_results, f1_results, jaccard_results, topic_results



def run_assessment():
    recall_results = {}
    precision_results = {}
    f1_results = {}
    jaccard_results = {}
    topic_results = {}

    ## loop through each manually annotated file
    for root, dirs, files in os.walk(VALIDATION_SET_PATH):
        for fname in files:
            annotated_file = open(os.path.join(VALIDATION_SET_PATH, fname),encoding='utf-8').read()
            manual_set = set(annotated_file.splitlines())
            precision, recall, f1, jaccard, topic = assess_models(fname, manual_set)
            recall_results[fname] = recall
            precision_results[fname] = precision
            f1_results[fname] = f1
            jaccard_results[fname] = jaccard
            topic_results[fname] = topic
    return precision_results, recall_results, f1_results, jaccard_results, topic_results



def tabulate_results(results):
    """
    Formats the results of a validation run into a table
    :param results: dictionary containing the results of a validation run. Key is the annotated filename, which maps
            to an inner dictionary where the key is the model name, and the value is the validation metric score
            of that model on the annotated filename

            Will take the form {"filename": {"model_name": metric_score, "model_name2": metric_score}, "filename2": ...}
    :return: the table (also prints to stdout)
    """
    # takes the form [<filename>, model1score, model2score,...]
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

    ## create the mean, median, stdev rows that tally the columns
    means = ["mean"]
    medians = ["median"]
    stdevs = ["stdev"]
    for model_name in sorted(per_model):
        means.append(mean(per_model[model_name]))
        medians.append(median(per_model[model_name]))
        stdevs.append(stdev(per_model[model_name]))

    ## get the model with the highest mean and median
    model_means = means[1:] # doesn't include the "mean" header
    model_medians = medians[1:]
    max_mean_model_name = sorted(file_dict)[model_means.index(max(model_means))]
    max_median_model_name = sorted(file_dict)[model_medians.index(max(model_medians))]
    means.append(max_mean_model_name)
    medians.append(max_median_model_name)

    # spacing between data table and summary statistics
    rows.append(["- " for i in range(len(means))]) # spacing
    rows.append(means)
    rows.append(medians)
    rows.append(stdevs)
    headers.append("file's best model")
    table = tabulate(rows, headers)
    print(table)
    return table



if __name__ == "__main__":
    # topic_validator = TopicCoverageValidation()
    # headers = ['precision_results', 'recall_results', 'f1_results', 'jaccard_results', 'topic_results']
    headers = ['precision_results', 'recall_results', 'f1_results']

    results = run_assessment()
    scoring_results = ""
    for header, result in zip(headers, results[:len(headers)]):
        print("\n\n" + header)
        table = tabulate_results(result)
        scoring_results += header
        scoring_results += "\n"
        scoring_results += str(table)
        scoring_results += "\n\n\n\n"
    with open("validation/scoring.txt", 'w') as f:
        f.write(str(scoring_results))
    f.close()




    
