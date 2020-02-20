  
import matplotlib.pyplot as plt
import matplotlib.cm
import csv
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
fig, ax= plt.subplots(figsize=(20,40))
print ("Calc basemap...")
'''florida's map'''
'''m = Basemap(resolution='c', # c, l, i, h, f or None
            projection='merc',
            lat_0=29.75, lon_0=-83.75,
            llcrnrlon=-87.5, llcrnrlat= 24.5, urcrnrlon= -80.0, urcrnrlat=33.0)'''
m = Basemap(resolution='c', # c, l, i, h, f or None
            projection='merc',
            lat_0=47.2, lon_0=-109.6,
            llcrnrlon=-169.5, llcrnrlat= 12.8, urcrnrlon=-49.7, urcrnrlat=72.0)
#print "Done."
m.drawmapboundary(fill_color='#99ffff')
m.fillcontinents(color='#aaff80',lake_color='#99ffff')
#m.drawcoastlines()
#m.drawstates(color='blue')
print ("Finished script.")

longitude = pd.read_csv('../Data/vertices.csv', sep=',', usecols=['lon'])
latitude = pd.read_csv('../Data/vertices.csv', sep=',', usecols=['lat'])
vertices = pd.read_csv('../Data/vertices.csv', sep=',', usecols=['v_id'])
#print(vertices.values)
voltage1=pd.read_csv('../Data/vertices.csv', sep=',', usecols=['voltage'])
#print(voltage1.values)
v1_edge=pd.read_csv('../Data/links.csv', sep=',', usecols=['v_id_1'])
v2_edge=pd.read_csv('../Data/links.csv', sep=',', usecols=['v_id_2'])
#print(type(longitude))
l_ids=pd.read_csv('../Data/links.csv', sep=',', usecols=['l_id'])

'''below comment is added and the above code can be commented out to read florida data'''
longitude = pd.read_csv('outcentrality_vertices.csv', sep=',', usecols=['lon'])
#lon=longitude['lon'].values
latitude = pd.read_csv('outcentrality_vertices.csv', sep=',', usecols=['lat'])
#lat=latitude['lon'].values
vertices = pd.read_csv('outcentrality_vertices.csv', sep=',', usecols=['v_id'])
#print(vertices.values)
nodes_color=pd.read_csv('outcentrality_vertices.csv', sep=',', usecols=['color'])
#print(voltage1.values)
v1_edge=pd.read_csv('outcentrality_edges.csv', sep=',', usecols=['v_id_1'])
v2_edge=pd.read_csv('outcentrality_edges.csv', sep=',', usecols=['v_id_2'])
#print(type(longitude))
l_ids=pd.read_csv('outcentrality_edges.csv', sep=',', usecols=['l_id'])
edges_color=pd.read_csv('outcentrality_edges.csv', sep=',', usecols=['color'])

#hld = pd.read_csv('r_highloadnodes_vertices.csv') 

#cascade_lon = hld[['lon1']]
#cascade_lat = hld[['lat']]
#cascade_nodes = hld[['v+AF8-id']]
#color_nodes=hld[['color']]
#hld1=pd.read_csv('r_highloadnodes_edges.csv')
#cascade_edges=hld1[['l_id']]
#color_edge=hld1[['color']]
print("syncing")
vertices_list=list(vertices.values)
longitude_list=list(longitude.values)
latitude_list=list(latitude.values)
links_id=list(l_ids.values)
v1_list=list(v1_edge.values)
v2_list=list(v2_edge.values)
#nodes=list(cascade_nodes.values)
colors=list(nodes_color.values)
#cascade_lat_list=list(cascade_lat.values)
#cascade_lon_list=list(cascade_lon.values)
#cascade_edges_list=list(cascade_edges.values)
color_edges=list(edges_color.values)

dicti={}
dicti2={}
for i in range(0,len(vertices_list)):
	dicti[vertices_list[i][0]]=(longitude_list[i][0], latitude_list[i][0])
	x,y = m(longitude_list[i][0], latitude_list[i][0])
	m.plot(x, y, colors[i][0], markersize=3)
	#x.remove()
	#y.remove()
xs=[]
ys=[]
for i in range(0, len(links_id)):
	x1,y1=m(dicti[v1_list[i][0]][0], dicti[v1_list[i][0]][1])
	xs.append(x1)
	ys.append(y1)
	x1,y1=m(dicti[v2_list[i][0]][0], dicti[v2_list[i][0]][1])
	xs.append(x1)
	ys.append(y1)
	m.plot(xs,ys, color_edges[i][0], markeredgewidth=10)
	xs=[]
	ys=[]
'''for i in range(0, len(nodes)):
	if(colors[i]=='ro'):
		x,y=m(cascade_lon.values, cascade_lat.values)
		m.plot(x,y, color='ro')'''

m.plot(xs,ys, 'k-', markersize=3, label='Power Network Connections')
m.plot(xs,ys, 'ko', markersize=10, label='Power Network Locations')
m.plot(xs,ys, 'r-', markersize=3, label='Power Network cascaded Connections')
m.plot(xs,ys, 'ro', markersize=10, label='Power Network cascaded Locations')
plt.title('Power Grid Network of North America')
plt.legend(loc=3)



plt.show()
