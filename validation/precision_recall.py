"""
Library of functions to compute the precision, recall, f1, and jaccard scores for a model-generated
summary against a manually generated summary.
"""

from difflib import SequenceMatcher


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


def compute_precision(manual_set, generated_set):
    """
    Computes the precision of the generated summary
    Precision is the fraction of relevant instances among the retrieved instances
    :param manual_set:
    :param generated_set:
    :return:
    """
    intersect = intersection(manual_set, generated_set)
    return float(len(intersect) / len(manual_set))



def compute_recall(manual_set, generated_set):
    """
    Computes the recall of the generated summary
    Recall is the fraction of the total amount of relevant instances that were actually retrieved
    :param manual_set:
    :param generated_set:
    :return:
    """
    intersect = intersection(manual_set, generated_set)
    return float(len(intersect) / len(generated_set))


def compute_f1(manual_set, generated_set):
    intersect = intersection(manual_set, generated_set)
    recall = compute_recall(manual_set, generated_set)
    precision = compute_precision(manual_set, generated_set)

    if (recall + precision) == 0:
        return 0

    return  2.0 * precision * recall / (precision + recall)

def compute_jaccard_index(manual_set, generated_set):
    # intersect = manual_set.intersection(generated_set)
    intersect = intersection(manual_set, generated_set)
    ## jaccard index score between the validation file and the corresponding model file
    return float(len(intersect)) / (len(manual_set) + len(generated_set) - len(intersect))