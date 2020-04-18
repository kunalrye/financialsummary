from validation.topic_coverage import *
model = TopicCoverageValidation()
vectors = model.get_manual_topic_vectors()
AVG_VEC = np.mean(vectors,axis=0)

def semisupervised_lda(text,NUM_SENTS):
    sents = text.splitlines()
    if NUM_SENTS == 0 or len(sents) == 0:
        return []

    lda_vecs = model.get_sent_topics(sents)
    if not lda_vecs:
        return []

    max_vecs = []
    for vec in lda_vecs:
        max_idx = np.flip(np.argsort(np.dot(np.asarray(vectors), vec)))[0]


    sent_ranking = np.flip(np.argsort(np.dot(np.asarray(lda_vecs),AVG_VEC)))
    if(NUM_SENTS<=len(sent_ranking)):
        ranked_idx = list(sent_ranking[:NUM_SENTS])
        return list(np.asarray(sents)[ranked_idx])
    else:
        return sents

summarize_train_docs(semisupervised_lda, "semisup_topic", True)
summarize_test_docs(semisupervised_lda, "semisup_topic", True)