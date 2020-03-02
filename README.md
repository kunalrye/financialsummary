# financialsummary
A Rice University D2K Lab Project
#About:
financialsummary is a repo dedicated to identification of key information in quarterly reports.
Specifically, financialsummary analyzes 10-Q reports from various companies in the Information Technology sector,
and extracts the most important sentences to form a summary.

#Directory Overview:
* Exploration: Data exploration, such as TFIDF, Sentiment analysis etc.
* Modeling: Methods to visualize the data, includes newsgraph and textrank
* Preprocessing: Removal of sentences that will hinder further classification, i.e. legal jargon
* Resources: Smaller csv and txt datafile 
* Wrangling: Gathers 10-Q data and performs basic parsing

# Installation
## To download dependecies:
* Install the pipenv package  
* Run pipenv install while in your repo directory

## BERT Usage: 
Much of the initial code to run bert was taken from the following link.
https://stackoverflow.com/questions/55619176/how-to-cluster-similar-sentences-using-bert

###To download the pretrained model:
* Visit: https://github.com/google-research/bert#pre-trained-models
* Download Bert-Base (Uncased) to ~/Documents/uncased_L-12_H-768_A-12/ 
###Bert server and bert client: 
####BERT CLI Usage
bert-serving-start -model_dir ~/Documents/uncased_L-12_H-768_A-12/ -num_worker=1 -max_seq_len=50

pip installations in the pip file
* note: tensorflow version 1.15 or lower must be used to avoid Type Error 


