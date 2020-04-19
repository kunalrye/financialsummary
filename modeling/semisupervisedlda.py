from modeling.topic_coverage import *
model = TopicCoverageValidation()
training_vectors = model.get_training_sent_topic_vectors()
AVG_VEC = np.mean(training_vectors,axis=0)

def semisupervised_lda(text,NUM_SENTS):
    sents = text.splitlines()
    if NUM_SENTS == 0 or len(sents) == 0:
        return []

    lda_vecs = model.get_sent_topics(sents)
    if not lda_vecs:
        return []

    # max_vecs = []
    # for vec in lda_vecs:
    #     max_idx = np.argmax(np.dot(np.asarray(vectors), vec))
    #


    sent_ranking = np.flip(np.argsort(np.dot(np.asarray(lda_vecs),AVG_VEC)))
    if(NUM_SENTS<=len(sent_ranking)):
        ranked_idx = list(sent_ranking[:NUM_SENTS])
        return list(np.asarray(sents)[ranked_idx])
    else:
        return sents


    # score_matrix = np.matmul(np.asarray(lda_vecs),np.transpose(np.asarray(training_vectors)))
    # row_maxes = np.amax(score_matrix,axis=1) # take the max of each row

    
    # sent_ranking = np.flip(np.argsort(row_maxes))
    # if(NUM_SENTS<=len(sent_ranking)):
    #     ranked_idx = list(sent_ranking[:NUM_SENTS])
    #     return list(np.asarray(sents)[ranked_idx])
    # else:
    #     return sents

summarize_train_docs(semisupervised_lda, "semisup_topic", True)
summarize_test_docs(semisupervised_lda, "semisup_topic", True)