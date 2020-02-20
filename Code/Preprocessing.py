#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Preprocessing.py
import os
import csv
import math
import string
import numpy as np
import networkx as nx
from makegraph import mgraph
G=nx.MultiDiGraph()
nodes_data={}
edges_data={}
(G,nodes_data,edges_data)=mgraph()

def distributers():
	distributers=[]
	for n in G.nodes():
		in_deg=G.in_edges(nbunch=n,keys=True,data=True)
		c=0
		#print in_deg
		for kk in in_deg:
			if float(kk[3]['voltages'])>=115000:
				c+=1
		del in_deg[:]
		if c==1:
			#print n
			distributers.append(n)
	return distributers
	
def preprocessing():
	'''removing isolated nodes'''
	isolated=nx.isolates(G)
	for j in isolated:
		for key in nodes_data.keys():
			if j == key:
				del nodes_data[key]
				G.remove_node(j)
				#print G.number_of_nodes(), len(nodes_data)
				continue
	for k in edges_data.keys():
		'''deleting all edges from edges_data which no more exist''' 
		if not G.has_edge(edges_data[k][1],edges_data[k][2],key=k):
			#print len(edges_data)
			del edges_data[k]
	gen=[]
	indegree=G.in_degree(G.nodes())
	'''number of nodes with no in_degree'''
	'''removing joints,merge nodes categorised as generators from graph and node data'''
	t=0
	for i in indegree:
		if indegree[i]==0:
			if nodes_data[i][3]=='merge' or nodes_data[i][3]=='joint':
				continue
			gen.append(i)
	for node,nd in nodes_data.iteritems():
		'''adding plants to generators'''
		if nd[3]== 'plant' and nd[0] not in gen:
			gen.append(node)
	voltages={}
	z=0
	for aa,val in edges_data.iteritems():
		'''adding edge attributes'''
		z+=1
		#print z
		if edges_data[aa][3].find(';')!= -1:
			xx=map(float,edges_data[aa][3].split(';'))
			edges_data[aa][3]=max(xx)
			del xx[:]
		elif edges_data[aa][3]=='':
			edges_data[aa][3]=np.nan
		else:
			edges_data[aa][3]=float(edges_data[aa][3])
		if val[4].find(';')!= -1:
			xy=map(float,val[4].split(';'))
			val[4]=sum(xy)
			del xy[:]
		else:
			val[4]=float(val[4])
		voltages[(val[1],val[2],val[0])]=val[3]
	nx.set_edge_attributes(G,'voltages',voltages)
	distr=distributers();
	for f in gen:
		if f in distr:
			distr.remove(f)
			#G.remove_edges_from(G.in_edges(f))
		if node in gen:
			nodes_data[node][3]='generators'
		elif node in distr:
			nodes_data[node][3]='distributors'
		else:
			nodes_data[node][3]='transmitters'
	for ab,v in nodes_data.iteritems():
		'''adding nodes attributes'''
		if v[4].find(';')!= -1:
			ss=map(float,v[4].split(';'))
			if v[3]=='generator' or v[3]=='distributor':
				v[4]=min(ss)
			else:
				v[4]=max(ss)
			del ss[:]
		elif v[4]=='':
			v[4]=np.nan
		else:
			v[4]=float(v[4])
	'''removing multi edges'''
	for x in G.nodes():
		for y in G.nodes():
			if x==y:
				continue
			if G.number_of_edges(x,y)>1:
				kkk=[]
				for ee in list(G.edges(x,keys=True)):
					if ee[0]==x and ee[1]==y:
						kkk.append(ee[2])
				for l in range(1,len(kkk)):
					edges_data[kkk[0]][4]+=edges_data[kkk[l]][4]
					edges_data[kkk[0]][3]=max(edges_data[kkk[0]][3],edges_data[kkk[l]][3])
					del edges_data[kkk[l]]
					G.remove_edge(x,y,key=kkk[l])
				G[x][y][kkk[0]]['cable']=edges_data[kkk[0]][4]
				G[x][y][kkk[0]]['voltages']=edges_data[kkk[0]][3]
	#return (G,nodes_data,edges_data)
	o=[]
	with open('../../NS_project/Data/Vertices_new.csv', 'wb') as csvfile:
		nodewriter = csv.writer(csvfile, delimiter=',')
		header=['v_id','lon','lat','typ','voltage']
		nodewriter.writerow(header)
		for da,it in nodes_data.iteritems():
			for l in range(0,5):
				o.append(str(it[l]))
			nodewriter.writerow(o)
			del o[:]
	with open('../../NS_project/Data/Edges_new.csv', 'wb') as csvfile1:
		edgewriter = csv.writer(csvfile1, delimiter=',')
		header1=['l_id','v_id_1','v_id_2','voltage','cables','length_m']
		edgewriter.writerow(header1)
		for db,itt in edges_data.iteritems():
			for l in range(0,5):
				o.append(str(itt[l]))
			o.append(str(itt[10]))
			edgewriter.writerow(o)
			del o[:]
	return G
preprocessing()
