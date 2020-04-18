# financialsummary
A Rice University D2K Lab Project - DSCI 400

# Installation
* Ensure that Python 3.2 or newer is installed
* If running code from an IDE, ensure that the IDE appends the project root to the system path. (Most IDEs already do this)
* Run `pip install -r requirements.txt` while in your repo directory to automatically install all project dependencies
 * Ensure that `pip` is tied to the desired Python 3 installation (NOT to the Python 2 installation). 
* Run the financialsummary.ipynb file

# About:
financialsummary is a repo dedicated to identification of key information in quarterly reports.
Specifically, financialsummary analyzes 10-Q reports from various companies in the Information Technology sector,
and extracts the most important sentences to form a summary.

# Running Code
The entire text-to-summary pipline can be run by running `financialsummary.ipynb`, located at the root of the repo. 
Files that can be directly run are highlighted in the Pipeline Overview section. 

*Note, all paths originate from the root of the project, so all files must be run with the working directory set to the root of the project.* 


# Repo Overview:
* Exploration: Data exploration, such as TFIDF, Sentiment analysis etc.
* Modeling: Methods to visualize the data, includes newsgraph and textrank
* Preprocessing: Removal of sentences that will hinder further classification, i.e. legal jargon
* Resources: Smaller csv and txt datafiles
* Wrangling: Gathers 10-Q data and performs basic parsing

## Pipeline Overview
1) Exploration: each .ipynb file explores an aspect of the corpus. For example, `ue_similarity.ipynb` compares the sentences across a company's 10-Qs to each other to see if there is sentence-level correlation between the 10-Qs of the same company. 
2) Wrangling: `sep_sections.py` will pull 10-Qs from the SEC EDGAR API and parse each 10-Q into individual sections. 
3) Preprocessing: `legal_filter.py` will pass each individual section through the legal filter, which compares sentences to a set of legal statements and removes the most similar sentences from the sections (i.e. the legal boilerplate)
4) Modeling: We use various unsupervised summarization models, such as LDA, TextRank, and K-Means clustering 
   * Each model will have its own file, such as `textranks.py`. Inside the file, a "model" function is defined that runs the model over a string (the function signature is described in modeling/README.md)
   * The file calls a summarizer function with the "model" function as an argument. The summarizer function will apply the "model" function to every 10-Q section in the corpus, and concatenate the sections of each 10-Q together to form a summary for each individual 10-Q. 
   * Finally, `validate_model.py` will compute the Jaccard index between the computer-generated summary and our manual summary for a set of validation documents. It outputs a table of the results for each model. 


### Initial Data Pull:
Prior to storing our data in the resources folder, we used https://github.com/alions7000/SEC-EDGAR-text to pull the data to text files.


## Other Notes 
The .py files contain many helper functions called by other py files. However, many of the .py
files contain small-use case examples under an `if __name__ == "__main__"` block. 

If tensorflow fails to install, one potential solution could be to run `python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl` 

### Code Reproducibility Testing
To test code reproducability, we created a blank virtual machine running Ubuntu 18.04 LTS and installed python 3.7 and the supporting packages according to the following procedure: 
* Use virtual box to [run an Ubuntu 18.04 running the command  LTS virtual machine] (https://www.imore.com/how-use-linux-your-mac-using-virtual-machine)
    * A disk size of 20GB should be sufficient for all project requirements, and we recommend running with at least 3 virtual cores
* Python 3.6 should already come with Ubuntu 18.04, and can be invoked using `python3`. However, if for some reason it is not already installed, it can be installed by running `sudo apt install python3.7`, though you will need to manually add this installation to your path. 
* Then, run `sudo apt install python3-pip` to install pip. Pip is can now be invoked with `pip3`
* Upgrade pip to the latest version by running `pip3 install --upgrade pip`. This is necessary to ensure the correct versions of the python dependencies are installed
* Install git with `sudo apt install git`
* Clone the repository with `git clone https://github.com/kunalrye/financialsummary.git`
* Install project dependencies with `pip3 install -r requirements.txt`
    * This may take some time, as setup scripts for installing tensorflow are time intensive
* Note: if running the project from the terminal inside the VM, the project root will need to be added to the system path: 
    * navigate to the project root, and then run `pwd`
    * then, run `PYTHONPATH = <pwd_output>:$PYTHONPATH`
    * finally, run `export PYTHONPATH`. Note, this addition to the python path will only persist for the current terminal instance 
    
    
* To run .ipynb files:
    * the jupyter notebook server dependencies must be installed via `sudo apt install python3-notebook jupyter jupyter-core python-ipykernel`
    * run in the project root, run `jupyter notebook` to start the server, which should automatically start a web client






  





 
