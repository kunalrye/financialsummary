import summa
from modeling.run_model import summarize_test_docs, summarize_train_docs



def textrank_summarize(doc, num_sents):
    if (len(doc.splitlines())) == 0:
        return []

    p = num_sents / len(doc.splitlines())

    summarized_section = summa.summarizer.summarize(doc, ratio=p) # textrank!
    return summarized_section.splitlines()


summarize_train_docs(textrank_summarize, "textrank")
summarize_test_docs(textrank_summarize, "textrank")