from validation.topic_coverage import *
model = TopicCoverageValidation()
vectors = model.get_manual_topic_vectors()
AVG_VEC = np.mean(vectors,axis=0)

def semisupervised_lda(text,NUM_SENTS):
    lda_vecs = model.get_sent_topics(text)
    sent_ranking = np.flip(np.argsort(np.dot(lda_vecs,AVG_VEC)))
    if(NUM_SENTS<=len(sent_ranking)):
        ranked_idx = list(sent_ranking[:NUM_SENTS])
        return list(np.asarray(text)[ranked_idx])
    else:
        return(text)

summarize_train_docs(semisupervised_lda, "semisup_topic", True)
summarize_test_docs(semisupervised_lda, "semisup_topic", True)