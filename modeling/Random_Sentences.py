import random
import summa
from modeling.run_model import *


def random_lines(document, sentences):
    """Choose lines at random from the text file"""
    lines = document.splitlines()
    return random.choices(lines, k=sentences)


summarize_train_docs(random_lines, "Random", True)
summarize_test_docs(random_lines, "Random", True)
