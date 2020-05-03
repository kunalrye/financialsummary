# Resources
## Folders
The following folders consist of intermediate files for convenience. \
**full_text**: raw text from the 10-Qs, pulled using SEC-EDGAR-text (https://github.com/alions7000/SEC-EDGAR-text/tree/master/src) \
**figures**: contains all image files of figures used in presentation \
**itemized**: Tokenized and section separated 10-Q reports using sep_sections.py \
**legal_filter_test**: output of files from legalfilter.py, input being itemized of test subset \
**legal_filter_train**: output of files from legalfilter.py, input being itemized of train subset \
**figures**: data visualizations \
**filtered**: original files parsed used for data visualization shown in figures \
**validation_set**: validation set for modeling, manually pulled files 

The output of models can be seen in the folders `<model_name>_output_<train/test>`. Train/test indicates whether the 10-Q was in the training or testing set. 


## Files
**call.txt** financial document used for similarity comparison against 10Qs \
**links.txt** contains the links to the html pages of the 10Qs for the companies in \
**10q_commpname** list of companies whose 10Qs we are extracting \
**forward_looking.txt** contains forward looking statements for legal filter removal \
**test_companies.txt & train_companies.txt** contains the companies for test and train \
**ALLTEXT.txt** contains all the manual extraction text in one file of the validation set 


 

 
