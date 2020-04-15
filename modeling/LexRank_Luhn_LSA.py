import sumy
import summa
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.reduction import ReductionSummarizer

from modeling.run_model import summarize_test_docs, summarize_train_docs


def LexRankSummary(document, sentences):
    parser = PlaintextParser.from_string(document,Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences)
    results = []
    for sentence in summary:
        results.append(str(sentence))
    return results

def LuhnSummary(document, sentences):
    parser = PlaintextParser.from_string(document,Tokenizer("english"))
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, sentences)
    results = []
    for sentence in summary:
        results.append(str(sentence))
    return results

def LsaSummary(document, sentences):
    parser = PlaintextParser.from_string(document,Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences)
    results = []
    for sentence in summary:
        results.append(str(sentence))
    return results

def EdmundsonSummary(document, sentences):
    parser = PlaintextParser.from_string(document,Tokenizer("english"))
    summarizer = EdmundsonSummarizer()
    summary = summarizer(parser.document, sentences)
    results = []
    for sentence in summary:
        results.append(str(sentence))
    return results

def TextRankSummary(document, sentences):
    parser = PlaintextParser.from_string(document,Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, sentences)
    results = []
    for sentence in summary:
        results.append(str(sentence))
    return results

def SumBasicSummary(document, sentences):
    parser = PlaintextParser.from_string(document,Tokenizer("english"))
    summarizer = SumBasicSummarizer()
    summary = summarizer(parser.document, sentences)
    results = []
    for sentence in summary:
        results.append(str(sentence))
    return results

def KLSummary(document, sentences):
    parser = PlaintextParser.from_string(document,Tokenizer("english"))
    summarizer = KLSummarizer()
    summary = summarizer(parser.document, sentences)
    results = []
    for sentence in summary:
        results.append(str(sentence))
    return results

def ReductionSummary(document, sentences):
    parser = PlaintextParser.from_string(document,Tokenizer("english"))
    summarizer = ReductionSummarizer()
    summary = summarizer(parser.document, sentences)
    results = []
    for sentence in summary:
        results.append(str(sentence))
    return results


#summarize_train_docs(LexRankSummary, "lexrank", True)
#summarize_test_docs(LexRankSummary, "lexrank", True )

#summarize_train_docs(LuhnSummary, "luhn", True)
#summarize_test_docs(LuhnSummary, "luhn", True)

#summarize_train_docs(LsaSummary, "lsa", True)
#summarize_test_docs(LsaSummary, "lsa", True)

summarize_train_docs(SumBasicSummary, "SumBasic", True)
summarize_test_docs(SumBasicSummary, "SumBasic", True)