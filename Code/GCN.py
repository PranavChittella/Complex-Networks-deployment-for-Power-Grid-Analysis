import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import networkx as nx
import collections
import tensorflow as tf
import operator
from collections import defaultdict
import scipy.sparse as sp

def color_one_hot(T):
	if T == 'generators':
		return 'red'
	elif T == 'distributors':
		return 'green'
	else:
		return 'blue'

def typ_one_hot(T):
	u = np.zeros(3)
	if T == 'generators':
		u[0] = 1
	elif T == 'distributors':
		u[1] = 1
	else:
		u[2] = 1

	return u

def sparse_to_tuple(sparse_mx):
    """Convert sparse matrix to tuple representation."""
    # The zeroth element of the tuple contains the cell location of each
    # non-zero value in the sparse matrix
    # The first element of the tuple contains the value at each cell location
    # in the sparse matrix
    # The second element of the tuple contains the full shape of the sparse
    # matrix
    def to_tuple(mx):
        if not sp.isspmatrix_coo(mx):
            mx = mx.tocoo()
        coords = np.vstack((mx.row, mx.col)).transpose()
        values = mx.data
        shape = mx.shape
        return coords, values, shape

    if isinstance(sparse_mx, list):
        for i in range(len(sparse_mx)):
            sparse_mx[i] = to_tuple(sparse_mx[i])
    else:
        sparse_mx = to_tuple(sparse_mx)

    return sparse_mx


def matmul(x, y, sparse=False):
    """Wrapper for sparse matrix multiplication."""
    if sparse:
        return tf.sparse_tensor_dense_matmul(x, y)
    return tf.matmul(x, y)


class GraphConvLayer:
    def __init__(
            self,
            input_dim,
            output_dim,
            activation=None,
            use_bias=False,
            name="graph_conv"):
        """Initialise a Graph Convolution layer.
        Args:
            input_dim (int): The input dimensionality.
            output_dim (int): The output dimensionality, i.e. the number of
                units.
            activation (callable): The activation function to use. Defaults to
                no activation function.
            use_bias (bool): Whether to use bias or not. Defaults to `False`.
            name (str): The name of the layer. Defaults to `graph_conv`.
        """
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.activation = activation
        self.use_bias = use_bias
        self.name = name

        with tf.variable_scope(self.name):
            self.w = tf.get_variable(
                name='w',
                shape=(self.input_dim, self.output_dim),
                initializer=tf.initializers.glorot_uniform())
            print("SAPE", (self.input_dim, self.output_dim))

            if self.use_bias:
                self.b = tf.get_variable(
                    name='b',
                    initializer=tf.constant(0.1, shape=(self.output_dim,)))

    def call(self, adj_norm, x, sparse=False):
    	#print("XSHAPE", np.asarray(x).shape)
    	x = matmul(x=x, y=self.w, sparse=sparse)
    	#print("XSHAPE1", np.asarray(x).shape)  # XW
    	x = matmul(x=adj_norm, y=x, sparse=True)  # AXW
    	#print("XSHAPE2", np.asarray(x).shape)
    	
    	if self.use_bias:
    	    x = tf.add(x, self.use_bias)          # AXW + B

    	if self.activation is not None:
    	    x = self.activation(x)                # activation(AXW + B)

    	return x

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)


testing_pandas = pd.read_csv('../Data/links.csv', sep=',', usecols=['v_id_1', 'v_id_2', 'l_id'])
vertices_type = pd.read_csv('../Data/Vertices_new.csv', sep = ',', usecols = ['v_id', 'lon', 'lat', 'typ'])

G = nx.DiGraph()
count = 0
for i in range(len(vertices_type)):
	#G.add_node(vertices_type.iloc[i,0], **{'type' : typ_one_hot(vertices_type.iloc[i,-1])})
	G.add_node(vertices_type.iloc[i,0], **{'color' : color_one_hot(vertices_type.iloc[i,-1]), 'type' : typ_one_hot(vertices_type.iloc[i,-1])})
	count += 1

#print("NODE TESTING", count)
count = 0
for i in range(len(testing_pandas)):
	if (testing_pandas.iloc[i,1] in G.node) and (testing_pandas.iloc[i,2] in G.node):
		G.add_edge(testing_pandas.iloc[i,1], testing_pandas.iloc[i,2])
		count += 1

#print("LINK COUNT", count)

m = nx.DiGraph()
for n in G.nodes:
	if G.degree(n) >= 9:
		m.add_node(n, **{'color' : G.nodes[n]['color'], 'type' : G.nodes[n]['type']})
		for r in G.neighbors(n):
			if G.degree(r) > 3:
				m.add_node(r, **{'color' : G.nodes[r]['color'], 'type' : G.nodes[r]['type']})
				m.add_edge(n,r)
ls = []
for n in m.nodes():
	if m.degree(n) <= 0 :
		ls.append(n)

m.remove_nodes_from(ls)
print("Number of nodes in graph = ", len(m))

between_ = nx.betweenness_centrality(m)
print(len(between_))
nx.set_node_attributes(m, between_, 'betweenness_centrality')
A = nx.adjacency_matrix(m)
A_ = A + np.eye(A.shape[0])

D = np.squeeze(np.sum(np.array(A_), axis=1))
D_ = np.power(D, -1/2)
D_n = np.diag(D)
Adj_ = np.dot(np.dot(D_n, A_), D_n)
Adj_norm = sparse_to_tuple(sp.coo_matrix(Adj_))

X = np.eye(A.shape[0])
X_ = sparse_to_tuple(sp.coo_matrix(X))
X_diff = []
for n in m.nodes(data = 'betweenness_centrality'):
    print(n)

labels = []
for n in m.nodes(data = 'type'):
	labels.append(n[-1])
labels = np.reshape(labels, (np.asarray(m).shape[0], 3))

# TensorFlow placeholders
ph = {
    'adj_norm': tf.sparse_placeholder(tf.float32, name="adj_mat"),
    'x': tf.sparse_placeholder(tf.float32, name="x"),
    'labels': tf.placeholder(tf.float32, shape = labels.shape)}

l_sizes = [4, 4, 2, 3]

o_fc1 = GraphConvLayer(
    input_dim=X.shape[-1],
    output_dim=l_sizes[0],
    name='fc1',
    activation=tf.nn.tanh)(adj_norm=ph['adj_norm'], x=ph['x'], sparse=True)

o_fc2 = GraphConvLayer(
    input_dim=l_sizes[0],
    output_dim=l_sizes[1],
    name='fc2',
    activation=tf.nn.tanh)(adj_norm=ph['adj_norm'], x=o_fc1)

o_fc3 = GraphConvLayer(
    input_dim=l_sizes[1],
    output_dim=l_sizes[2],
    name='fc3',
    activation=tf.nn.tanh)(adj_norm=ph['adj_norm'], x=o_fc2)

o_fc4 = GraphConvLayer(
    input_dim=l_sizes[2],
    output_dim=l_sizes[3],
    name='fc4',
    activation=tf.nn.tanh)(adj_norm=ph['adj_norm'], x=o_fc3)


correct = tf.equal(tf.argmax(o_fc4,1) , tf.argmax(ph['labels'],1))
accuracy = tf.reduce_mean(tf.cast(correct , tf.float32))

cost = tf.nn.softmax_cross_entropy_with_logits_v2(labels = ph['labels'] , logits = o_fc4)
optimize = tf.train.AdamOptimizer(0.001).minimize(cost)

epochs = 2000
outputs = {}
with tf.Session() as session:
	session.run(tf.global_variables_initializer())

	for epoch in range(epochs):
		feed_dict = {ph['adj_norm'] : Adj_norm , ph['x'] : X_ , ph['labels'] : labels}
		#outputs = session.run(o_fc4, feed_dict=feed_dict)
		_ = session.run(optimize, feed_dict = feed_dict)

		'''if epoch % save_ == 0:
			feed_dict_output = {ph['adj_norm'] : Adj_norm, ph['x'] : X_}
			output = session.run(o_fc3, feed_dict=feed_dict_output)
			outputs[epoch] = output'''

	inputs = session.run(o_fc3, feed_dict = feed_dict)



'''feed_dict = {ph['adj_norm']: Adj_norm,
             ph['x']: X_
             ph['labels'] : labels}'''

#outputs = sess.run(o_fc4, feed_dict=feed_dict)
#x_min, x_max = outputs[:, 0].min(), outputs[:, 0].max()
#y_min, y_max = outputs[:, 1].min(), outputs[:, 1].max()

node_pos_gcn = {n: tuple(inputs[j]) for j, n in enumerate(nx.nodes(m))}
'''node_pos_ran = {n: (np.random.uniform(low=x_min, high=x_max),
                    np.random.uniform(low=y_min, high=y_max))
                for j, n in enumerate(nx.nodes(G))}'''

#all_node_pos = (node_pos_gcn)#, node_pos_ran)
plot_titles = ('3-layer randomly initialised graph CNN with Supervised Learning.', 'random')

#node_positions = {o: {n: tuple(outputs[o][j]) for j, n in enumerate(nx.nodes(m))} for o in outputs}
#plot_titles = {o: 'epoch {o}'.format(o=o) for o in outputs}
#e = list(node_positions.keys())

# Two subplots, unpack the axes array immediately
f, axes = plt.subplots(nrows=1, ncols=1, sharey=True, sharex=True)
colors = []
for n in m.nodes(data = 'color'):
	colors.append(n[-1])

nx.draw(m, cmap = plt.get_cmap('jet'), node_color = colors, pos = node_pos_gcn, ax = axes)
plt.title(plot_titles[0])
#axes.set_title(plot_titles[0])
'''for i, ax in enumerate(axes.flat):
    pos = all_node_pos[i]
    ax.set_title(plot_titles[i])

    nx.draw(
        G,
        cmap=plt.get_cmap('jet'),
        node_color=colors,
        pos=pos, ax=ax)'''

plt.show()
#print(node_positions[e[0]])
'''f, axes = plt.subplots(nrows=2, ncols=3, sharey=True, sharex=True)

e = list(node_positions.keys())

for i, ax in enumerate(axes.flat):
    pos = node_positions[e[i]]
    ax.set_title(plot_titles[e[i]])

    nx.draw(
        m,
        cmap=plt.get_cmap('jet'),
        node_color=colors,
        pos=pos, ax=ax)

plt.show()'''


