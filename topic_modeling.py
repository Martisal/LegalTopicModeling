import gensim
import os
from gensim import corpora, models
from gensim.corpora import Dictionary
import sys
import pickle

sentences = []
names = []

for fname in os.listdir('parsed/'):
    with open('parsed/'+fname,'r') as f:
        sentences.append(f.read())
        names.append(fname)

tokens = [[text for text in doc.split()] for doc in sentences]
dictionary = corpora.Dictionary(tokens)

corpus = [dictionary.doc2bow(text) for text in tokens]

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

pickle.dump(corpus_tfidf, open('models/corpus.pickle', 'wb'))
dictionary.save('models/dictionary.gensim')

for i in range(3,21):
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=i, id2word=dictionary, passes=15)
    ldamodel.save('models/lda_all_{}topic_{}passes_42seed_filnames-50.gensim'.format(i,15))

    print('TOPIC MODELLING WITH', i, 'TOPICS, ({} PASSES LDA)'.format(15))
    print()
    topics = ldamodel.print_topics(num_words=5)
    for topic in topics:
        print(topic)
    print()

