from abaqus import *
from abaqusConstants import *
import xlwt
import xlrd
import regionToolset
import math
import material

file=xlwt.Workbook()
table=file.add_sheet('sheet1',cell_overwrite_ok=True)

diameter=[]
area=[]
i=0
p=mdb.models['Model_100_crystal'].parts['P1']
f=p.faces
while i<len(f):
	p=mdb.models['Model_100_crystal'].parts['P1']
	f=p.faces
	size=f[i].getSize()
	d=2*((size/math.pi)**0.5)
	diameter.append(d)
	table.write(i,0,d,)
	table.write(i,1,size,)
	i=i+1
file.save('diameter.xls')
