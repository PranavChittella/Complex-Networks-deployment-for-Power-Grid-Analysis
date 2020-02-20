#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  original_graph.py
#  
#  Copyright 2017 shivani <shivani@DESKTOP-4E711IT>
import networkx as nx
import csv
import numpy as np

G=nx.DiGraph()
nodes_data={}
edges_data={}
nodes=[]
edges=[]
voltage={}
longitude={}
latitude={}
voltages={}
length={}
cable={}
n_color={}
e_color={}
def graph():
	with open('../Data/Vertices_new.csv','r') as dfile:
		reader=csv.reader(dfile,delimiter=",")
		node_data=list(reader)
		node_data.remove(node_data[0])
	with open('../Data/Edges_new.csv','r') as dfile1:
		reader1=csv.reader(dfile1,delimiter=",")
		edge_data=list(reader1)
		edge_data.remove(edge_data[0])
	for n in node_data:
		nodes_data[n[0]]=n
		nodes_data[n[0]].append('ko')
		for i in [1,2,4]:
			nodes_data[n[0]][i]=float(nodes_data[n[0]][i])
		nodes.append(n[0])
		if n[4]=='nan':
			voltage[n[0]]=np.nan
		else:
			voltage[n[0]]=float(n[4])
		longitude[n[0]]=float(n[1])
		latitude[n[0]]=float(n[2])
		n_color[n[0]]='black'
	G.add_nodes_from(nodes)
	#nx.set_node_attributes(G,'voltage',voltage)
	nx.set_node_attributes(G,longitude,'longitude')
	nx.set_node_attributes(G,latitude,'latitude')
	nx.set_node_attributes(G,n_color,'color')
	for e in edge_data:
		edges_data[(e[1],e[2])]=e
		edges_data[(e[1],e[2])].append('k-')
		for ii in [3,4,5]:
			edges_data[(e[1],e[2])][ii]=float(edges_data[(e[1],e[2])][ii])
		G.add_edge(e[1],e[2],key=e[0])
		if e[3]=='nan':
			voltages[(e[1],e[2])]=np.nan
		else:
			voltages[(e[1],e[2])]=float(e[3])
		length[(e[1],e[2])]=float(e[5])
		cable[(e[1],e[2])]=float(e[4])
		e_color[(e[1],e[2])]='black'
	#nx.set_edge_attributes(G,'voltages',voltages)
	nx.set_edge_attributes(G,length,'length')
	nx.set_edge_attributes(G,cable,'cable')
	nx.set_edge_attributes(G,e_color,'color')
	return (G,nodes_data,edges_data)
graph()
