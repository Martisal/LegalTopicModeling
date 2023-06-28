from gensim import models 
from gensim.corpora import Dictionary
import os

sentences = []
for fname in os.listdir('allStemmed'):
    with open('allStemmed/'+fname,'r') as f:
        sentences.append(f.read())
tokens = [[text for text in doc.split()] for doc in sentences]
dictionary = Dictionary.load('models/dictionary_filnames-50.gensim')
corpus = [dictionary.doc2bow(text) for text in tokens]

for t in range(3,21):
    ldamodel = models.LdaModel.load('models/lda_all_{}topic_15passes_42seed_filnames-50.gensim'.format(t))
            
    cm = models.CoherenceModel(model=ldamodel, dictionary=dictionary, corpus=corpus, texts=tokens)
    c = cm.get_coherence()

    print('{} topics: {}'.format(t,c))
