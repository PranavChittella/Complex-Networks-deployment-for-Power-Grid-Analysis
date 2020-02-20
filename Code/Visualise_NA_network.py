  
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
m = Basemap(resolution='c', # c, l, i, h, f or None
            projection='merc',
            lat_0=47.2, lon_0=-109.6,
            llcrnrlon=-169.5, llcrnrlat= 12.8, urcrnrlon=-49.7, urcrnrlat=72.0)
m.bluemarble(scale = 0.5)
#m.drawmapboundary(fill_color='#566573')
#m.fillcontinents(color='#F0B27A',lake_color='#566573')
#m.drawcoastlines()
#m.drawstates(color='blue')
#print ("before reading")
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
#print("syncing")
x,y = m(longitude.values, latitude.values)
vertices_list=list(vertices.values)
longitude_list=list(longitude.values)
latitude_list=list(latitude.values)
links_id=list(l_ids.values)
v1_list=list(v1_edge.values)
v2_list=list(v2_edge.values)
#print(v1_list)

dicti={}
for i in range(0,len(vertices_list)):
	dicti[vertices_list[i][0]]=(longitude_list[i][0], latitude_list[i][0])
xs=[]
ys=[]

for i in range(0, len(links_id)):
	x1,y1=m(dicti[v1_list[i][0]][0], dicti[v1_list[i][0]][1])
	xs.append(x1)
	ys.append(y1)
	x1,y1=m(dicti[v2_list[i][0]][0], dicti[v2_list[i][0]][1])
	xs.append(x1)
	ys.append(y1)
	m.plot(xs,ys, 'g-', markersize=3)
	del xs[:]
	del ys[:]
	#print (i)
#m.plot(xs,ys, 'g-', markersize=3, label='Power Network Connections')
#m.plot(x, y, '#66ff33', markersize=1)
#m.plot(xs,ys, 'go', markersize=3, label='Power Network Grid Locations')
plt.title('Power Grid Network of North America')
plt.legend(loc=3)


plt.show()
# Algorithm: 
# 1. Read data from the CSV files for nodes and edges and corresponding coordinates
# 2. Process the data into a dictionary formed by lists
# 3. Use Basemap to draw the background of the scenario
# 4. call plt.plot and then call plt.show().
