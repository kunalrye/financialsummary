from modeling.run_model import summarize_test_docs, summarize_train_docs, summarize_company_docs
from modeling.LexRank_Luhn_LSA import LexRankSummary, LuhnSummary, LsaSummary
import os

os.chdir('C:/Users/jsbae/financialsummary/resources/legal_filter_train/ADI')
print(os.getcwd())

# summarize_train_docs('ADI', LexRankSummary(open('ADI_0000006281_20180505_item1.txt')), 'LexRank')

adi_item1 = open('ADI_0000006281_20180505_item1.txt', encoding='utf-8').read().splitlines()
adi_item2 = open('ADI_0000006281_20180505_item2.txt', encoding='utf-8').read().splitlines()
adi_item3 = open('ADI_0000006281_20180505_item3.txt', encoding='utf-8').read().splitlines()
adi_item4 = open('ADI_0000006281_20180505_item4.txt', encoding='utf-8').read().splitlines()
adi_part2 = open('ADI_0000006281_20180505_part2.txt', encoding='utf-8').read().splitlines()
entire_corpus = adi_item1 + adi_item2 + adi_item3 + adi_item4

# discrete tax benefit
# recorded tax expense amount
# europe, japan, china revenue
# liquidity
LexRankSummary(entire_corpus, 10)
print('\n')

# mostly tax and contractual agreements
# records revenue increase and decrease of automotive and consumer end market
LuhnSummary(entire_corpus, 10)
print('\n')

# talks about stock?
# term loans
# talks about ability to produce products due to unstable areas
LsaSummary(entire_corpus, 10)


summarize_company_docs("CDW", LexRankSummary, "lexrank")
summarize_company_docs("CDW", LuhnSummary, "lunhsummary")
summarize_company_docs("CDW", LsaSummary, "lsasummary")


