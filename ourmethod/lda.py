# !/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
import csv
from gensim import corpora, models, similarities
from pprint import pprint
import time
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# def load_stopword():
    # '''
    # 加载停用词表
    # :return: 返回停用词的列表
    # '''
    # f_stop = open('input/stopword.txt')
    # sw = [line.strip() for line in f_stop]
    # f_stop.close()
    # return sw

def docs_preprocessor(docs):
    stop_words = set(stopwords.words('english'))

    #word_tokens = word_tokenize(example_sent)
    word_tokens = word_tokenize(docs)

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    return docs
def delete_biaodian(text):

    string = re.sub("[+\.\:\!\/_,$%^*(+\"\')\<\>\[\]+|[+——\-()?【】“”！，。？、~@#￥%……&*（）]+", " ",str(text))

    return string

if __name__ == '__main__':

    print ('1.initialization ------')
    #
    t_start = time.time()
    # stop words
    #stop_words = load_stopword()

    print ('2.read data ------ ')

    f = pd.read_csv('emails.csv',low_memory=False)

    f['content']=f['content'].apply(delete_biaodian)
    f['content']=f['content'].apply(docs_preprocessor)#stop words 
    
    texts = [[word for word in str(line).strip().lower().split()] for line in f['content'].tolist()]

    print ('time consuming is %.3f sectonds' % (time.time() - t_start))

    M = len(texts)
    print ('number of documents：%d' % M)

    print ('3. create the dictionary ------')
    # 
    dictionary = corpora.Dictionary(texts)
    V = len(dictionary)

    print ('4.calculate the vectors------')
    #
    corpus = [dictionary.doc2bow(text) for text in texts]

    print ('5.calculate TF-IDF ------')
    t_start = time.time()
    #
    corpus_tfidf = models.TfidfModel(corpus)[corpus]
    print ('TF-IDF complete，time consuming is %.3f seconds' % (time.time() - t_start))


    num_topics = 210 # you can get this number by the perplexity
   

    matirx_done = [i for i in range(0, num_topics)]
    t_start = time.time()
    passes = 2 # 
    iterations = 6000 #
    workers = 3 # 
    
    lda = models.LdaMulticore(corpus_tfidf, num_topics=num_topics, id2word=dictionary,iterations=iterations, passes=passes, workers=workers, minimum_probability=0.00001)
    
    print ('LDA model complete，the training time is \t%.3f second' % (time.time() - t_start))

    #
    num_show_topic = 10  # 
    print ('7.distribution of topics under random 10 documents：--')
    doc_topics = lda.get_document_topics(corpus_tfidf)  # 
    idx = np.arange(M)
    np.random.shuffle(idx)
    idx = idx[:10]
    for i in idx:
 
        topic = np.array(doc_topics[i])
        topic_distribute = np.array(topic[:, 1])
        # print topic_distribute
        topic_idx = topic_distribute.argsort()[:-num_show_topic-1:-1]
        print (('topic %d - top %d topics ：' % (i, num_show_topic)), topic_idx)
        print (topic_distribute[topic_idx])
    
    # distribution of topics   
    with open("outputemail/"+str(num_topics)+"/enrn_topic.csv","w") as csvfile: #
        writer = csv.writer(csvfile)
        nnn=['num']
        num_all=nnn+matirx_done
        writer.writerow(num_all)
        num_t = 0
        for ti in range(M):
            topic_t = np.array(doc_topics[ti])
            topic_distribute_t = np.array(topic_t[:, 1])
            list_num=[num_t]
            list_all=[]
            for item in list_num:
                list_all.append(item)
            for item in topic_distribute_t:
                list_all.append(item)
            
            writer.writerow(list_all)
            num_t=num_t+1            
    num_show_term = 20   # top-20 words
    print ('8.distribution of words：--')
    with open("outputemail/"+str(num_topics)+"/enrn_topic_word.txt","w") as f:
        #先写入columns_name
        #writer.writerow(["topic_id","word"])
        for topic_id in range(num_topics):
            print ('topic #%d：\t' % topic_id)
            f.write('topic #%d：\r\n' % topic_id)
            term_distribute_all = lda.get_topic_terms(topicid=topic_id, topn=30)
            print (len(term_distribute_all))
            term_distribute = term_distribute_all[:num_show_term]
            term_distribute = np.array(term_distribute)
            term_id = term_distribute[:, 0].astype(np.int)
            #print ('term_id:',term_id)
            print ('words：\t',)
            f.write('words：\r\n')
            for t in term_id:
                print (dictionary.id2token[t],)
                f.write(dictionary.id2token[t]+'\t')
            f.write('\r\n')
            print ('\n  probability：\t', term_distribute[:, 1])
            S='\t'.join(str(num)[1:-1] for num in term_distribute[:, 1])
            f.write(S+'\r\n')
