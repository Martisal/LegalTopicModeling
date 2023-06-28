from gensim import models
import sys
import pickle
from sklearn.metrics import silhouette_score, silhouette_samples
import numpy as np
from gensim.corpora import Dictionary

def print_topics(ldam):
    topics = ldam.print_topics(num_words=5)
    for topic in topics:
        print(topic)

def topic_distribution(corpus, model):
    """
    Return the topics for each document, sorted by probability
    """
    topic_dist = []
    for doc in corpus:
        dist = model.get_document_topics(doc)
        topic_dist.append(sorted(dist, key=lambda tup: tup[1], reverse=True))
    return topic_dist

if __name__=='__main__':
    """
    if len(sys.argv) == 1:
        ldamodel = models.LdaModel.load('models/lda_all_4topic_15passes.gensim')
    else:
        ldamodel = models.LdaModel.load(sys.argv[1])
    """

    with open('models/corpus_filnames-50.pickle', 'br') as cf:
        tfidf = pickle.load(cf)

    dictionary = Dictionary.load('models/dictionary_filnames-50.gensim')    
    ldamodel = models.LdaModel.load('models/lda_all_15topic_15passes_42seed_filnames-50.gensim')

    tdist = []
    for doc in tfidf:
        dist = ldamodel.get_document_topics(doc)
        distall = []
        i = 0
        for t in dist:
            while i < 15 and t[0] > i:
                distall.append(0)
                i += 1
            distall.append(t[1])
            i += 1
        while i < 15:
            distall.append(0)
            i += 1

        tdist.append(distall)

    with open('results/tdist.pickle', 'bw') as tf:
        pickle.dump(tdist, tf)    

    """
    tfidflist = []
    for d in tfidf:

        vec = []
        cur = d[0][0]
        pos = 0
        
        for i in range(len(dictionary)):

            if i != cur:
                vec.append(0)
            elif pos < len(d)-1:
                vec.append(d[pos][1])
                pos += 1
                cur = d[pos][0]
            else:
                vec.append(d[pos][1])    

        tfidflist.append(vec)  

    with open('data/tfidf_all_dense_filnames-50.pickle', 'bw') as tf:
        pickle.dump(tfidflist, tf)

    sil_all = []
    for i in range(3,21):    
        print('Loading model...')    
        ldamodel = models.LdaModel.load('models/lda_all_{}topic_15passes_42seed_filnames-50.gensim'.format(i))
        print('Computing topic distribution...')
        tdist = topic_distribution(tfidf, ldamodel)
        print('Building labels')
        labels = []
        for t in tdist:
            labels.append(t[0][0])
        print('Computing silhouette score')
        s = silhouette_score(tfidflist, labels, metric='cosine') 
        print('Silhouette score for {} topics: {}'.format(i,s))
        print('Computing silhouette samples')
        sil_all.append((silhouette_samples(tfidflist, labels, metric='cosine'), labels))
        
   
    print('Saving results')    
    #Silhouette file is a list:
    #    - each element represents a different number of topics
    #    - each element is a tuple (sil_samples, labels)
    with open('results/silhouette_3-20topic_filnames-50.pickle', 'bw') as sf:
        pickle.dump(sil_all, sf)
    """
