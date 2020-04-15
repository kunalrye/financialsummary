"""
For any 10Q, computes the number of sentences to take from each section (i.e. the cluster size for every section)
with a bias towards taking more sentences from item2

Running calculate_cluster_sizes will return a mapping of 10Q name to an inner
dictionary specifying how many sentences to take from each section

ex. AAPL_0000320193_20171230: {'item2': 15, 'item1': 14, ...}
"""


import os
import math
from collections import defaultdict
SUMMARY_LEN = 20
BIAS = 0.2


def calculate_cluster_dict_for_doc(in_comp_dirpath, full_doc_name):
    """
    Helper function for calculating cluster size for a specific 10Q
    :param in_comp_dirpath: the directory containing the sections for that 10Q
    :param full_doc_name: the name of the document (excluding the section identifier (i.e. part2 or item1)
    :return: a dictionary mapping the section identifier to the cluster size
    """
    cluster_sizes = {}
    num_sects = 0
    # first calculate the number of sentences per 10Q (across all filtered sections)
    total_lines = 0
    for root, dirs, files in os.walk(in_comp_dirpath):
        for fname in files:
            if full_doc_name in fname:
                contents = open(os.path.join(in_comp_dirpath, fname),'r',encoding='utf-8').read()
                total_lines += len(contents.splitlines())
                num_sects += 1


    # now, calculate the cluster sizes
    for root, dirs, files in os.walk(in_comp_dirpath):
        for fname in files:
            if full_doc_name in fname:
                proportion = 0
                contents = open(os.path.join(in_comp_dirpath, fname),'r',encoding='utf-8').read()
                lines = len(contents.splitlines())

                sect_identifier = fname.split("_")[3]
                if lines == 0:
                    proportion = 1
                elif num_sects == 1:
                    proportion = 1
                elif (sect_identifier == "item2"): # impart bias towards item 2
                    proportion = lines/total_lines + BIAS
                else:
                    # subtract the BIAS equally from every other section
                    proportion = lines/total_lines - (BIAS / (num_sects - 1))
                    proportion = proportion if proportion > 0 else 0

                sect_num_clusters = math.ceil(proportion * SUMMARY_LEN)
                cluster_sizes[sect_identifier] = sect_num_clusters
    return cluster_sizes


def calculate_cluster_sizes(input_dirpath):
    """
    Creates a mapping from the 10Q name (which is the filename without the section idenfitifer) to an inner
    dictionary that specifies the number of clusters for each section in that 10Q

    ex. 'SRMC_0000100625_20180630': {'item2.txt': 14, 'item3.txt': 0, 'item1.txt': 11, 'item4.txt': 2, 'part2.txt': 3, 'fls.txt': 0}

    :return: a dictionary with the structure described above
    """
    doc_groups = defaultdict(dict) ## maps a document to an inner mapping of section identifier -> num clusters
    processed = set()
    for root, dirs, files in os.walk(input_dirpath):
        for comp_name in dirs:
            ## directory of a particular company
            in_comp_dirpath = os.path.join(input_dirpath, comp_name)

            for root2, dirs2, files2 in os.walk(in_comp_dirpath):
                for filename in files2:
                    comps = filename.split("_")
                    full_doc_name = "_".join(comps[:3]) # the doc name without the section identifier

                    if full_doc_name in processed: # we've already calculated the cluster amounts for this document
                        continue

                    # the first time we see a section from a 10Q, we just process all sections of the 10Q at once
                    processed.add(full_doc_name)
                    doc_groups[full_doc_name] = calculate_cluster_dict_for_doc(in_comp_dirpath, full_doc_name)

    return doc_groups


def calculate_train_cluster_sizes():
    """
    Calculates cluster sizes for documents of the training companies
    :return: a dictionary with the structure in calculate_cluster_sizes above
    """
    return calculate_cluster_sizes(os.path.expanduser("resources/legal_filter_train"))

def calculate_test_cluster_sizes():
    """
    Calculates cluster sizes for documents of the testing companies
    :return: a dictionary with the structure in calculate_cluster_sizes above
    """
    return calculate_cluster_sizes(os.path.expanduser("resources/legal_filter_test"))

if __name__ == "__main__":
    print(calculate_train_cluster_sizes())
    print(calculate_test_cluster_sizes())











