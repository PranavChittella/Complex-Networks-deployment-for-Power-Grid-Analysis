#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  defense.py
#  
#  Copyright 2017 shivani <shivani@DESKTOP-4E711IT>
#  



import networkx as nx
import csv
from original_graph import graph
import copy
import random

G=nx.DiGraph()
nodes_data={}
edges_data={}
(G,nodes_data,edges_data)=graph()
H=copy.deepcopy(G)
V=copy.deepcopy(G)
generators=[]
for ss,vv in nodes_data.items():
	if vv[3]=='generators':
		generators.append(ss)
gen=set(generators)
'''the below defence line can be added to add defense to the cascade'''
#defended=['1898','5312','3106','4534','1101','648','5860','4294','3023','5860','242','1394','2724','8955','8413','759','2028','100','7456','7101','7189','6745','28563','3614']
defended=[]
def defense():
	'''for key,value in voltages.iteritems():
		weight[key[2]]=value'''
	initial_l={}
	initial_l_edges={}
	initial_l=nx.load_centrality(H,normalized=True,weight='cable')
	#bc=sorted(nx.edge_betweenness_centrality(H,normalized=True,weight='cable',reverse=True)
	#print initial_l_edges
	#nodes_to_remove=nx.load_centrality(H)
	nodes_to_remove=nx.out_degree_centrality(H)
	#nodes_to_remove=nx.in_degree_centrality(H)
	#nodes_to_remove=nx.closeness_centrality(H,distance='length',normalized=True)
	#nodes_to_remove=nx.betweenness_centrality(H,weight='cable',normalized=True)
	#hub,authorities=nx.hits(H)
	lamda=2
	for m,n in initial_l.items():
		initial_l[m]=lamda*n
	m=0
	remove=[]
	remove_nodes=[]
	remove_edges=[]
	pp=0
	#High_centrality={}
	'''for key,value in sorted(nodes_to_remove.iteritems(), key=lambda (k,v): (v,k),reverse=True):
		m+=1
		if m>=80 and m<=100:
			remove_nodes.append(key)
	rn=random.choice(remove_nodes)
	remove.append(rn)
	print rn'''
	'''appending 100 nodes that are to be removed from network'''
	wow = nodes_to_remove.items()
	for i in nodes_to_remove.keys():
		print(i)
	for key, value in sorted(nodes_to_remove.items(), key = lambda k,v:(v,k) ,reverse=True):
		m+=1
		if m<=1000:
			remove.append(key)
	in_wcc=len(max(nx.weakly_connected_components(H), key=len))
	'''n_wcc=nx.number_weakly_connected_components(H)
	in_scc=len(max(nx.strongly_connected_components(H), key=len))
	n_scc=nx.number_strongly_connected_components(H)'''
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
		H.remove_nodes_from(remove)
		for n in list(V.in_edges(remove)):
			V[n[0]][n[1]]['color']='red'
			edges_data[(n[0],n[1])][6]='r-'
		for oe in list(V.out_edges(remove)):
			V[oe[0]][oe[1]]['color']='red'
			edges_data[(oe[0],oe[1])][6]='r-'
		for l in remove:
			V.node[l]['color']='red'
			nodes_data[l][5]='ro'
		for ed in remove_edges:
			V.edge[ed[0]][ed[1]]['color']='red'
			edges_data[(ed[0],ed[1])][6]='r-'
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
					for x in list(H.successors(nn)):
						if x not in set(successor) and x not in set(remove):
							successor.append(x)
				H.remove_nodes_from(remove)
				for n in list(V.in_edges(remove)):
					V[n[0]][n[1]]['color']='red'
					edges_data[(n[0],n[1])][6]='r-'
				for oe in list(V.out_edges(remove)):
					V[oe[0]][oe[1]]['color']='red'
					edges_data[(oe[0],oe[1])][6]='r-'
				for l in remove:
					V.node[l]['color']='red'
					nodes_data[l][5]='ro'
			else:
				a+=1
			del remove[:]
		'''checking for nodes which are overloaded and appending them into remove list'''
		trans_l=nx.load_centrality(H,normalized=True,weight='cable')
		#trans_l_edges=nx.edge_betweenness_centrality(H,normalized=True,weight='cable')
		b=0
		for key,value in trans_l.items():
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
	for cc,vv in nodes_data.items():
		if vv[5]=='ro':
			h+=1
	#print "node removed",rn
	f_wcc=len(max(nx.weakly_connected_components(H), key=len))
	#f_scc=len(max(nx.strongly_connected_components(H), key=len))
	#nx.write_graphml(V,"outdegreelambda.graphml")
	print ("cascade size %f"%((float(in_wcc)-float(f_wcc))/float(in_wcc)))
	print ("%d wcc %d"%(in_wcc,f_wcc))
	print ("no. of nodes effected after removing 100 nodes",h)
	'''print "%d numberwcc %d"%(n_wcc,nx.number_weakly_connected_components(H))
	print "%d scc %d"%(in_scc,f_scc)
	print "%d numberscc %d"%(n_scc,nx.number_strongly_connected_components(H))'''
	'''creating a csv file containing the nodes and edges with cascaded nodes colored as red'''
	#o=[]
	'''with open('../../NS_project/Code/outcentrality_vertices.csv', 'wb') as csvfile:
		nodewriter = csv.writer(csvfile, delimiter=',')
		header=['v_id','lon','lat','color']
		nodewriter.writerow(header)
		for da,it in nodes_data.iteritems():
			for l in range(0,3):
				o.append(str(it[l]))
			o.append(str(it[5]))
			nodewriter.writerow(o)
			del o[:]
	with open('../../NS_project/Code/outcentrality_edges.csv', 'wb') as csvfile1:
		edgewriter = csv.writer(csvfile1, delimiter=',')
		header1=['l_id','v_id_1','v_id_2','color']
		edgewriter.writerow(header1)
		for db,itt in edges_data.iteritems():
			for l in range(0,3):
				o.append(str(itt[l]))
			o.append(str(itt[6]))
			edgewriter.writerow(o)
			del o[:]'''
defense()

