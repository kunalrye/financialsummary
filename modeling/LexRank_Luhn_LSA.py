import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer

def LexRankSummary(file, sentences):
    parser = PlaintextParser.from_file(file, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences)
    for sentence in summary:
        print(sentence)

def LuhnSummary(file, sentences):
    parser = PlaintextParser.from_file(file, Tokenizer("english"))
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, sentences)
    for sentence in summary:
        print(sentence)

def LsaSummary(file, sentences):
    parser = PlaintextParser.from_file(file, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences)
    for sentence in summary:
        print(sentence)

#LexRankSummary('C:/Users/sotoa/financialsummary/resources/legal_filter/AAPL/AAPL_0000320193_20171230_item2.txt', 10)
#LuhnSummary('C:/Users/sotoa/financialsummary/resources/legal_filter/AAPL/AAPL_0000320193_20171230_item2.txt', 10)
#LsaSummary('C:/Users/sotoa/financialsummary/resources/legal_filter/AAPL/AAPL_0000320193_20171230_item2.txt', 10)