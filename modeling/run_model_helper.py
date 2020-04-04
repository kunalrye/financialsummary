'''
Applies the text rank model to summarize the filtered files

Output of the model can be found in resources/textrank,
which contains a directory for each company. Within each directory
are files that correspond to the summary for that quarter

'''

import summa
import os
from modeling.compute_num_clusters import calculate_test_cluster_sizes, calculate_train_cluster_sizes
from typing import Callable, List
import math


def by_key(item):
    # for iterating by sorted value so that sections are in alphabetical order
    return item[0]


def summarize_sections(full_doc_name, in_comp_dirpath, out_comp_dirpath, cluster_sizes,
                       model_func: Callable[[str, int], List[str]], update):
    """
    Helper function to summarize all sections for a single 10Q and outputs the summaries into a single document

    :param update:
    :param model_func: lambda to apply the model to a specific document
    :param full_doc_name: the document filename without the section identifier or file type (ex AAPL_0000320193_20171230)
    :param in_comp_dirpath: the directory containing the input files of that company
    :param out_comp_dirpath: the directory to write the output summary file to
    :param cluster_sizes: dictionary calculated via calculate_cluster_sizes() to determine the number of sentences to take for each section
    :return: nothing (writes the file into the out_comp_dirpath directory)
    """
    section_summaries = {}
    for root, dirs, files in os.walk(in_comp_dirpath):
        for filename in files:
            if full_doc_name in filename:  # only process sections from this 10Q
                section_identifier = filename.split("_")[3]  # item1, part2, etc.

                if not update:
                    print("checking " + os.path.join(out_comp_dirpath, "_".join(filename.split("_")[:3]) + ".txt"))
                    if os.path.exists(os.path.join(out_comp_dirpath, "_".join(filename.split("_")[:3]) + ".txt")):
                        print("SKIPPED " + filename)
                        continue

                ## desired length of the summary from this section
                sect_summary_len = cluster_sizes[full_doc_name][section_identifier]

                doc = open(os.path.join(in_comp_dirpath, filename),'r',encoding='utf-8').read()
                if len(doc.splitlines()) == 0 or len(doc) == 0:
                    continue

                summarized_lines = model_func(doc, math.ceil(len(doc.splitlines()) / 2))  # rank half the doc sentences, we'll cut down later
                if not summarized_lines or len(summarized_lines) == 0:  # don't include empty summaries
                    continue
                else:
                    summarized_lines = summarized_lines[:sect_summary_len]
                    # only take as many sentences as we previously computed via cluster_sizes
                    section_summaries[section_identifier] = "\n".join(summarized_lines)

    ## concatenate all section summaries into a single string
    full_summary = ""
    for sect_id, sect_summary in sorted(section_summaries.items(), key=by_key):
        full_summary += sect_id
        full_summary += "\n"
        full_summary += sect_summary
        full_summary += "\n\n\n"

    # write the summary string to the output file
    text_file = open(os.path.join(out_comp_dirpath, full_doc_name) + ".txt", "w")
    text_file.write(full_summary)
    text_file.close()


def summarize_docs(modifier, model_func: Callable[[str, int], List[str]], model_name: str, update: bool):
    """
    Main function to summarize all 10Qs from the filtered input files

    Writes the summary to a textfile in the company folder located at resources/textranks/<company_code>
    :return: nothing
    """
    if modifier == "train":
        cluster_sizes = calculate_train_cluster_sizes()
    else:
        cluster_sizes = calculate_test_cluster_sizes()
    print(cluster_sizes)
    processed = set()

    input_dirpath = os.path.expanduser("../resources/legal_filter_" + modifier)
    output_dirpath = os.path.expanduser(('../resources/' + model_name + '_output_' + modifier))
    for root, dirs, files in os.walk(input_dirpath):
        for comp_name in dirs:
            ## directory of a particular company
            out_comp_dirpath = os.path.join(output_dirpath, comp_name)
            in_comp_dirpath = os.path.join(input_dirpath, comp_name)
            if not os.path.exists(out_comp_dirpath):
                os.makedirs(out_comp_dirpath)

            for root2, dirs2, files2 in os.walk(in_comp_dirpath):
                for filename in files2:
                    comps = filename.split("_")
                    full_doc_name = "_".join(comps[:3])

                    if full_doc_name in processed:
                        continue

                    summarize_sections(full_doc_name, in_comp_dirpath, out_comp_dirpath, cluster_sizes, model_func, update)
                    # the first time we see a section from a 10Q, we just process all sections of the 10Q at once
                    processed.add(full_doc_name)
                    print("processed " + full_doc_name)
