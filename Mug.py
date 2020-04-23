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

	ri.SubdivisionMesh("catmull-clark", nverts, indices, tags, nargs, edgeloops, floatargs, {ri.P: verts})

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
	Cylinder(height=height, radius=radius)
	ri.TransformEnd()

	ri.TransformBegin()
	ri.Translate(0,radius,0)
	ri.Rotate(-70,1,0,0)
	Cylinder(height=height, radius=radius)
	ri.TransformEnd()

	ri.TransformBegin()
	ri.Translate(6,radius,0)
	ri.Rotate(90,1,0,0)
	Cylinder(height=height, radius=radius)
	ri.TransformEnd()
	ri.AttributeEnd()

ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "Mug.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render") #filename)
ri.Integrator ('PxrPathTracer' ,'integrator')
# ri.Integrator("PxrVisualizer" ,"integrator", {"string style" : "shaded"}, {"normalCheck": 1})
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

ri.WorldEnd()
ri.End()
