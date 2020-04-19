# The embeddings we have chosen here require a lot of memory.\
import os
import gensim
import pickle
from time import time
start = time()
os.chdir('C:/Users/jsbae/financialsummary')
print('starting embedding...')
model = gensim.models.KeyedVectors.load_word2vec_format('C:/Users/jsbae/Downloads/GoogleNews-vectors-negative300.bin.gz', binary=True)
print('Cell took %.2f seconds to run.' % (time() - start))

# with open('store.pkl', 'rb') as f:
  #   model = pickle.load(f)

kl = open('resources/KL_output_test/AAPL/AAPL_0000320193_20180630.txt', encoding='utf-8').read().splitlines()
generated = open('resources/validation_set/AAPL_0000320193_20180630.txt', encoding='utf-8').read().splitlines()
sumbasic = open('resources/SumBasic_output_test/AAPL/AAPL_0000320193_20180630.txt', encoding='utf-8').read().splitlines()
reduction = open('resources/Reduction_output_test/AAPL/AAPL_0000320193_20180630.txt', encoding='utf-8').read().splitlines()


def compute_word_mover(manual_set, generated_set):
    """
    Computes the precision of the generated summary
    Precision is the fraction of relevant instances among the retrieved instances
    :param manual_set:
    :param generated_set:
    :return: value which shows how similar the two are (made it negative to pull maximum score)
    """

    distance = -model.wmdistance(manual_set, generated_set)
    return distance

compute_word_mover(sumbasic, generated)
compute_word_mover(reduction, generated)
compute_word_mover(kl, generated)