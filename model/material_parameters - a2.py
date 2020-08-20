#! /user/bin/python
# - * - coding:UTF-8 - * -
from abaqus import *
from abaqusConstants import *
import __main__

#读取晶粒取向
f = open("C:\\temp\\grain_Orientations.txt",'r')
s = f.read()
a = s.split()
n = len(a)
grain_Orientations = []
for i in range(n):
	b = a[i].split(',')
	grain_Orientation = (float(b[0]),float(b[1]),float(b[2]))
	grain_Orientations = grain_Orientations + [grain_Orientation]

f.close()
#读取晶粒尺寸
f = open("C:\\temp\\diameter.txt",'r')
s = f.read()
a = s.split()
n = len(a)
grain_sizes= []
for i in range(n):
	b = a[i].split(',')
	grain_size = (float(b[0]))
	grain_sizes = grain_sizes + [grain_size]

f.close()

#读取晶核坐标
f = open("C:\\temp\\grain_nucleus.txt",'r')
s = f.read()
f.close()
a = s.split()
n = len(a)
nucleus_coordinates = []
for i in range(n):
	b = a[i].split(',')
	nucleus_coordinate = (float(b[0]),float(b[1]),float(b[2]))
	nucleus_coordinates = nucleus_coordinates + [nucleus_coordinate]


#获取模型名称
mname = mdb.models.keys()[1]
#获取部件名称
pname = mdb.models[mname].parts.keys()[0]
#生成面标号
f=mdb.models[mname].parts[pname].faces
faces = []
for i in range(n):
	faces = faces + [f.findAt((nucleus_coordinates[i],))]

def giveMaterial_alpha(faces,i,a1,b1,c1,a2):
	import section
	import regionToolset
	import displayGroupMdbToolset as dgm
	import part
	import material
	import assembly
	import step
	import interaction
	import load
	import mesh
	import job
	import sketch
	import visualization
	import xyPlot
	import displayGroupOdbToolset as dgo
	import connectorBehavior
	name='alpha'+str(i)
	mdb.models[mname].Material(name=name)
	mdb.models[mname].materials[name].Depvar(n=68)
	mdb.models[mname].materials[name].UserMaterial(unsymm=ON,
		mechanicalConstants=(
		   0,  1,  0,  1.00,  1,  1,  0,  0,
           a1,    b1,    c1,     0.500,     1.000,  1,  5, a2,))
	mdb.models[mname].HomogeneousSolidSection(name=name, 
		material=name, thickness=None)
	p = mdb.models[mname].parts[pname]
	region = regionToolset.Region(faces=faces)
	p.SectionAssignment(region=region, sectionName=name, offset=0.0, 
		offsetType=MIDDLE_SURFACE, offsetField='', 
		thicknessAssignment=FROM_SECTION)

def giveMaterial_beta(faces,i,a1,b1,c1,a2):
	import section
	import regionToolset
	import displayGroupMdbToolset as dgm
	import part
	import material
	import assembly
	import step
	import interaction
	import load
	import mesh
	import job
	import sketch
	import visualization
	import xyPlot
	import displayGroupOdbToolset as dgo
	import connectorBehavior
	name='beta'+str(i)
	mdb.models[mname].Material(name=name)
	mdb.models[mname].materials[name].Depvar(n=68)
	mdb.models[mname].materials[name].UserMaterial(unsymm=ON,
		mechanicalConstants=(		
		   0,  1,  0,  1.00,  1,  1,  0,  0,
                 a1,    b1,    c1,     0.500,     1.000,  1,  5,a2,))
	mdb.models[mname].HomogeneousSolidSection(name=name, 
		material=name, thickness=None)
	p = mdb.models[mname].parts[pname]
	region = regionToolset.Region(faces=faces)
	p.SectionAssignment(region=region, sectionName=name, offset=0.0, 
		offsetType=MIDDLE_SURFACE, offsetField='', 
		thicknessAssignment=FROM_SECTION)

#形成面集合
fields=(('alpha volume fraction(for example:80%,0.8):',''),)
alpha,=getInputs(fields=fields,label="Input the parameters")
alpha=float(alpha)
alpha_n = int(alpha*n)
for i in range(alpha_n):
	giveMaterial_alpha(faces[i],i,grain_Orientations[i][0],grain_Orientations[i][1],grain_Orientations[i][2],grain_sizes[i])

for i in range(alpha_n,n):
	giveMaterial_beta(faces[i],i,grain_Orientations[i][0],grain_Orientations[i][1],grain_Orientations[i][2],grain_sizes[i])

set = mdb.models[mname].parts[pname].Set(name='alpha', faces=faces[0:alpha_n])
#set = mdb.models[mname].parts[pname].Set(name='beta', faces=faces[alpha_n:n])
