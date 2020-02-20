#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  makegraph.py
#  
#  Copyright 2017 shivani <shivani@DESKTOP-4E711IT>
#  
import networkx as nx
import numpy as np
import csv

def mgraph():
	with open('../Data/vertices.csv','r') as dfile:
		reader=csv.reader(dfile,delimiter=",")
		node_data=list(reader)
		node_data.remove(node_data[0])
		#print node_data[0]
	with open('../Data/links.csv','r') as dfile1:
		reader1=csv.reader(dfile1,delimiter=",")
		edge_data=list(reader1)
		edge_data.remove(edge_data[0])
	#print len(edge_data)
	G=nx.MultiDiGraph()
	nodes=[]
	nodes_data={}
	edges_data={}
	for n in node_data:
		nodes.append(n[0])
		nodes_data[n[0]]=n
	G.add_nodes_from(nodes)
	edges=[]
	for e in edge_data:
		edges.append((e[1],e[2],e[0]))
		edges_data[e[0]]=e
	for i in edges:
		G.add_edge(i[0],i[1],key=i[2])
	return (G,nodes_data,edges_data)
mgraph()

