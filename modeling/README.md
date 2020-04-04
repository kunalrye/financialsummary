# Modeling

For convenience, `summarize_train_docs`, `summarize_test_docs`, and `summarize_company_docs` functions have been supplied in `run_model.py` so that a caller can apply a model to all files in the corpus

*These functions standardize and encapsulate the process of running every section individually through a model and concatenating the outputs of sections into a single summary.* 

To use these functions, write a wrapper function that calls your model, where the wrapper function follows the following signature (Java-style notation): 

`List<String> model_func(String document_text, int num_sents_to_extract)`

 where `document_text` is a string containing the contents of the document, and `num_sents_to_extract` is the number of sentences that the model should extract from the document.
 
 * `summarize_train_docs` summarizes all the training documents 
 * `summarize_test_docs` summarizes all the testing documents
 * `summarize_company_docs` summarizes all the documents for a single company (SHOULD BE USED FOR PRELIMINARY MODEL TESTING)
