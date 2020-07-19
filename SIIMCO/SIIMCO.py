# coding=utf-8 

import math
import os
from sys import argv
import pandas as pd
import numpy as np
import csv

sta = pd.read_csv('../input/total_statistics.csv')

def vv_in(person):

    mt= [row for row in sta[str(person)].tolist()]
    total_num= sum(mt)
    max_r =max(mt)
    n=0
    for i in mt:
        if i!=0:
            n=n+1
    w_all = 0
    for num in sta[str(person)].tolist():

        if num !=0 and n !=0:
            w_ik = (math.log(1+max_r/num))/n
            w_all = w_all+w_ik

    return w_all
def vv_out(person):

    mt = [row for row in sta.loc[person].tolist()]
    del mt[0]

    total_num= sum(mt)

    max_r =max(mt)
    n=0
    for i in mt:
        if i!=0:
            n=n+1
    w_all = 0
    w_all = 0
    for num in mt:

        if num !=0 and n !=0:
            w_ik = (math.log(1+max_r/num))/n
            w_all = w_all+w_ik

    return w_all
info={}
import operator
for k in sta['ID'].tolist():
    w_in = vv_in(k)
    w_out = vv_out(k)
    w_k=0
    if w_in!=0 or w_out!=0:
        w_k = (w_in+w_out)/(0.8*w_in+0.6*w_out)
    info[k]=w_k

    list_sort = sorted(info.items(), key=lambda x: x[1], reverse=True)

count =0
c_c = 0
total_per_num = len(sta['ID'].tolist())

name = pd.read_csv('../input/criminals.csv')
cri_per_num = len(name['num'].tolist()) # the number of criminals

for key,value in list_sort: 
    count+=1
    if key in name['ID'].tolist():
        c_c=c_c+1
        print (key)
    print(key,value)
    if count>=cri_per_num:# top-k is the number of criminals
        break
#end_p=float((total_per_num-2*(cri_per_num-c_c)))/float(total_per_num)
print(c_c)

print ('Recall:')
r=c_c/cri_per_num
print (r)
print ('Precision:')
p=c_c/cri_per_num
print (p)
f1=2*p*r/(p+r)
print('F1-score:')
print(f1)

