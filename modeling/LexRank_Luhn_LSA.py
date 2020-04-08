import sumy
import summa
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from modeling.run_model import summarize_test_docs, summarize_train_docs


def LexRankSummary(document, sentences):
    parser = PlaintextParser.from_string(document,Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences)
    # for sentence in summary:
    #     print(sentence)
    return summary

def LuhnSummary(document, sentences):
    parser = PlaintextParser.from_string(document,Tokenizer("english"))
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, sentences)
    # for sentence in summary:
    #     print(sentence)
    return summary

def LsaSummary(document, sentences):
    parser = PlaintextParser.from_string(document,Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences)
    # for sentence in summary:
    #     print(sentence)
    return summary

summarize_train_docs(LexRankSummary, "lexrank")
summarize_test_docs(LexRankSummary, "lexrank")

#summarize_train_docs(LuhnSummary, "luhn")
#summarize_test_docs(LuhnSummary, "luhn")

#summarize_train_docs(LsaSummary, "lsa")
#summarize_test_docs(LsaSummary, "lsa")