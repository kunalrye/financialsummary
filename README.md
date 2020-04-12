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

## Code Reproducibility Testing
To test code reproducability, we created a blank ivirtual machine running Ubuntu 18.04 LTS and installed python 3.7 and the supporting packages according to the following procedure: 
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






  





 
