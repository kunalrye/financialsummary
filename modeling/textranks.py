"""
Uses the textrank algorithm to summarize 10Q documents
"""
import summa
from modeling.run_model import *



def textrank_summarize(doc, num_sents):
    """
    Summarizes a 10Q section using textrank
    This function can be passed to the summarize function to run over the entire corpus
    :param doc: the document text as a string
    :param num_sents: the number of sentences to extract
    :return: a list of sentences that is the summary
    """
    if (len(doc.splitlines())) == 0:
        return []

    p = num_sents / len(doc.splitlines())

    summarized_section = summa.summarizer.summarize(doc, ratio=p) # textrank!
    return summarized_section.splitlines()


summarize_train_docs(textrank_summarize, "textrank", True)
summarize_test_docs(textrank_summarize, "textrank", True)