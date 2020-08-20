from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=282.98975533247, 
    height=152.084639698267)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
Mdb()

session.viewports['Viewport: 1'].setValues(displayedObject=None)
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)

p.WirePolyLine(points=(((0.0, 0.0, 0.0), (5.0, 0.0, 0.0)), ((0.0, 5.0, 0.0), (
    0.0, 0.0, 0.0)), ((5.0, 0.0, 0.0), (0.0, 5.0, 0.0))), mergeWire=OFF, 
    meshable=ON)
e = p.edges
edges = e.getSequenceFromMask(mask=('[#7 ]', ), )
p.Set(edges=edges, name='Wire-1-Set-1')

p.WirePolyLine(points=(((0.0, 0.0, 0.0), (0.0, 0.0, 5.0)), ), mergeWire=OFF, 
    meshable=ON)

e = p.edges
edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
p.Set(edges=edges, name='Wire-2-Set-1')


v = p.vertices
p.WirePolyLine(points=((v[0], v[2]), (v[3], v[0])), mergeWire=OFF, meshable=ON)
p = mdb.models['Model-1'].parts['Part-1']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#3 ]', ), )
p.Set(edges=edges, name='Wire-3-Set-1')

e = p.edges
p.CoverEdges(edgeList = e[0:1]+e[3:5], tryAnalytical=True)

e1 = p.edges
p.CoverEdges(edgeList = e1[0:1]+e1[2:3]+e1[5:6], tryAnalytical=True)

e = p.edges
p.CoverEdges(edgeList = e[0:1]+e[3:4]+e[5:6], tryAnalytical=True)

e1 = p.edges
p.CoverEdges(edgeList = e1[0:1]+e1[3:4]+e1[5:6], tryAnalytical=True)

f = p.faces
p.AddCells(faceList = f[0:4])
session.viewports['Viewport: 1'].setValues(displayedObject=p)
