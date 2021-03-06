"""
Helper functions to apply a model to all text in our corpus -->
The caller should supply a model_func that applies the model to a single section of a 10Q document
(function signature specified below in the docstrings)

The logic contained in these functions below will handle concatenating all the summarized sections into the complete
summary for one document

See textranks.py for an example of how to use this library
"""
from modeling.run_model_helper import summarize_docs, summarize_docs_for_company
from typing import Callable, List


def summarize_train_docs(model_func: Callable[[str, int], List[str]], model_name: str, update=False):
    """
    Summarizes all training documents according to the supplied model
    
    :param update: whether to update an existing file (true) or not (false)
    :param model_func: function handle to the modeling function,
                must follow the following function signature: 
                List<String> model_func(String document, int num_sents_to_extract) 
    :param model_name: name of the model (will be used for output folder naming, so keep it short)
    :return: nothing
    """
    summarize_docs("train", model_func, model_name, update)


def summarize_test_docs(model_func: Callable[[str, int], List[str]], model_name: str, update=False):
    """
    Summarizes all testing documents according to the supplied model

    :param update: whether to update an existing file (true) or not (false)
    :param model_func: function handle to the modeling function,
                must follow the following function signature:
                List<String> model_func(String document, int num_sents_to_extract)
    :param model_name: name of the model (will be used for output folder naming, so keep it short)
    :return: nothing
    """
    summarize_docs("test", model_func, model_name, update)

def summarize_company_docs(company_name: str, model_func: Callable[[str, int], List[str]], model_name: str):
    """
    Summarizes the 10Qs for a specific company
    :param company_name: the company code (as listed in the legal filter directories
    :param model_func: function handle to the modeling function,
                must follow the following function signature:
                List<String> model_func(String document, int num_sents_to_extract)
    :param model_name: name of the model (will be used for output folder naming, so keep it short)
    :return: nothing
    """
    summarize_docs_for_company(company_name, model_func, model_name, True)