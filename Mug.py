#!/usr/bin/python
import prman
import math

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

def Square(x,y,z):
	return [
		-x, y, -z,
		x, y, -z,
		x, y, z,
		-x, y, z
	]

class Verts():
	verts = []
	indices = []
	y = 0.0
	index = 0
	edge_loop = []
	sharpness = 0.0

	def __init__(self, x, y, z, index, sharpness):
		self.index = index
		self.y = y
		self.verts = Square(x,y,z)
		self.index = index
		self.indices = [(index*4 + i) for i in [0,1,2,3]]
		self.edge_loop = [(index*4 + i) for i in [0,1,2,3,0]]
		self.sharpness = sharpness

	def __str__(self):
		return str("Verts\n") + \
			"\tverts: " + str(self.verts) + \
			"\n\tindices: " + str(self.indices) + \
			"\n\ty: " + str(self.y) + \
			"\n\tindex: " + str(self.index) + \
			"\n\tedge_loop: " + str(self.edge_loop) + \
			"\n\tsharpness: " + str(self.sharpness)
		
def Cylinder(radius=0.5, height=1.0):
	X_BASE=math.sqrt((radius*radius)/1.5)
	Z_BASE=X_BASE
	LIP_HEIGHT=height*0.08

	DEFAULT_SHARPNESS=1.85
	i = 0

	verts_list = []

	x=X_BASE*0.5
	y=LIP_HEIGHT*0.25
	z=Z_BASE*0.5
	verts_list.append(Verts(x,y,z,i,0))
	i += 1

	x=X_BASE*0.7
	y=0
	z=Z_BASE*0.7
	verts_list.append(Verts(x,y,z,i,DEFAULT_SHARPNESS))
	i += 1

	x=X_BASE*0.85
	y=0
	z=Z_BASE*0.85
	verts_list.append(Verts(x,y,z,i,DEFAULT_SHARPNESS))
	i += 1

	x=X_BASE*0.89
	y=LIP_HEIGHT*0.25
	z=Z_BASE*0.89
	verts_list.append(Verts(x,y,z,i,0))
	i += 1

	x=X_BASE*0.95
	y=LIP_HEIGHT*0.5
	z=Z_BASE*0.95
	verts_list.append(Verts(x,y,z,i,DEFAULT_SHARPNESS))
	i += 1

	x=X_BASE*0.96
	y=LIP_HEIGHT*0.75
	z=Z_BASE*0.96
	verts_list.append(Verts(x,y,z,i,0))
	i += 1

	x=X_BASE
	y=LIP_HEIGHT
	z=Z_BASE
	verts_list.append(Verts(x,y,z,i,DEFAULT_SHARPNESS))
	i += 1

	x=X_BASE
	y=LIP_HEIGHT*2
	z=Z_BASE
	verts_list.append(Verts(x,y,z,i,DEFAULT_SHARPNESS))
	i += 1

	x=X_BASE
	y=height*0.925
	z=Z_BASE
	verts_list.append(Verts(x,y,z,i,DEFAULT_SHARPNESS))
	i += 1

	###########
	# TOP LIP #
	###########

	TOP_LIP_BOTTOM_Y = height*0.95
	TOP_LIP_MIDDLE_Y = height*0.975
	THICKNESS = 0.15
	INNER_XZ = X_BASE * (1-THICKNESS)
	MIDDLE_XZ = X_BASE * (1-THICKNESS/2.0)

	LIP_SHARPNESS=0.1
	LIP_EXTRUDE_FRACTION=1.02

	x=X_BASE
	y=TOP_LIP_BOTTOM_Y
	z=Z_BASE
	verts_list.append(Verts(x,y,z,i,LIP_SHARPNESS))
	i += 1

	x=X_BASE*LIP_EXTRUDE_FRACTION
	y=TOP_LIP_MIDDLE_Y
	z=Z_BASE*LIP_EXTRUDE_FRACTION
	verts_list.append(Verts(x,y,z,i,LIP_SHARPNESS))
	i += 1

	x=MIDDLE_XZ
	y=height
	z=MIDDLE_XZ
	verts_list.append(Verts(x,y,z,i,LIP_SHARPNESS))
	i += 1

	##################
	# INSIDE THE MUG #
	##################

	x=INNER_XZ*(2-LIP_EXTRUDE_FRACTION)
	y=TOP_LIP_MIDDLE_Y
	z=INNER_XZ*(2-LIP_EXTRUDE_FRACTION)
	verts_list.append(Verts(x,y,z,i,LIP_SHARPNESS))
	i += 1

	x=INNER_XZ
	y=TOP_LIP_BOTTOM_Y
	z=INNER_XZ
	verts_list.append(Verts(x,y,z,i,LIP_SHARPNESS))
	i += 1

	x=INNER_XZ
	y=height*0.925
	z=INNER_XZ
	verts_list.append(Verts(x,y,z,i,DEFAULT_SHARPNESS))
	i += 1

	x=INNER_XZ
	y=(height-LIP_HEIGHT*2)/2.0
	z=INNER_XZ
	verts_list.append(Verts(x,y,z,i,DEFAULT_SHARPNESS))
	i += 1

	x=INNER_XZ
	y=LIP_HEIGHT*2
	z=INNER_XZ
	verts_list.append(Verts(x,y,z,i,3))
	i += 1

	x=X_BASE*0.5
	y=LIP_HEIGHT*2
	z=Z_BASE*0.5
	verts_list.append(Verts(x,y,z,i,0))
	i += 1

	edgeloops  = [val for sublist in verts_list for val in sublist.edge_loop]
	verts = [val for sublist in verts_list for val in sublist.verts]

	indices = [
		0,1,2,3
	]
	for i in range(len(verts_list)-1):
		indices = indices + CreateFaceLoop(i)

	# Add final face for inside bottom.
	i = verts_list[len(verts_list)-1].index * 4
	indices = indices + [i+1,i,i+3,i+2]

	num = len(verts_list)
	tags = [ri.CREASE]*num
	nargs = [5,1]*num
	floatargs = [v.sharpness for v in verts_list]
	nfaces = len(indices)/4
	nverts = [4]*nfaces

	return Component(nverts, indices, tags, nargs, edgeloops, floatargs, verts)

class Component():
	nverts = []
	indices = []
	tags = []
	nargs = []
	intargs = []
	floatargs = []
	verts = []

	def __init__(self, nverts, indices, tags, nargs, intargs, floatargs, verts):
		self.nverts = nverts
		self.indices = indices
		self.tags = tags
		self.nargs = nargs
		self.intargs = intargs
		self.floatargs = floatargs
		self.verts = verts

	def draw(self):
		ri.SubdivisionMesh("catmull-clark",
			self.nverts, self.indices, self.tags, self.nargs, self.intargs, self.floatargs, {ri.P: self.verts})

	def add(self, other):
		self.nverts += other.nverts
		start_index = len(self.verts)/3
		self.indices += [i+start_index for i in other.indices]
		self.tags += other.tags
		self.nargs += other.nargs
		self.intargs += [i+start_index for i in other.intargs]
		self.floatargs += other.floatargs
		self.verts += other.verts


def MultipleCyliders():
	height = 4.5
	radius = 2

	ri.AttributeBegin()
	ri.Attribute( 'identifier',{ 'name' :'cylinders'})
	ri.Bxdf('PxrSurface', 'plastic',{
			'color diffuseColor' : [.8, .8, .8],
			'color specularEdgeColor' : [1, 1 , 1],
			'color clearcoatFaceColor' : [.1, .1, .1], 
			'color clearcoatEdgeColor' : [.1, .1, .1],
			'float clearcoatRoughness' : 0.01,
			'float clearcoatThickness' : 1,
	})
	ri.TransformBegin()
	ri.Translate(-6,0,0)
	cylinder = Cylinder(height=height, radius=radius)
	cylinder.draw()
	ri.TransformEnd()

	ri.TransformBegin()
	ri.Translate(0,radius,0)
	ri.Rotate(-70,1,0,0)
	cylinder = Cylinder(height=height, radius=radius)
	cylinder.draw()
	ri.TransformEnd()

	ri.TransformBegin()
	ri.Translate(6,radius,0)
	ri.Rotate(90,1,0,0)
	cylinder = Cylinder(height=height, radius=radius)
	cylinder.draw()
	ri.TransformEnd()
	ri.AttributeEnd()

class HandleVerts():
	verts = []
	indices = []
	index = 0
	edge_loop = []
	sharpness = 0.0
	thickness = 0.0

	def __edge_loop__(self,x1,y1,x2,y2,z):
		return [
			x1, y1, -z,
			x2, y2, -z,
			x2, y2, z,
			x1, y1, z
		]

	def __init__(self, x1, y1, x2, y2, z, index, sharpness):
		self.index = index
		self.verts = self.__edge_loop__(x1,y1,x2,y2,z)
		self.index = index
		self.indices = [(index*4 + i) for i in [0,1,2,3]]
		self.edge_loop = [(index*4 + i) for i in [0,1,2,3,0]]
		self.sharpness = sharpness

	def __str__(self):
		return str("Verts\n") + \
			"\tverts: " + str(self.verts) + \
			"\n\tindices: " + str(self.indices) + \
			"\n\tindex: " + str(self.index) + \
			"\n\tedge_loop: " + str(self.edge_loop) + \
			"\n\tsharpness: " + str(self.sharpness)

def Mug(width=0.5, height=0.5):
	cylinder = Cylinder(height=4.5,radius=2)
	cylinder.draw()
	cylinder.add(Cylinder(height=2,radius=10))
	cylinder.draw()


def HalfHandle(x,y,z,sharpness,sign=1,start_index=0,reverse=False):
	X_BASE = x
	Y_BASE = y
	Z_BASE = z
	SHARPNESS=sharpness
	THICKNESS=0.2*y

	verts_list = []
	i = start_index

	x=X_BASE
	y=Y_BASE*0.75*sign
	z=Z_BASE
	verts_list.append(HandleVerts(x,y,x-THICKNESS,y,z,i,SHARPNESS))
	i += 1

	x=-1
	y=Y_BASE*sign
	z=Z_BASE
	verts_list.append(HandleVerts(x,y,x-THICKNESS,y+3*THICKNESS*sign,z,i,SHARPNESS))
	i += 1

	x=0
	y=(Y_BASE+1)*sign
	z=Z_BASE
	verts_list.append(HandleVerts(x,y,x,y+THICKNESS*sign,z,i,SHARPNESS))
	i += 1

	x=1
	y=Y_BASE*0.85*sign
	z=Z_BASE
	verts_list.append(HandleVerts(x,y,x+THICKNESS,y+THICKNESS*sign,z,i,SHARPNESS))
	i += 1

	if reverse:
		for i in range(len(verts_list)/2):
			a = verts_list[i].verts
			b = verts_list[len(verts_list)-i-1].verts
			verts_list[len(verts_list)-i-1].verts = a
			verts_list[i].verts = b

	return verts_list

def Handle(width=0.5, height=0.5):
	X_BASE=-1
	Y_BASE=2
	Z_BASE=0.5
	SHARPNESS=0.0
	THICKNESS=0.4

	verts_list= []
	verts_list = HalfHandle(X_BASE, Y_BASE, Z_BASE, SHARPNESS)

	i = len(verts_list)
	x=X_BASE*(-1)+0.15
	y=0
	z=Z_BASE
	verts_list.append(HandleVerts(x,y,x+THICKNESS,y,z,i,SHARPNESS))
	i += 1

	other_verts = HalfHandle(X_BASE, Y_BASE, Z_BASE, SHARPNESS, sign=-1, start_index=i, reverse=True)
	for v in other_verts:
		verts_list.append(v)

	# edgeloops  = [val for sublist in verts_list for val in sublist.edge_loop]
	verts = [val for sublist in verts_list for val in sublist.verts]

	tmpedgeloops = []
	tmpnargs = []
	tmpfloatargs = []
	SHARPNESS=0.5
	for i in range(0,4):
		edgeloop = []
		for e in range(len(verts_list)):
			edgeloop.append(i + 4*e)
		tmpedgeloops = tmpedgeloops + edgeloop
		tmpnargs = tmpnargs + [len(edgeloop),1]
		tmpfloatargs.append(SHARPNESS) # Sharpness

	Z_BASE = width/2.0

	indices = [
		0,1,2,3
	]
	for i in range(len(verts_list)-1):
		indices = indices + CreateFaceLoop(i)
	# Add final face for inside bottom.
	i = verts_list[len(verts_list)-1].index * 4
	indices = indices + [i+1,i,i+3,i+2]
	tags = [ri.CREASE]*4
	nargs = tmpnargs
	floatargs = tmpfloatargs
	nfaces = len(indices)/4
	nverts = [4]*nfaces
	ri.SubdivisionMesh("catmull-clark", nverts, indices, tags, nargs, tmpedgeloops, floatargs, {ri.P: verts})

def MultipleHandles():
	ri.TransformBegin()
	ri.Translate(-2,3,0)
	Handle()
	ri.TransformEnd()
	ri.TransformBegin()
	ri.Translate(2,2,0)
	ri.Rotate(70,0,1,0)
	Handle()
	ri.TransformEnd()


ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "Mug.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render") #filename)
# ri.Integrator ('PxrPathTracer' ,'integrator')
ri.Integrator("PxrVisualizer" ,"integrator", {"string style" : "shaded"}, {"normalCheck": 1})

ri.Option('searchpath', {'string texture':'./textures/:@'})
ri.Hider('raytrace' ,{'int incremental' :[1]})
ri.ShadingRate(10)
ri.PixelVariance(0.1)
# ArchiveRecord is used to add elements to the rib stream in this case comments
# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("Mug.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,576,1)
ri.Projection(ri.PERSPECTIVE,{ri.FOV:40}) 
ri.WorldBegin()

# Camera transformation
ri.Translate(0,-3,0)
ri.Translate(0,0,20)
ri.Rotate(-20,1,0,0)

# Lighting
ri.TransformBegin()
ri.AttributeBegin()
ri.Declare('domeLight' ,'string')
ri.Rotate(-90,1,0,0)
ri.Rotate(100,0,0,1)
ri.Light( 'PxrDomeLight', 'domeLight', { 
          'string lightColorMap'  : 'Luxo-Jr_4000x2000.tex'
  })
ri.AttributeEnd()
ri.TransformEnd()

MultipleCyliders()
Table()
MultipleHandles()
# ri.TransformBegin()
# ri.Translate(0,3,0)
# Handle()
# ri.TransformEnd()

# Mug()

ri.WorldEnd()
ri.End()
