#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  most_cascadenodes_forida.py
import networkx as nx
import csv
from original_graph import graph
from Florida_cascade import florida
import copy

G=nx.DiGraph()
nodes_data={}
edges_data={}
(G,nodes_data,edges_data)=graph()
def nodes_cascaded():
	florida_nodes=[]
	cascade={}
	for jj,val in nodes_data.items():
		if float(val[1])<=-80.0 and float(val[1])>=-87.5 and float(val[2])>=24.5 and float(val[2])<=31.0:
			florida_nodes.append(jj) 
	nodes_to_remove=nx.out_degree_centrality(G) 
	florida_highoutd={}
	for key, value in nodes_to_remove.items():
		if key in set(florida_nodes):
			florida_highoutd[key]=value
	r=0
	ne=[]
	csd=[]
	for ky,vl in florida_highoutd.items():
		print (ky)
		ne.append(florida([ky]))
		if r==0:
			print ("node removed %s cascade %f nodes effected %s",(ky,csd,ne[r]))
			cascade[ky]=ne[r]
		elif r>0:
			print ("node removed %s cascade %f nodes effected %s",(ky,csd,ne[r]-ne[r-1]))
			cascade[ky]=ne[r]-ne[r-1]
		r+=1
	m=0
	for k, v in sorted(cascade.items(), key=lambda (k,v): (v,k),reverse=True):
		m+=1
		if m<=20:
			print("node",k,"cascade",v)
nodes_cascaded()
		
