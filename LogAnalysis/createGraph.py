#GN_weight
import pandas as pd

total_statistics=pd.read_csv('input/total_statistics.csv')

with open('output/data.gml','w') as f:    #
    f.write("graph\n")
    f.write("[\n")

    for i in total_statistics['ID'].tolist():
        f.write("node\n")
        f.write("[\n")
        f.write("id "+str(i)+"\n")
        f.write("label \""+str(i)+"\"\n")
        f.write("]\n")
    for i in total_statistics['ID'].tolist():
        k=0
        for j in total_statistics[str(i)]:
            if j!=0:
                f.write("edge\n")
                f.write("[\n")
                f.write("source "+str(k)+"\n")
                f.write("target "+str(i)+"\n")
                f.write("weight "+str(j)+"\n")
                f.write("]\n")
            k+=1
    f.write("]")
