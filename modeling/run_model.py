"""
Helper functions to apply a model to all text in our corpus -->
The caller should supply a model_func that applies the model to a single section of a 10Q document
(function signature specified below in the docstrings)

The logic contained in these functions below will handle concatenating all the summarized sections into the complete
summary for one document
"""
from modeling.run_model_helper import summarize_docs
from typing import Callable, List


def summarize_train_docs(model_func: Callable[[str, int], List[str]], model_name: str):
    """
    Summarizes all training documents according to the supplied model
    
    :param model_func: function handle to the modeling function, 
                must follow the following function signature: 
                List<String> model_func(String document, int num_sents_to_extract) 
    :param model_name: name of the model (will be used for output folder naming, so keep it short)
    :return: nothing
    """
    summarize_docs("train", model_func, model_name)

def summarize_test_docs(model_func: Callable[[str, int], List[str]], model_name: str):
    """
    Summarizes all testing documents according to the supplied model

    :param model_func: function handle to the modeling function,
                must follow the following function signature:
                List<String> model_func(String document, int num_sents_to_extract)
    :param model_name: name of the model (will be used for output folder naming, so keep it short)
    :return: nothing
    """
    summarize_docs("test", model_func, model_name)



