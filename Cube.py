#!/usr/bin/python
# import the python renderman library
import prman
import math

# def Cube(width=1.0,height=1.0,depth=1.0) :	
# 	w=width/2.0
# 	h=height/2.0
# 	d=depth/2.0
# 	ri.ArchiveRecord(ri.COMMENT, 'Cube Generated by Cube Function')
# 	#rear
# 	face=[-w,-h,d,-w,h,d,w,-h,d,w,h,d]								
# 	ri.Patch("bilinear",{'P':face})
# 	#front
# 	face=[-w,-h,-d,-w,h,-d,w,-h,-d,w,h,-d]								
# 	ri.Patch("bilinear",{'P':face})
# 	#left
# 	face=[-w,-h,-d,-w,h,-d,-w,-h,d,-w,h,d]									
# 	ri.Patch("bilinear",{'P':face})
# 	#right
# 	face=[w,-h,-d,w,h,-d,w,-h,d,w,h,d]								
# 	ri.Patch("bilinear",{'P':face})
# 	#bottom
# 	face=[w,-h,d,w,-h,-d,-w,-h,d,-w,-h,-d]								
# 	ri.Patch("bilinear",{'P':face})
# 	#top
# 	face=[w,h,d,w,h,-d,-w,h,d,-w,h,-d]								
# 	ri.Patch("bilinear",{'P':face})
# 	ri.ArchiveRecord(ri.COMMENT, '--End of Cube Function--')

# def Cubes():
# 	ri = prman.Ri()
# 	ri.TransformBegin() 
# 	ri.Translate(-2,0,0)
# 	ri.Rotate(25,0,1,0)
# 	Cube()
# 	ri.TransformEnd()
# 	ri.TransformBegin() 
# 	ri.Translate( 0,0,0)
# 	ri.Rotate( 25,1,1,0)
# 	ri.Skew(45.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0)
# 	Cube(0.8,0.8,0.8)
# 	ri.TransformEnd()
# 	ri.TransformBegin() 
# 	ri.Translate(2,0,0)
# 	ri.Rotate(-25,1,1,1)
# 	Cube(0.2,2,0.2)
# 	ri.TransformEnd()

# def HullSubdiv() :
# 	ri = prman.Ri()
# 	s = 0.5
# 	nverts = [4] * 1
# 	verts = [
# 		-s,-s,s, # front bottom left
# 		s,-s,s,  # front bottom right
# 		s,s,s,   # front top right
# 		-s,s,s   # front top left
# 	]
# 	indices = [0,1,2,3]
# 	ri.SubdivisionMesh("catmull-clark", nverts, indices, [ri.INTERPBOUNDARY], [0,0], [], [], {ri.P: verts})

def Table():
	ri = prman.Ri()
	x = 10
	y = 0
	z = x
	verts = [
		-x, y, -z,
		-x, y, z,
		x, y, -z,
		x, y, z
	]
	ri.Patch("bilinear", {'P':verts})

class Model():
	nverts = []
	verts = []
	indices = []
	tags = []
	edgeLoops = []
	sharpness = []
	nargs = []

	def __init__(self):
		print("model created")
		self.nverts = []
		self.verts = []
		self.indices = []
		self.tags = []
		self.edgeLoops = []
		self.sharpness = []
		self.nargs = []

	def update(self, nverts, verts, indices, tags, edgeLoops, sharpness):
		numverts = len(self.verts)/3
		offset = numverts
		self.nverts = self.nverts + nverts
		self.verts = self.verts + verts
		for i in indices:
			self.indices.append(i+offset)
		self.tags = self.tags + tags
		if len(tags) > 0:
			for i in range(0, len(tags)):
				self.nargs = self.nargs + [5,1]
		for e in edgeLoops:
			self.edgeLoops.append(e+offset)
		self.sharpness = self.sharpness + sharpness

	def draw(self):
		ri.SubdivisionMesh("catmull-clark", self.nverts, self.indices, self.tags, self.nargs, self.edgeLoops, self.sharpness, {ri.P: self.verts})


def CylinderBase(radius=0.5, height=1.0):
	ri = prman.Ri()

	y=1
	x=math.sqrt((radius*radius)/1.5)
	z=x
	verts = [
		-x, y, -z,
		-x, y, z,
		x, y, z,
		x, y, -z
	]

	x = x*0.9
	z = z*0.9
	y = y-0.1
	verts = verts + [
		-x, y, -z,
		-x, y, z,
		x, y, z,
		x, y, -z
	]

	x = x*0.8
	z = z*0.8
	y = y-0.2
	verts = verts + [
		-x, y, -z,
		-x, y, z,
		x, y, z,
		x, y, -z
	]

	nFaces = 9
	nverts = [4]*nFaces
	indices = [
		4,0,1,5,
		5,1,2,6,
		6,2,3,7,
		7,3,0,4,
		8,4,5,9,
		9,5,6,10,
		10,6,7,11,
		11,7,4,8,
		8,9,10,11
	]
	tags = [ri.CREASE, ri.CREASE]
	intargs = [
		4,5,6,7,4,
		8,9,10,11,8,
	]
	sharpness = [5,5]

	model = Model()
	model.update(nverts, verts, indices, tags, intargs, sharpness)
	# model.draw()


def Square(x,y,z):
	return [
		-x, y, -z,
		-x, y, z,
		x, y, z,
		x, y, -z
	]

def Cylinder(radius=0.5, height=1.0) :
	ri = prman.Ri()
	indices=[
		# Bottom base face
		0,1,2,3,
		# Outside faces
		0,4,5,1,
		1,5,6,2,
		2,6,7,3,
		3,7,4,0,
		# Top faces
		4,8,9,5,
		5,9,10,6,
		6,10,11,7,
		7,11,8,4,
		# Inside faces
		8,12,13,9,
		9,13,14,10,
		10,14,15,11,
		11,15,12,8,
		# Bottom inside face
		12,15,14,13,
		# Bottom lip 1 faces
		16,0,1,17,
		17,1,2,18,
		18,2,3,19,
		19,3,0,16
	]
	nverts=[4]*(len(indices)/4)
	y=0.5
	x=math.sqrt((radius*radius)/1.5)
	z=x
	bottom_verts = [
		-x, y, -z,
		-x, y, z,
		x, y, z,
		x, y, -z
	]
	top_verts = [
		-x, y, -z,
		-x, y, z,
		x, y, z,
		x, y, -z
	]
	lip = 0.9
	x = x*lip
	z = z*lip
	top_verts_inside = [
		-x, y, -z,
		-x, y, z,
		x, y, z,
		x, y, -z
	]
	depth = 0.1
	bottom_verts_inside = [
		-x, depth, -z,
		-x, depth, z,
		x, depth, z,
		x, depth, -z
	]
	y = 0.05
	x=math.sqrt((radius*radius)/1.5)
	z=x
	bottom_verts_lip1 = [
		-x, y, -z,
		-x, y, z,
		x, y, z,
		x, y, -z
	]
	verts=bottom_verts + top_verts + top_verts_inside + bottom_verts_inside
	verts=verts + bottom_verts_lip1

	tags=[ri.CREASE,ri.CREASE,ri.CREASE,ri.CREASE]
	nargs=[5,1,5,1,5,1,5,1] # number of args.
	intargs=[  # int args - the chain of verts that make up the edges (5 from the previous one)
		0,1,2,3,0,
		4,5,6,7,4,
		8,9,10,11,8,
		12,13,14,15,12
	]
	sharp=2
	bottom_sharp = 10
	sharpness=[bottom_sharp,sharp,sharp,bottom_sharp] # sharpness of creases (float args). If >= 10 infinite sharpness.
	ri.SubdivisionMesh("catmull-clark", nverts, indices, tags, nargs, intargs, sharpness, {ri.P: verts})


def CreateFaceLoop(startindex=0):
	faces = [
		0,4,5,1,
		1,5,6,2,
		2,6,7,3,
		3,7,4,0
	]
	faces = [i+(startindex*4) for i in faces]
	return faces

def CreateEdgeLoop(startindex=0):
	edges = [0,1,2,3,0]
	edges = [i+(startindex*4) for i in edges]
	return edges

def Cylinder2(radius=0.5, height=1.0):
	X_BASE=math.sqrt((radius*radius)/1.5)
	Z_BASE=X_BASE
	LIP_HEIGHT=height*0.05

	x=X_BASE*0.4
	y=0
	z=Z_BASE*0.4
	bottom_verts3 = Square(x,y,z)

	x=X_BASE*0.4
	y=LIP_HEIGHT/2
	z=Z_BASE*0.4
	bottom_verts4 = Square(x,y,z)

	x=X_BASE*0.8
	y=0
	z=Z_BASE*0.8
	bottom_verts1 = Square(x,y,z)

	x=X_BASE*0.9
	y=LIP_HEIGHT/2
	z=Z_BASE*0.9
	bottom_verts2 = Square(x,y,z)

	x=X_BASE
	y=LIP_HEIGHT
	z=Z_BASE
	top_verts_1 = Square(x,y,z)

	verts = bottom_verts4 + bottom_verts3 + bottom_verts1 + bottom_verts2 + top_verts_1

	num = 4
	edgeloops = []
	indices = [
		0,1,2,3
	]
	for i in range(num):
		edgeloops = edgeloops + CreateEdgeLoop(i)
		indices = indices + CreateFaceLoop(i)

	tags = [ri.CREASE]*num
	nargs = [5,1]*num
	floatargs = [2]*num
	nfaces = len(indices)/4
	nverts = [4]*nfaces

	ri.SubdivisionMesh("catmull-clark", nverts, indices, tags, nargs, edgeloops, floatargs, {ri.P: verts})



ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "Cube.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render") #filename)
# ArchiveRecord is used to add elements to the rib stream in this case comments
# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("Cube.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,576,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:40}) 

# now we start our world
ri.WorldBegin()

ri.Translate(0,-3,0)
ri.Translate(0,0,20)
ri.Rotate(-20,1,0,0)

ri.TransformBegin()
ri.Translate(-2,1,0)
Cylinder2(height=10, radius=2)
ri.TransformEnd()

ri.TransformBegin()
radius=2
ri.Translate(2,radius,0)
ri.Rotate(-90,1,0,0)
Cylinder2(height=5, radius=radius)
ri.TransformEnd()

ri.TransformBegin()
radius=2
ri.Translate(6,radius,0)
ri.Rotate(90,1,0,0)
Cylinder2(height=5, radius=radius)
ri.TransformEnd()

# CylinderBase(height=5,radius=2)

# Table()

ri.WorldEnd()
ri.End()
