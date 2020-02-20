#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  model_on_smallergraph.py

import networkx as nx
import csv
import copy
H=nx.DiGraph()
nodes=[(1,{'color':'green'}),(2,{'color':'green'}),(3,{'color':'green'}),(4,{'color':'green'}),(5,{'color':'green'}),(6,{'color':'green'}),(7,{'color':'green'}),(8,{'color':'green'}),(9,{'color':'green'}),(10,{'color':'green'}),(11,{'color':'green'})]
edges={(1,3):{'weight':5,'length':7,'color':'green'},(3,2):{'weight':3,'length':5,'color':'green'},(3,4):{'weight':3,'length':2,'color':'green'},(2,5):{'weight':2,'length':3,'color':'green'},(4,7):{'weight':4,'length':8,'color':'green'},(5,6):{'weight':6,'length':4,'color':'green'},(5,10):{'weight':5,'length':5,'color':'green'},(7,6):{'weight':9,'length':3,'color':'green'},(6,8):{'weight':9,'length':3,'color':'green'},(8,9):{'weight':3,'length':7,'color':'green'},(10,11):{'weight':7,'length':5,'color':'green'}}
for ll in nodes:
	H.add_node(ll[0],color=ll[1]['color'])
for i,j in edges.iteritems():
	H.add_edge(i[0],i[1],weight=j['weight'],length=j['length'],color=j['color'])
V=copy.deepcopy(H)
generators=[1]
defended=[]
def model():
	initial_l={}
	initial_l_edges={}
	initial_l=nx.load_centrality(H,normalized=True,weight='weight')
	lamda=1
	for m,n in initial_l.iteritems():
		initial_l[m]=lamda*n
	m=0
	remove=[2]
	remove_iter=[]
	remove_edges=[]
	pp=0
	in_wcc=len(max(nx.weakly_connected_components(H), key=len))
	g=0
	successor=[]
	trans_l={}
	'''removing the nodes which are selected'''
	while g==0:
		rr=list(remove)
		ee=list(remove_edges)
		for r in rr:
			if r in set(generators):
				generators.remove(r)
			if V.node[r]['color']=='red' or r in set(defended):
				remove.remove(r)
		for inn,e in enumerate(ee):
			if V.edge[ee[inn][0]][ee[inn][1]]['color']=='red':
				remove_edges.remove(ee[inn])
		del rr[:]
		del ee[:]
		H.remove_edges_from(remove_edges)
		for ind,eee in enumerate(remove_edges):
			if remove_edges[ind][1] not in set(remove):
				remove.append(remove_edges[ind][1])
		for nn in remove:
				for x in list(H.successors(nn)):
					if x not in set(successor) and x not in set(remove):
						successor.append(x)
		for rem in remove:
			remove_iter.append(rem)
		H.remove_nodes_from(remove)
		for n in list(V.in_edges(remove)):
			V[n[0]][n[1]]['color']='red'
		for oe in list(V.out_edges(remove)):
			V[oe[0]][oe[1]]['color']='red'
		for l in remove:
			V.node[l]['color']='red'
		for ed in remove_edges:
			V.edge[ed[0]][ed[1]]['color']='red'
		del remove[:]
		del remove_edges[:]
		'''removing components not containing a generator'''
		'''the inner loop is for cascade caused by removed nodes'''
		a=0
		while a==0:
			sss=list(successor)
			for zz,rz in enumerate(sss):
				if rz in generators or V.node[rz]['color']=='red' or rz in set(defended):
					successor.pop(zz)
			del sss[:]
			for su in successor:
				itera=0
				for g in generators:
					if su==g:
						itera+=1
						break
					elif nx.has_path(H,g,su):
						itera+=1 
						break
				if itera==0:
					remove.append(su)
			del successor[:]
			if len(remove)!=0:
				rrrr=list(remove)
				for ll,r in enumerate(rrrr):
					#dont have to pop generators here cause they are not getting added in the first place
					if V.node[r]['color']=='red':
						remove.pop(ll)
				del rrrr[:]
				for nn in remove:
					for x in list(V.successors(nn)):
						if x not in set(successor) and x not in set(remove_iter):
							successor.append(x)
				for rem in remove:
					remove_iter.append(rem)
				H.remove_nodes_from(remove)
				for n in list(V.in_edges(remove)):
					V[n[0]][n[1]]['color']='red'
				for oe in list(V.out_edges(remove)):
					V[oe[0]][oe[1]]['color']='red'
				for l in remove:
					V.node[l]['color']='red'
			else:
				a+=1
			del remove[:]
		'''checking for nodes which are overloaded and appending them into remove list'''
		trans_l=nx.load_centrality(H,normalized=True,weight='weight')
		#trans_l_edges=nx.edge_betweenness_centrality(H,normalized=True,weight='cable')
		b=0
		for key,value in trans_l.iteritems():
			if trans_l[key]>initial_l[key] and key not in generators:
				remove.append(key)
				b+=1
		'''for ky,vl in trans_l_edges.iteritems():
			if trans_l_edges[ky]>initial_l_edges[ky]:
				print (ky," ",vl," ")
				remove_edges.append(ky)
				mm+=1'''
		trans_l.clear()
		#trans_l_edges.clear()
		if b==0:
			break
	h=0
	print 6
	for cc in V.nodes():
		if V.node[cc]['color']=='red':
			h+=1
	f_wcc=len(max(nx.weakly_connected_components(H), key=len))
	nx.write_graphml(V,"smallgraph_cascade.graphml")
	print "cascade size %f"%((float(in_wcc)-float(f_wcc))/float(in_wcc))
	print "%d wcc %d"%(in_wcc,f_wcc)
	print "no. of nodes effected after removing one node named 2 is ",h
model()
