# !/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
import csv
from gensim import corpora, models, similarities
from pprint import pprint
import time
import pandas as pd
import nltk
import re
import math
#from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def load_stopword():
    '''
    stop words
    '''
    f_stop = open('input/stopword.txt')
    sw = [line.strip() for line in f_stop]
    f_stop.close()
    return sw
def docs_preprocessor(docs):
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(docs)

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    return docs
def delete_biaodian(text):

    string = re.sub("[+\.\:\!\/_,$%^*(+\"\')\[\]+|[+——\-()?【】“”！，。？、~@#￥%……&*（）]+", " ",str(text))

    return string

def lda_train(corpus_tfidf, num_topics=30, id2word=None, iterations=5000, passes=1, workers=3):
    t_start = time.time()
    lda = models.LdaMulticore(corpus_tfidf, num_topics=num_topics, id2word=dictionary,iterations=iterations, passes=passes, workers=workers, minimum_probability=0.001)
    print ('LDA model complete，the training time is \t%.3f second' % (time.time() - t_start))
    
 
    lda.save('outputemail/'+str(num_topics)+'/lda_%s_%s.model'%(num_topics, iterations)) # save the model


def perplexity(ldamodel, testset, dictionary, size_dictionary, num_topics):
    """calculate the perplexity of a lda-model"""
    # dictionary : {7822:'deferment', 1841:'circuitry',19202:'fabianism'...]
    print ('the info of this ldamodel: \n')
    print ('num of testset: %s; size_dictionary: %s; num of topics: %s'%(len(testset), size_dictionary, num_topics))
    prep = 0.0
    prob_doc_sum = 0.0
    topic_word_list = [] # store the probablity of topic-word:[(u'business', 0.010020942661849608),(u'family', 0.0088027946271537413)...]
    for topic_id in range(num_topics):
        topic_word = ldamodel.show_topic(topic_id, size_dictionary)
        dic = {}
        for word, probability in topic_word:
            dic[word] = probability
        topic_word_list.append(dic)
    doc_topics_ist = [] #store the doc-topic tuples:[(0, 0.0006211180124223594),(1, 0.0006211180124223594),...]
    for doc in testset:

        doc_topics_ist.append(ldamodel.get_document_topics(doc, minimum_probability=0))
    testset_word_num = 0
    for i in range(len(testset)):
        prob_doc = 0.0 # the probablity of the doc
        doc = testset[i]
        doc_word_num = 0 # the num of words in the doc
        for word_id, num in doc:
            prob_word = 0.0 # the probablity of the word 
            doc_word_num += num
            word = dictionary[word_id]
            for topic_id in range(num_topics):
                # cal p(w) : p(w) = sumz(p(z)*p(w|z))
                prob_topic = doc_topics_ist[i][topic_id][1]
                prob_topic_word = topic_word_list[topic_id][word]
                prob_word += prob_topic*prob_topic_word
            prob_doc += math.log(prob_word) # p(d) = sum(log(p(w)))
        prob_doc_sum += prob_doc
        testset_word_num += doc_word_num
    print (prob_doc_sum)
    print (testset_word_num)
    prep = math.exp(-prob_doc_sum/testset_word_num) # perplexity = exp(-sum(p(d)/sum(Nd))
    print ("the perplexity of this ldamodel is : %s"%prep)
    return prep







if __name__ == '__main__':

    print ('1.initialization ------')
    # start time 
    t_start = time.time()
    # stop words
    #stop_words = load_stopword()

    print ('2.read data ------ ')


    f = pd.read_csv('output/emails_use.csv',low_memory=False)

    f['content']=f['content'].apply(delete_biaodian)
    f['content']=f['content'].apply(docs_preprocessor)
    #texts = [[word for word in line.strip().lower().split() if word not in stop_words] for line in f]
    texts = [[word for word in str(line).strip().lower().split()] for line in f['content'].tolist()]

    print ('time consuming is %.3f sectonds' % (time.time() - t_start))
    #f.close()
    M = len(texts)
    print ('number of documents：%d' % M)

    print ('3. create the dictionary ------')
    # 
    dictionary = corpora.Dictionary(texts)
    dictionary.save('dictionary.dictionary')
    V = len(dictionary)

    print ('4.calculate the vectors ------')

    corpus = [dictionary.doc2bow(text) for text in texts]
    print(type(corpus))
    print ('5.calculate TF-IDF ------')
    t_start = time.time()

    corpus_tfidf = models.TfidfModel(corpus)[corpus]
    print (' TF-IDF complete，time consuming is %.3f seconds' % (time.time() - t_start))

    # train 
    
    f_test = pd.read_csv('140yu.csv',low_memory=False)# you can load the whole data or just some of them.

    f_test['content']=f_test['content'].apply(delete_biaodian)
    f_test['content']=f_test['content'].apply(docs_preprocessor)
    testset = [[word for word in str(line).strip().lower().split()] for line in f_test['content'].tolist()]

    corpus_test = [dictionary.doc2bow(text) for text in testset]
    passes = 2 
    iterations = 6000
    workers = 3 
    for n in range (250):
        num_topics = (n+1)*10
        print('the number of topics trained in this time is：')
        print (num_topics)
        lda_train(corpus_tfidf, num_topics=num_topics, id2word=dictionary, iterations=iterations, passes=passes, workers=workers)

        ldamodel_path= 'outputemail/'+str(num_topics)+'/lda_'+str(num_topics)+'_'+str(iterations)+'.model'
        lda_multi=models.ldamodel.LdaModel.load(ldamodel_path)
        prep = perplexity(lda_multi, corpus_test, dictionary, len(dictionary.keys()), num_topics)
        f2 = open('perplexity.txt','a')
        f2.write(str(num_topics)+'\,'+str(prep)+'\n')
        f2.close()