"""
Extract random sentences from the 10Q documents to use as a benchmark for our models
"""
import random
import summa
from modeling.run_model import *


def random_lines(document, sentences):
    """
    Randomly select sentences from a section
    :param document: the document text as a string
    :param sentences: the number of sentences to extract
    :return: a list of randomly selected sentences
    """
    """Choose lines at random from the text file"""
    lines = document.splitlines()
    return random.choices(lines, k=sentences)


summarize_train_docs(random_lines, "Random", True)
summarize_test_docs(random_lines, "Random", True)
