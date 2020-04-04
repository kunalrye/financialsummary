'''
Applies the text rank model to summarize the filtered files

Output of the model can be found in resources/textrank,
which contains a directory for each company. Within each directory
are files that correspond to the summary for that quarter

'''

import summa
import os
from modeling.compute_num_clusters import calculate_cluster_sizes



def by_key(item):
    # for iterating by sorted value so that sections are in alphabetical order
    return item[0]

def summarize_sections(full_doc_name, in_comp_dirpath, out_comp_dirpath, cluster_sizes):
    """
    Helper function to summarize all sections for a single 10Q and outputs the summaries into a single document

    :param full_doc_name: the document filename without the section identifier or file type (ex AAPL_0000320193_20171230)
    :param in_comp_dirpath: the directory containing the input files of that company
    :param out_comp_dirpath: the directory to write the output summary file to
    :param cluster_sizes: dictionary calculated via calculate_cluster_sizes() to determine the number of sentences to take for each section
    :return: nothing (writes the file into the out_comp_dirpath directory)
    """
    section_summaries = {}
    for root, dirs, files in os.walk(in_comp_dirpath):
        for filename in files:
            if full_doc_name in filename: # only process sections from this 10Q
                section_identifier = filename.split("_")[3] # item1, part2, etc.
                ## desired length of the summary from this section
                sect_summary_len = cluster_sizes[full_doc_name][section_identifier]

                doc = open(os.path.join(in_comp_dirpath, filename)).read()
                num_sents = len(doc.splitlines())

                print("sect summary len is " + str(sect_summary_len))
                print("num sents is " + str(num_sents))
                if num_sents == 0 or sect_summary_len == 0: # don't process empty sections
                    continue
                proportion = sect_summary_len / num_sents  # proportion of the section to summarize
                summarized_section = summa.summarizer.summarize(doc, ratio=proportion) # textrank!
                print(proportion)
                if len(summarized_section.splitlines()) == 0:  # don't include non-standard summary
                    continue

                if len(summarized_section.splitlines()) > sect_summary_len + 2:
                    print("summarized section length case is " + str(len(summarized_section.splitlines())))
                    print("sect summary should have been " + str(sect_summary_len))

                section_summaries[section_identifier] = summarized_section


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


def summarize_docs():
    """
    Main function to summarize all 10Qs from the filtered input files

    Writes the summary to a textfile in the company folder located at resources/textranks/<company_code>
    :return: nothing
    """
    cluster_sizes = calculate_cluster_sizes()
    print(cluster_sizes)
    processed = set()

    input_dirpath = os.path.expanduser("../resources/legal_filter")
    output_dirpath = os.path.expanduser(('../resources/textrank'))
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

                    summarize_sections(full_doc_name, in_comp_dirpath, out_comp_dirpath, cluster_sizes)
                    # the first time we see a section from a 10Q, we just process all sections of the 10Q at once
                    processed.add(full_doc_name)
                    print("processed " + full_doc_name)


if __name__ == "__main__":
    summarize_docs()


