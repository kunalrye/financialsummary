"""
Takes a document path and returns MMR summaries for each document in that directory 
"""

import nltk
import os
import math
import string
import re
import sentence
from nltk.corpus import stopwords

def doc_to_tfidf(document_path):
	"""
	takes a document and tokenizes to sentences
	"""
	with open(document_path, 'r') as in_file:
    text = in_file.read()
    sents = nltk.sent_tokenize(text)
    term_freq = {}
    len_sents = len(sents)
    inverse_docfreq = 0
    idf = {}
    words = {}
    check = []
	for sent in sents:
	    word_freqs = sent.getWordFreq()
	    for word in word_freqs.keys():
	        if term_freq.get(word, 0) != 0:				
				term_freq[word] = term_freq[word] + wordFreqs[word]
	        else:				
				term_freq[word] = wordFreqs[word]	
		for word in sent.getPreProWords():
			if sent.getWordFreq().get(word,0) != 0:
				words[word] = words.get(word, 0) + 1
		for word in words:
			n = words[word]
			try:
				check.append(n)
				idf = math.log10(float(len_sents)/n)
			except ZeroDivisionError:
				idf = 0

			idf[word] = inverse_docfreq
	return sents, term_freq, idf


def tfidf(docpath):
	tf = doc_to_tfidf(docpath)[1]
	idf = doc_to_tfidf(docpath)[2]
	dict_tfidf = {}

	for word in tf:
		tfidf = tf[word] * idf[word]

		if dict_tfidf.get(tfidf, None) == None:
			dict_tfidf[tfidf] = [word]
		else:
			dict_tfidf[tfidf].append(word)

	return dict_tfidf


def sentenceSim(sentence1, sentence2, IDF_w):
	numerator = 0
	denominator = 0	
	
	for word in sentence2.getPreProWords():		
		numerator+= sentence1.getWordFreq().get(word,0) * sentence2.getWordFreq().get(word,0) *  IDF_w.get(word,0) ** 2

	for word in sentence1.getPreProWords():
		denominator+= ( sentence1.getWordFreq().get(word,0) * IDF_w.get(word,0) ) ** 2

	# check for divide by zero cases and return back minimal similarity
	try:
		return numerator / math.sqrt(denominator)
	except ZeroDivisionError:
		return float("-inf")	


def buildQuery(sentences, TF_IDF_w, n):
	#sort in descending order of TF-IDF values
	scores = TF_IDF_w.keys()
	scores.sort(reverse=True)	
	
	i = 0
	j = 0
	queryWords = []

	# select top n words
	while(i<n):
		words = TF_IDF_w[scores[j]]
		for word in words:
			queryWords.append(word)
			i=i+1
			if (i>n): 
				break
		j=j+1

	# return the top selected words as a sentence
	return sentence.sentence("query", queryWords, queryWords)


def bestSentence(sentences, query, IDF):
	best_sentence = None
	maxVal = float("-inf")

	for sent in sentences:
		similarity = sentenceSim(sent, query, IDF)		

		if similarity > maxVal:
			best_sentence = sent
			maxVal = similarity
	sentences.remove(best_sentence)

	return best_sentence


def makeSummary(sentences, best_sentence, query, summary_length, lambta, IDF):	
	summary = [best_sentence]
	sum_len = len(best_sentence.getPreProWords())

	MMRval={}

	# keeping adding sentences until number of words exceeds summary length
	while (sum_len < summary_length):	
		MMRval={}		

		for sent in sentences:
			MMRval[sent] = MMRScore(sent, query, summary, lambta, IDF)
		
		maxxer = max(MMRval, key=MMRval.get)
	 	summary.append(maxxer)
		sentences.remove(maxxer)
		sum_len += len(maxxer.getPreProWords())	

	return summary


def MMRScore(Si, query, Sj, lambta, IDF):	
	Sim1 = sentenceSim(Si, query, IDF)
	l_expr = lambta * Sim1
	value = [float("-inf")]

	for sent in Sj:
		Sim2 = sentenceSim(Si, sent, IDF)
		value.append(Sim2)

	r_expr = (1-lambta) * max(value)
	MMR_SCORE = l_expr - r_expr	

	return MMRScore


if __name__=='__main__':	

	# set the main Document folder path where the subfolders are present
	main_folder_path = os.getcwd() + "/Documents"

	# read in all the subfolder names present in the main folder
	for folder in os.listdir(main_folder_path):
		
		print "Running MMR Summarizer for files in folder: ", folder 
		# for each folder run the MMR summarizer and generate the final summary
		curr_folder = main_folder_path + "/" + folder		

		# find all files in the sub folder selected
		files = os.listdir(curr_folder)

		sentences = []	

		for file in files:			
			sentences = sentences + processFile(curr_folder + "/" + file)

		# calculate TF, IDF and TF-IDF scores
		# TF_w 		= TFs(sentences)
		IDF_w 		= IDFs(sentences)
		TF_IDF_w 	= TF_IDF(sentences)	

		# build query; set the number of words to include in our query
		query = buildQuery(sentences, TF_IDF_w, 10)		

		# pick a sentence that best matches the query	
		best1sentence = bestSentence(sentences, query, IDF_w)		

		# build summary by adding more relevant sentences
		summary = makeSummary(sentences, best1sentence, query, 100, 0.5, IDF_w)
		
		final_summary = ""
		for sent in summary:
			final_summary = final_summary + sent.getOriginalWords() + "\n"
		final_summary = final_summary[:-1]
		results_folder = os.getcwd() + "/MMR_results"		
		with open(os.path.join(results_folder,(str(folder) + ".MMR")),"w") as fileOut: fileOut.write(final_summary)
	