import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import networkx as nx
import collections
import tensorflow as tf
import operator
from collections import defaultdict

def typ_one_hot(T):
	u = np.zeros(3)
	if T == 'generators':
		u[0] = 1
	elif T == 'distributors':
		u[1] = 1
	else:
		u[2] = 1

	return u

vertices = pd.read_csv('../Data/vertices.csv', sep=',', usecols=['v_id'])
v1_edge=pd.read_csv('../Data/links.csv', sep=',', usecols=['v_id_1'])
v2_edge=pd.read_csv('../Data/links.csv', sep=',', usecols=['v_id_2'])
l_ids=pd.read_csv('../Data/links.csv', sep=',', usecols=['l_id'])

vertices_list=list(vertices.values)
testing_pandas = pd.read_csv('../Data/links.csv', sep=',', usecols=['v_id_1', 'v_id_2', 'l_id'])
vertices_type = pd.read_csv('../Data/Vertices_new.csv', sep = ',', usecols = ['v_id', 'lon', 'lat', 'typ'])

vert = np.zeros(len(vertices))
#print(testing_pandas.iloc[0,0])
#d = np.zeros((len(vertices), 2))
#d = {}

'''for i in range(len(vertices)):
	d[str(vertices.iloc[i])] = i 
    for j in range(d.shape[-1]):
		if j == 0:
			d[i,0] = vertices.iloc[i,0]
		else:
			d[i,1] = i'''

#links_id=list(l_ids.values)
#v1_list=list(v1_edge.values)
#v2_list=list(v2_edge.values)

#v_list = []
'''x = {}
for i in range(len(v1_edge)):
	if v1_edge.iloc[i,0] in x:
		if v2_edge.iloc[i,0] in x:
			continue
		else:
			x[v2_edge.iloc[i,0]] = i 
	else:
		x[v1_edge.iloc[i,0]] = i'''


#x = {}
#for i in range(len(vertices_type)):
	#x[vertices_type.iloc[i,0]] = i
'''A = np.zeros((len(l_ids), len(l_ids)))
count = 0
for i in range(len(l_ids)):
	if l_ids.iloc[i,0] == testing_pandas.iloc[i,0]:
		if testing_pandas.iloc[i,1] in x:
			if testing_pandas.iloc[i,2] in x:
				A[x[testing_pandas.iloc[i,1]], x[testing_pandas.iloc[i,2]]] = 1
				count += 1'''
#testing_list = [l_ids.values,v1_edge.values, v2_edge.values]
#print(l_ids.iloc[0,0])
#print(testing_pandas.iloc[i,0])
#print(d[str(testing_pandas.iloc[i,1])])
'''lsr = []
for i in A:
	lsr.append(sum(i))'''

#print("MAXIMUM DEGREE", max(lsr))
#print("MINIMUM DEGREE", min(lsr))
#plt.plot([i for i in range(len(lsr))], lsr)
#plt.title("Degree Distribution.")
#plt.xlabel("Number of nodes in the network.")
#plt.ylabel("Degrees of nodes.")
#plt.show()


# USING NETWORKX 
G = nx.DiGraph()
#mno = []
x = {}
count = 0
for i in range(len(vertices_type)):
	G.add_node(vertices_type.iloc[i,0], **{'type' : typ_one_hot(vertices_type.iloc[i,-1])})
	#x['type'] = typ_one_hot(vertices_type.iloc[i, -1])
	count += 1
	'''if not vertices_type.iloc[i,0] in mno:
		
		mno.append(vertices_type.iloc[i,0])

	#elif not vertices.iloc[i,2] in mno:
		#G.add_node(vertices.iloc[i,2])
		#mno.append(vertices.iloc[i,2])
		count += 1
	else:
		continue'''
print("NODE TESTING", count)
#nx.set_node_attributes(G, 'type', x)
#print(G.node[vertices_type.iloc[0,0]]['type'])
#count = 0
'''for i in range(len(l_ids)):
	if l_ids.iloc[i,0] == testing_pandas.iloc[i,0]:
		if testing_pandas.iloc[i,1] in mno:
			if testing_pandas.iloc[i,2] in mno:
				#A[x[testing_pandas.iloc[i,1]], x[testing_pandas.iloc[i,2]]] = 1
				G.add_edge(x[testing_pandas.iloc[i,1]], x[testing_pandas.iloc[i,2]])
				count += 1'''


for i in range(len(l_ids)):
	if (testing_pandas.iloc[i,1] in G.node) and (testing_pandas.iloc[i,2] in G.node):
		G.add_edge(testing_pandas.iloc[i,1], testing_pandas.iloc[i,2])
		#count += 1
	'''for j in range(len(vertices_type)):
		if testing_pandas.iloc[i,1] == vertices_type.iloc[j,0]:
			for k in range(len(vertices_type)):
				if testing_pandas.iloc[i,2] == vertices_type.iloc[k,0]:
					#G.add_edge(testing_pandas.iloc[i,1], testing_pandas.iloc[i,2])
					G.add_edge(vertices_type.iloc[j,0],vertices_type.iloc[k,0])
					count += 1'''
#print(count)

#A = nx.adjacency_matrix(G)
#print(A.shape)
#ls = []
#for i in A:
	#print(sum(i))
#	ls.append(sum(i))
#print(np.array(ls).shape)
#plt.plot([i for i in range(len(ls))], ls)
#plt.title("Degree Distribution.")
#plt.xlabel("Number of nodes in the network.")
#plt.ylabel("Degrees of nodes.")
#nx.draw(G)
#plt.show()

degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
# print "Degree sequence", degree_sequence
print("MAXIMUM DEGREE", max(degree_sequence))
print("MINIMUM DEGREE", min(degree_sequence))
#degreeCount = collections.Counter(degree_sequence)
#deg, cnt = zip(*degreeCount.items())

#fig, ax = plt.subplots()
#plt.plot(deg, cnt, width=0.5, color='r')
#plt.plot(deg, cnt, 'ro-')
#plt.title("US Powergrid Degree Distribution")
#plt.ylabel("Number of Nodes")
#plt.xlabel("Degree")
#ax.set_xticks([d  for d in deg])
#ax.set_xticklabels(deg)
#plt.show()


#pos = nx.spring_layout(G, k = 0.3, iterations = 20)
#nx.draw(G, pos)
#plt.show()

#G_numpy = nx.to_numpy_matrix(G)
m = nx.DiGraph()
countm = 0
for n in G.nodes:
	if G.degree(n) >= 9:
		m.add_node(n, **{'color' : G.nodes[n]['type']})
		for r in G.neighbors(n):
			if G.degree(r) > 0:
				m.add_node(r, **{'color' : G.nodes[r]['type']})
				m.add_edge(n,r)
		countm += 1
ls = []
c = 0
for n in m.nodes():
	if m.degree(n) <= 0 :
		ls.append(n)
	else:
		print(m.nodes[n]['color'])
		c += 1
m.remove_nodes_from(ls)

print("NODES", c)
degree_sequence_m = sorted([d for n, d in m.degree()], reverse=True)
print("MAXIMUM DEGREE", max(degree_sequence_m))
print("MINIMUM DEGREE", min(degree_sequence_m))
print(np.asarray(m).shape)
#for i in m.nodes.items():
	#print(i)
#print(G_numpy.shape)


#in_degrees = G.degree() # dictionary node:degree
#in_values = sorted(set(in_degrees.values()))
#in_hist = [in_degrees.values().count(x) for x in in_values]
#plt.figure()
'''plt.plot(np.array([range(count)]).T,degree_sequence,'ro-') # in-degree
plt.xlabel('Degree')
plt.ylabel('Number of nodes')
plt.title('US Powergrid Degree Distribution')
plt.show()'''

#A = nx.adjacency_matrix(G)

# TO AGGREGRATE NODES BASED ON THEMSELVES AND NOT JUST THE SURROUNDINGS
#A_ = A + np.eye(A.shape[0])
#print(A_.shape)

#D = np.eye(A.shape[0])
#degree_sequence = [d for n, d in G.degree()]
#print(np.array(degree_sequence).shape)
#print(G.adj[4446])
#for i in range(A.shape[0]):
	#D[i,i] = degree_sequence[i]
#pg = nx.pagerank_numpy(G)

#out = nx.out_degree_centrality(G)
#print(max(out.items(), key = operator.itemgetter(1)))
#print(out[max(out.items(), key = operator.itemgetter(1))[0]])
'''best = max(out.items(), key = operator.itemgetter(1))[1]
for a,b in out.items():
	if b > best:
		print("LOL",a)'''
#if cb.is_numlike(alpha):
    #edge_collection.set_alpha(alpha)



'''degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
# print "Degree sequence", degree_sequence
dmax = max(degree_sequence)

plt.loglog(degree_sequence, 'b-', marker='o')
#plt.loglog(np.array(sorted(lsr, reverse = True)), 'r-', marker='o')
plt.title("Degree rank plot")
plt.ylabel("degree")
plt.xlabel("rank")
plt.show()'''