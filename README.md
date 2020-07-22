# SIIMCO-and-LogAnalysis

##1. DATA SET:<tr/>
   The raw data set is ENRON EMAILS DATASET. It can be download from webset： *https://data.world/brianray/enron-email-dataset*.<tr/>
   
   All three systems are applied on the data set after pre-processing. There are remain 47468 emails in the dataset.<tr/>
   
   The namelist of employees, namelist of the criminals, and the pre-processing code can be found at the github:*https://github.com/Sun121sun/ENRON-EMAILS-AND-EMPLOYEE*<tr/>

##2. THE INTRODUCTION OF THE FOLDS:<tr/>
###   1. In SIIMCO folder:<tr/>
      
      Paper:**SIIMCO A forensic investigation tool for identifying the influential members of a criminal organization**.<tr/>
      
      In this system, the emails dataset is constructed as a social network. SIIMCO proposed the formula to calculate the weight of the vertexes in this social network.
      
      SIIMCO.png: It shows a formula which is proposed in SIIMCO.<tr/>
      
      SIIMCO.py: It is the code for rebuild the formula in SIIMCO.png.<tr/>
      
      In this system, a adjacency matrix with weights will be as the input. The value in the adjacency matrix represents the number of emails sent by individuals to the others.<tr/>
      
###   2. In LogAnalysis folder:<tr/>

      Paper:**Detecting criminal organizations in mobile phone networks**.<tr/>
      
      In this system, the emails dataset is constructed as a social network. Then two strategies are employed as main the tools.<tr/>
      
      a.  Girvan and Newman algorithm: it is proposed in the paper *"Community structure in social and biological networks"*.<tr/>
      
      LogAnalysis-GN.py: It is the implement of Girvan and Newman algorithm. <tr/>
      
      A adjacency matrix with weights will be as the input, which represent the number of emails sent by individuals to the others.<tr/>
   
      b.  Fast Newman algorithm: it is proposed in the paper *" Fast algorithm for detecting community structure in networks"*.<tr/>
      
      LogAnalysis-FN.m: It is the implement of Fast Newman algorithm. <tr/>
      
      A adjacency matrix will be as the input, which represent the relationship between the individuals.<tr/>
      
###   3. In ourmethod folder:<tr/>

      In this folder, we released some original codes. Since we have many experimental steps, we share the main function code here.<tr/>
      
      Paper:**NLP-Based Digital Forensic Investigation Platform for Online Communications**.<tr/>
   
      perplexity.py:It is the implementation algorithm for getting perplexity.<tr/>
      
      lda.py:It is the implementation algorithm for getting LDA model.<tr/>
      
      featuresel.py:It contains core codes of our method<tr/>

      
