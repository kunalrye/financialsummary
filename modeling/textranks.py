import summa

document = open('resources/filtered/0.txt').read()
summarized_doc = summa.summarizer.summarize(document, ratio=.05)
print(summarized_doc)
words = summa.keywords.keywords(document).split()
# summarized_doc = " ".join(summarized_doc)
text_file = open("resources/textrank_files/" + str(0) + ".txt", "w")
text_file.write(summarized_doc)
text_file.close()

# summ_summarized_doc = summa.summarizer.summarize(summarized_doc)
# print(summ_summarized_doc)
import nltk
from nltk.corpus import wordnet

# nltk.download('wordnet') #Run once

unique_lemma = list()
for word in words:
    lemma = wordnet.morphy(word)
    if lemma is not None:
        # print(word, lemma)
        if lemma not in unique_lemma:
            unique_lemma.append(lemma)
    else:
        # print(word, word)
        if lemma not in unique_lemma:
            unique_lemma.append(lemma)
print(f"No of TextRank Keywords = {len(words)}")
print(f"No of Unique Lemma = {len(unique_lemma)}")
print(unique_lemma)
