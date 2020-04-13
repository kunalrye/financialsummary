# Exploration

The following Python files and Jupyter notebooks serve to visualize and project our data in a variety of manners. Some examples of the strategies we employed were cosine similarity to target repetitive jargon and lemmatized text to more accurately tokenize text files.

 * `legal_similarity.ipynb` uses cosine similarity to visualize a heatmap between a company's 10-Q and a set of cautionary statements
 * `off_diagonal_exploration.ipynb` calculates and creates histogram of the sentence similarity scores along off diagonals
 * `text_parsing.ipynb` investigates stemmed and lemmatized text and n-grams for example text
 * `tfidf.py` computes the TF-IDF matrix and outputs the top-n words from the corpus of 187 text documents
 * `ue_heatmap.ipynb` pairwise Universal Sentence Encoded (USE) sentence similarity (cosine) heatmap generated for a sample company
 * `ue_similarity.ipynb` similar objective as above but includes t-SNE of visualizations of USE vectors
 * `visualize_words.ipynb` creates histograms for the word frequencies of the top-n words for a set of documents.
