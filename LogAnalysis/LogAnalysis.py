# -*- coding: utf-8 -*-
#GN_weight
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import sys


sys.path.append('../')

class GN_w:
    def __init__(self, G):
        self.G_copy = G.copy()
        self.G = G
        self.partition = [[n for n in G.nodes()]]
        self.all_Q = [0.0]
        self.max_Q = 0.0

    #Using max_Q to divide communities 
    def run(self):
        while len(self.G.edges()) != 0:
            edges={}
            edges_betweenness_centrality = nx.edge_betweenness_centrality(self.G)
            
            #for e, ebc in edges_betweenness_centrality.items():
                #print(print(self.G.get_edge_data(e[0],e[1])))
            for e, ebc in edges_betweenness_centrality.items():
                #print(self.G.get_edge_data(e[0],e[1]))
                edge_weight = ebc/self.G.get_edge_data(e[0],e[1])['weight']
                edges[e]=edge_weight
                
            edge = max(edges.items(), key=lambda item:item[1])[0]
            self.G.remove_edge(edge[0], edge[1])
            components = [list(c) for c in list(nx.connected_components(self.G))]
            if len(components) != len(self.partition):
            #compute the Q
                cur_Q = self.cal_Q(components, self.G_copy)
                if cur_Q not in self.all_Q:
                    self.all_Q.append(cur_Q)
                if cur_Q > self.max_Q:
                    self.max_Q = cur_Q
                    self.partition = components
                    
        print('-----------the divided communities and the Max Q------------')
        print('The number of Communites:', len(self.partition))
        print('Max_Q:', self.max_Q)
        print(self.partition)
        return self.partition, self.all_Q, self.max_Q
    
    def group(self,node1):
        num1 = 0
        nodegroup1 = {}
        for partition in self.partition:
            for node in partition:
                nodegroup1[node] = {'group':num1}
            num1 = num1 + 1  
        nx.set_node_attributes(self.G_copy, nodegroup1)
        for partition in self.partition:
            for node in partition:
                if node==node1:
                    return nodegroup1[node]['group']
                else:pass
    
    
    def add_group(self):
        num = 0
        nodegroup = {}
        for partition in self.partition:
            for node in partition:
                nodegroup[node] = {'group':num}
            num = num + 1  
        nx.set_node_attributes(self.G_copy, nodegroup)
        return self.partition
        
    def to_gml(self):
        nx.write_gml(self.G_copy, 'output/outtoGN_weighted.gml')
    
	#Computing the Q
    def cal_Q(self,partition,G):
        m = len(G.edges(None, False))
        a = []
        e = []
    
        for community in partition:
            t = 0.0
            for node in community:
                t += len([x for x in G.neighbors(node)])
            a.append(t/(2*m))
        
        for community in partition:
            t = 0.0
            for i in range(len(community)):
                for j in range(len(community)):
                    if(G.has_edge(community[i], community[j])):
                        t += 1.0
            e.append(t/(2*m))
        
        q = 0.0
        for ei,ai in zip(e,a):
            q += (ei - ai**2) 
        return q 
        
if __name__ == '__main__':
    M=nx.read_gml('data.gml')
    G = nx.Graph()
    for u,v,data in M.edges(data=True):
        w = data['weight'] if 'weight' in data else 1.0
        if G.has_edge(u,v):
            G[u][v]['weight'] += w
        else:
            G.add_edge(u, v, weight=w)
    algorithm = GN_w(G)
    algorithm.run()
    zidian=algorithm.add_group()
    algorithm.to_gml()
    
    G1 = nx.read_gml('output/outtoGN_weighted.gml')
    bet_cen = nx.betweenness_centrality(G1)
    bet_cen1 = sorted(bet_cen.items(), key=lambda d:d[1], reverse = True )  
    #print(order_dict(bet_cen,25))
    # Closeness centrality
    clo_cen = nx.closeness_centrality(G1)
    clo_cen1 = sorted(clo_cen.items(), key=lambda d:d[1], reverse = True )  
    # Eigenvector centrality
    eig_cen = nx.eigenvector_centrality(G1)
    eig_cen1 = sorted(eig_cen.items(), key=lambda d:d[1], reverse = True )  
    # Degree centrality
    deg_cen = nx.degree_centrality(G1)
    deg_cen1 = sorted(deg_cen.items(), key=lambda d:d[1], reverse = True ) 
    
    
    criminals=pd.read_csv('output/criminals.csv')
    n=len(criminals['num']) # the nimber
    bet_cen2=bet_cen1[:n]
    clo_cen2=clo_cen1[:n]
    eig_cen2=eig_cen1[:n]
    deg_cen2=deg_cen1[:n]
    result1 = []
    for i in range(n):
        result1.append(bet_cen2[i][0])
    print (result1)
    result2 = []
    for i in range(n):
        result2.append(clo_cen2[i][0])
    print (result2)
    result3 = []
    for i in range(n):
        result3.append(eig_cen2[i][0])
    print (result3)
    result4 = []
    for i in range(n):
        result4.append(deg_cen2[i][0])
    print (result4)
    

    print('---------------------------')
    print('betweenness_centrality')
    j=0
    for i in result1:
        #print(type(i))
        for k in criminals['num'].tolist():
            #print(k)
            if int(i)==k:
                print (i)
                j+=1
    print(j)
    print('---------------------------')
    print('closeness_centrality')
    j=0
    for i in result2:
        #print(type(i))
        for k in criminals['num'].tolist():
            #print(k)
            if int(i)==k:
                print (i)
                j+=1
    print(j)
    print('---------------------------')
    print('eigenvector_centrality')
    j=0
    for i in result3:
        #print(type(i))
        for k in criminals['num'].tolist():
            #print(k)
            if int(i)==k:
                print (i)
                j+=1
    print(j)
    print('---------------------------')
    print('degree_centrality')
    j=0
    for i in result4:
        #print(type(i))
        for k in criminals['num'].tolist():
            #print(k)
            if int(i)==k:
                print (i)
                j+=1
    print(j)
    print('---------------------------')
