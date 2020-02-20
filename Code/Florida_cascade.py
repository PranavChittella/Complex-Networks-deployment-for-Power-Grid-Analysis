#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Florida_cascade.py
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
for ss,vv in nodes_data.iteritems():
	if vv[3]=='generators':
		generators.append(ss)
gen=set(generators)
defended=[]
defended=['878','100','3537','900','6103','3529','14527','7488','7366','3561','24872','1762','14527','1299','11954','7536','7517','7512','7398','7039','6859','6806','6800','6790','6366']
for xx in defended:
	V.node[xx]['color']='green'
	nodes_data[xx][5]='go'
print "1"

def florida(remove=[]):
	'''for key,value in voltages.iteritems():
		weight[key[2]]=value'''
	initial_l={}
	initial_l_edges={}
	initial_l=nx.load_centrality(H,normalized=True,weight='cable')
	lamda=2
	for m,n in initial_l.iteritems():
		initial_l[m]=lamda*n
	m=0
	florida_nodes=[]
	remove_nodes=[]
	remove_edges=[]
	pp=0
	#High_centrality={}
	print (2)
	for jj,val in nodes_data.iteritems():
		if float(val[1])<=-80.0 and float(val[1])>=-87.5 and float(val[2])>=24.5 and float(val[2])<=31.0:
			florida_nodes.append(jj) 
	nodes_to_remove=nx.out_degree_centrality(H) 
	florida_highoutd={}
	for key, value in nodes_to_remove.iteritems():
		if key in set(florida_nodes):
			florida_highoutd[key]=value
	'''for key,value in sorted(florida_highoutd.iteritems(), key=lambda (k,v): (v,k),reverse=True):
		m+=1
		if m>=0 and m<=50:
			remove_nodes.append(key)
	rn=random.choice(remove_nodes)
	remove.append(rn)
	print rn'''
	
	for key, value in sorted(florida_highoutd.iteritems(), key=lambda (k,v): (v,k),reverse=True):
		m+=1
		if m<=50:
			remove.append(key)
	in_wcc=len(max(nx.weakly_connected_components(H), key=len))
	'''n_wcc=nx.number_weakly_connected_components(H)
	in_scc=len(max(nx.strongly_connected_components(H), key=len))
	n_scc=nx.number_strongly_connected_components(H)'''
	g=0
	successor=[]
	trans_l={}
	print "3"
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
		print "4"
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
		a=0
		while a==0:
			print (5)
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
			del successor[:]
			del remove[:]
		print "6"
		trans_l=nx.load_centrality(H,normalized=True,weight='cable')
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
	for cc,vv in nodes_data.iteritems():
		if vv[5]=='ro':
			h+=1
	print "7"
	#print "node removed",rn
	f_wcc=len(max(nx.weakly_connected_components(H), key=len))
	#f_scc=len(max(nx.strongly_connected_components(H), key=len))
	#nx.write_graphml(V,"outdegreelambda.graphml")
	print "cascade size %f"%((float(in_wcc)-float(f_wcc))/float(in_wcc))
	print "%d wcc %d"%(in_wcc,f_wcc)
	print "no. of nodes effected",h
	'''print "%d numberwcc %d"%(n_wcc,nx.number_weakly_connected_components(H))
	print "%d scc %d"%(in_scc,f_scc)
	print "%d numberscc %d"%(n_scc,nx.number_strongly_connected_components(H))'''
	o=[]
	with open('../../NS_project/Code/floridacascade_vertices.csv', 'wb') as csvfile:
		nodewriter = csv.writer(csvfile, delimiter=',')
		header=['v_id','lon','lat','color']
		nodewriter.writerow(header)
		for da,it in nodes_data.iteritems():
			for l in range(0,3):
				o.append(str(it[l]))
			o.append(str(it[5]))
			nodewriter.writerow(o)
			del o[:]
	with open('../../NS_project/Code/floridacascade_edges.csv', 'wb') as csvfile1:
		edgewriter = csv.writer(csvfile1, delimiter=',')
		header1=['l_id','v_id_1','v_id_2','color']
		edgewriter.writerow(header1)
		for db,itt in edges_data.iteritems():
			for l in range(0,3):
				o.append(str(itt[l]))
			o.append(str(itt[6]))
			edgewriter.writerow(o)
			del o[:]
florida()
