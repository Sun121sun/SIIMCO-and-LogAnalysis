import scipy.io as sio

crims = []
crim = [2,6,9,11,12,20,28,29,39,49,59,66,79,78,80,81,89,97,112,118,126,127,131,143,158]
for cr in crim:
    crims.append(cr+1)

res = {}
cluster = []
data = sio.loadmat('result.mat')
inter=[]
for arrs in data['c_newman'][0]:
    for arr in arrs:
        inter.append(len(list(set(crims).intersection(arr))))
        pp.append(inter)

n=max(inter)
c=inter.index(p)
p=n/len(crims)
r=n/len(data['c_newman'][0][c][0])
f1=2*p*r/(p+r)
print('P:{}'.format(p))
print('R：{}'.format(r))
print('F1：{}'.format(r))   