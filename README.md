# financialsummary
A Rice University D2K Lab Project

# Running Our Project
If running code from an IDE, ensure that the run configuration has set the working directory to be the root of the project. 
All paths in the code are specified from the project root. 

The .py files contain many helper functions called by other py files. However, many of the .py
files contain small-use case examples under an `if __name__ == "__main__"` block. 

# Installation
## To download dependecies:
* Install required packages through the requirements.txt file
* Run `pip install -r requirements.txt` while in your repo directory to automatically install all project dependencies

# About:
financialsummary is a repo dedicated to identification of key information in quarterly reports.
Specifically, financialsummary analyzes 10-Q reports from various companies in the Information Technology sector,
and extracts the most important sentences to form a summary.

# Directory Overview:
* Exploration: Data exploration, such as TFIDF, Sentiment analysis etc.
* Modeling: Methods to visualize the data, includes newsgraph and textrank
* Preprocessing: Removal of sentences that will hinder further classification, i.e. legal jargon
* Resources: Smaller csv and txt datafiles
* Wrangling: Gathers 10-Q data and performs basic parsing

### Initial Data Pull:
Prior to storing our data in the resources folder, we used https://github.com/alions7000/SEC-EDGAR-text to pull the data to text files.


