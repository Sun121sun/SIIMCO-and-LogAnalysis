#coding=UTF-8
import numpy as np
import xlrd
from xlutils.copy import copy
import scipy.io
import pandas as pd
import time
from sklearn.cross_validation import StratifiedKFold
import skfeature.utility.entropy_estimators as ees
import xlsxwriter

from sklearn.naive_bayes import GaussianNB

from sklearn.tree import DecisionTreeClassifier

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import  AdaBoostClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.metrics import f1_score


from sklearn.preprocessing import label_binarize
from scipy import interp
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score


def readexcel(filename):
    """
    read .xlsx file
    """
    data=xlrd.open_workbook(filename)
    table=data.sheet_by_name('Sheet1')
    arr=[]
    for i in range(table.nrows):
        arr.append(table.row_values(i))
    arr=np.array(arr)
    return arr


def read_xlsx(filename):
    """
    separate the feature and label (the last column is label)
    """
    arr=readexcel(filename)
    X=arr[:,:-1]
    y=arr[:,-1]
    m,n=np.shape(X)
    return X,y




def discrete_5(X):
    """
    Box method -5
    """
    sample_row,sample_colum=np.shape(X)
    for i in xrange(sample_colum):
        m=pd.cut(X[:,i],5,labels=[0,1,2,3,4])
        for j in xrange(sample_row):
            X[j,i]=m[j]
    return X



def cfr(X,y,k):
    """
    CFR
    """
    t1=[]
    n_samples, n_features = X.shape
    for i in range(n_features):   #MI
        f = X[:, i]
        t1.append(ees.midd(f, y))
    F=[]
    tt =np.zeros(n_features)

    while len(F)<k:
        if len(F)==0:
            index=t1.index(max(t1))
            F.append(index)
            f_select = X[:, index]
        j_mim = -1000000000000
        for i in xrange(n_features):
            if i not in F:
                fi=X[:, i]
                cmi=ees.cmidd(y,fi ,f_select)
                inter =t1[i]-cmi
                tt[i] +=cmi-inter
                t=tt[i]
                if t> j_mim:
                    j_mim = t
                    idx = i
        F.append(idx)
        f_select = X[:, idx]
    return F






def writestality(filename,dataname,Is,start_pos,flag,select_nub):
   """
   Stored in excel;
   parameter ：filename='name of file'  dataname='name of data set'  Is='results'
        start_pos='the position in excel now'   flag='y/n first create'
        select_nub='the number of features selected'
   """
 
   alg=["CFR"]
   leng=len(alg)
   if flag==1:  #first create
       workbook=xlsxwriter.Workbook(filename)
       worksheet=workbook.add_worksheet()
       worksheet.write(start_pos-1,0,dataname)
       for i in range(leng):
           worksheet.write(start_pos+i,0,alg[i])
       for i in xrange(leng):
           for j in xrange(1,select_nub+1):
               worksheet.write(start_pos+i,j,Is[i][j-1])
       workbook.close()
   else:
       data=xlrd.open_workbook(filename)
       table=data.sheet_by_name('Sheet1')
       wb=copy(data)
       ws = wb.get_sheet(0)
       ws.write(start_pos-1,0,dataname)
       for i in range(leng):
           ws.write(start_pos+i,0,alg[i])
       for i in xrange(leng):
           for j in xrange(1,select_nub+1):
               ws.write(start_pos+i,j,Is[i][j-1])
       wb.save(filename)



def read_data(X,F):
    """
    read the data with the index in F
    """
    data=np.zeros((np.shape(X)[0],len(F)))
    z=0
    for i in F:
        i=int(float(i))
        data[:,z]=X[:,i]
        z=z+1
    return data


def cv(alg_nub):
    """
    using a feature selection method
    """
    flag=1 

    filename=["train_va_test.xlsx"] # the last column is label, the other columns are features

    ttn=[166,166,166] # number of employees (train, validate, test) 
    exceldata=["210"]# the total number of features(topics)
    exceltrain=["train.xlsx"] 
    start_pos=1   
    length=len(filename_t)  
    for i in xrange(length):

        X,y =read_xlsx(filename[i])

        XX=discrete_5(X)
        XX1,y1=XX[:ttn[0]], y[:ttn[0]] # train set
        XX2,y2=XX[ttn[0]:ttn[0]+ttn[1]], y[ttn[0]:ttn[0]+ttn[1]] # validate set
        XX3,y3=XX[ttn[0]+ttn[1]:ttn[0]+ttn[1]+ttn[2]], y[ttn[0]+ttn[1]:ttn[0]+ttn[1]+ttn[2]] #test set

        select_nub=210 # the total number of features (topics)

        FF=[]
        X_train, X_test = XX1, XX2
        y_train, y_test = y1, y2
        F=cfr(X_train,y_train,select_nub)
        print "cfr=",F
        FF.append(F)
        writestality("train/"exceltrain[i],exceldata[0],FF,start_pos,flag,select_nub)



def cv_f1(alg_nub):
    """
    f1-score //same to recall and precision
    """
    flag=1  #
 
    filename=["train_va_test.xlsx"]
    ttn=[166,166,166]
    exceldata=["210"]

    exceltrain=["train1.xlsx"]
    start_pos=0   
    length=len(filename_t) 
    datapos=1
   
    for i in xrange(length):
      
        select_nub=210
        
        X,y =read_xlsx(filename[i])
        
        XX=discrete_5(X)
        print XX.shape
        XX1,y1=XX[:ttn[0]], y[:ttn[0]]
 
        XX2,y2=XX[ttn[0]:ttn[0]+ttn[1]], y[ttn[0]:ttn[0]+ttn[1]]
        XX3,y3=XX[ttn[0]+ttn[1]:ttn[0]+ttn[1]+ttn[2]], y[ttn[0]+ttn[1]:ttn[0]+ttn[1]+ttn[2]]
        print XX2.shape
       
        clf_nb=GaussianNB()
    
        clf_dt = DecisionTreeClassifier()
        clf_lr = LogisticRegression(penalty='l2')
 
        clf_ab = AdaBoostClassifier()
        clf_ld = LinearDiscriminantAnalysis()
 

       
        f1_nbscores=np.zeros((alg_nub,select_nub))
        f1_dtscores=np.zeros((alg_nub,select_nub))
        f1_lrscores=np.zeros((alg_nub,select_nub))
        f1_abscores=np.zeros((alg_nub,select_nub))
        f1_ldscores=np.zeros((alg_nub,select_nub))


        X_train, X_test = XX1, XX2
        y_train, y_test = y1, y2
        train_n = 0
        FF=readF("train/"+str(i+10)+exceltrain[i],alg_nub,datapos)
        max_f =0
        cccc=0
        for an in xrange(alg_nub):
            for k in xrange(1,select_nub+1):
                Fk=FF[an,:k]
                data_tr=read_data(X_train,Fk)
                data_te=read_data(X_test,Fk)

                       
                #======nb分类器======
                 
                clf_nb.fit(data_tr,y_train)
                y_pre=clf_nb.predict(data_te)
                
                s3=f1_score(y_test, y_pre) #f1-score
                #s3=recall_score(y_test, y_pre) #recall
				#s3=precision_score(y_test, y_pre) #precision
                f1_nbscores[an][k-1]=s3
                #======dt分类器======
                
                clf_dt.fit(data_tr,y_train)
                y_pre=clf_dt.predict(data_te)
                
                s4=f1_score(y_test, y_pre)
                
                f1_dtscores[an][k-1]=s4
                
                #======lr分类器======
                
                clf_lr.fit(data_tr,y_train)
                y_pre=clf_lr.predict(data_te)
                s6=f1_score(y_test, y_pre)
                    #scores_lr[train_n][an][k-1]=s6
                f1_lrscores[an][k-1]=s6
                
                #======ab分类器======
                
                clf_ab.fit(data_tr,y_train)
                y_pre=clf_ab.predict(data_te)
                s9=f1_score(y_test, y_pre)
                
                f1_abscores[an][k-1]=s9
                #======ld分类器======
                
                clf_ld.fit(data_tr,y_train)
                y_pre=clf_ld.predict(data_te)
                s10=f1_score(y_test, y_pre)
                
                f1_ldscores[an][k-1]=s10
 
                
            
            print i
        
        writestality("output/new_NB_f1_"+str(i)+".xlsx",exceldata[0],f1_nbscores,datapos,flag,select_nub)
        writestality("output/new_DT_f1_"+str(i)+".xlsx",exceldata[0],f1_dtscores,datapos,flag,select_nub)
        writestality("output/new_lr_f1_"+str(i)+".xlsx",exceldata[0],f1_lrscores,datapos,flag,select_nub)
       
        writestality("output/new_ab_f1_"+str(i)+".xlsx",exceldata[0],f1_abscores,datapos,flag,select_nub)
        writestality("output/new_ld_f1_"+str(i)+".xlsx",exceldata[0],f1_ldscores,datapos,flag,select_nub)
        print str(i)+"----end"
        



def readF(filename,algnub,index):
    """
    read file name
    """
    data=xlrd.open_workbook(filename)
    table=data.sheet_by_name('Sheet1')
    arr=[]
    print table.cell(index-1,0)
    for i in range(algnub):
        #print i+index
        arr.append(table.row_values(i+index,1))
    arr=np.array(arr)
    return arr






if __name__=="__main__":
    start=time.localtime()
    alg_nub=1  #算法个数
    cv(alg_nub)
       
    cv_f1(alg_nub)
    #cv_p(alg_nub)
    #cv_r(alg_nub)
    
    end=time.localtime()
    print "start time=",time.asctime(start)
    print "end time=",time.asctime(end)

