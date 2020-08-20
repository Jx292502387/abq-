#! /user/bin/python
# - * - coding:UTF-8 - * -
from abaqus import *
from abaqusConstants import *
import part
import __main__

#读取晶粒顶点坐标
f = open("C:\\temp\\grain_topology_coords.txt",'r')
s = f.read()
a = s.split()
n = len(a)
grain_topology_coords = []
for i in range(n):
	b = a[i].split(',')
	grain_topology_coord = (float(b[0]),float(b[1]))
	grain_topology_coords = grain_topology_coords + [grain_topology_coord]

f.close()

#读取晶粒各顶点连接顺序
f = open("C:\\temp\\grain_topology_connection.txt",'r')
s = f.read()
a = s.split()
n = len(a)
grain_topology_connections = []
for i in range(n):
	b = a[i].split(',')
	grain_topology_connection = []
	for j in range(len(b)-1):
		grain_topology_connection = grain_topology_connection + [int(b[j])]
	grain_topology_connections = grain_topology_connections + [grain_topology_connection]

f.close()

#生成晶粒图-voronoi
mname='Model_'+str(len(a))+'_crystal'
m=mdb.Model(name=mname, modelType=STANDARD_EXPLICIT)
for i in range(len(a)):
	s1 = mdb.models[mname].ConstrainedSketch(name='__profile__', sheetSize=0.001*5.0)
	g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
	s1.setPrimaryObject(option=STANDALONE)
	for j in range(len(grain_topology_connections[i])-1):
		s1.Line(point1=grain_topology_coords[grain_topology_connections[i][j]-1], point2=grain_topology_coords[grain_topology_connections[i][j+1]-1])
	s1.Line(point1=grain_topology_coords[grain_topology_connections[i][j+1]-1], point2=grain_topology_coords[grain_topology_connections[i][0]-1])
	pname='Part'+str(i)
	p = mdb.models[mname].Part(name=pname, dimensionality=TWO_D_PLANAR, 
		type=DEFORMABLE_BODY)
	p = mdb.models[mname].parts[pname]
	p.BaseShell(sketch=s1)
	s1.unsetPrimaryObject()
	p = mdb.models[mname].parts[pname]
	session.viewports['Viewport: 1'].setValues(displayedObject=p)
	del mdb.models[mname].sketches['__profile__']


