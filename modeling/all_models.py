"""
Regenerates the summaries for all documents
"""

from modeling.LexRank_Luhn_LSA import LexRankSummary, LsaSummary, LuhnSummary, ReductionSummary, KLSummary, EdmundsonSummary,  SumBasicSummary
from modeling.lda import do_lda
from modeling.textranks import textrank_summarize
from modeling.run_model import summarize_test_docs, summarize_train_docs


summarize_train_docs(LexRankSummary, "lexrank", True)
summarize_test_docs(LexRankSummary, "lexrank", True )

summarize_train_docs(LuhnSummary, "luhn", True)
summarize_test_docs(LuhnSummary, "luhn", True)

summarize_train_docs(LsaSummary, "lsa", True)
summarize_test_docs(LsaSummary, "lsa", True)

summarize_train_docs(KLSummary, "KL", True)
summarize_test_docs(KLSummary, "KL", True)

summarize_train_docs(ReductionSummary, "Reduction", True)
summarize_test_docs(ReductionSummary, "Reduction", True)

summarize_train_docs(SumBasicSummary, "SumBasic", True)
summarize_test_docs(SumBasicSummary, "SumBasic", True)

summarize_train_docs(textrank_summarize, "textrank", True)
summarize_test_docs(textrank_summarize, "textrank", True)

summarize_train_docs(do_lda, "lda", True)
summarize_test_docs(do_lda, "lda", True)

