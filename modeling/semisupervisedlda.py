"""
A semi-supervised LDA (Latent Dirichlet Allocation) model to summarize financial documents.

Creates a target topic vector from the training vectors. 10Qs are summarized by taking the k sentences
whose topic vectors are most similar (via inner product) to the target topic vector
"""
from modeling.topic_coverage import *
model = TopicCoverageValidation()
training_vectors = model.get_training_sent_topic_vectors()
AVG_VEC = np.mean(training_vectors,axis=0)

def semisupervised_lda(text,NUM_SENTS):
    """
    Implements the semisupervised lda model that can be run on a single 10Q section (approach outlined above)
    :param text: the document as a string
    :param NUM_SENTS: k, the number of sentences we want the model to extract
    :return: a list of sentences (the summmary)
    """
    sents = text.splitlines()
    if NUM_SENTS == 0 or len(sents) == 0:
        return []

    lda_vecs = model.get_sent_topics(sents)
    if not lda_vecs:
        return []

    sent_ranking = np.flip(np.argsort(np.dot(np.asarray(lda_vecs),AVG_VEC)))
    if(NUM_SENTS<=len(sent_ranking)):
        ranked_idx = list(sent_ranking[:NUM_SENTS])
        return list(np.asarray(sents)[ranked_idx])
    else:
        return sents


summarize_train_docs(semisupervised_lda, "semisup_topic", True)
summarize_test_docs(semisupervised_lda, "semisup_topic", True)