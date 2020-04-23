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
		-x, y, z,
		x, y, z,
		x, y, -z
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

	# 0
	x=X_BASE*0.7
	y=LIP_HEIGHT*0.5
	z=Z_BASE*0.7
	bottom_verts_inner_top = Verts(x,y,z,0,DEFAULT_SHARPNESS)

	# 1
	x=X_BASE*0.8
	y=0
	z=Z_BASE*0.8
	bottom_verts_inner_bottom = Verts(x,y,z,1,DEFAULT_SHARPNESS)

	# 2
	x=X_BASE*0.9
	y=0
	z=Z_BASE*0.9
	bottom_verts_outer_bottom = Verts(x,y,z,2,DEFAULT_SHARPNESS)

	# 3
	x=X_BASE*0.95
	y=LIP_HEIGHT*0.5
	z=Z_BASE*0.95
	bottom_verts_outer_middle = Verts(x,y,z,3,DEFAULT_SHARPNESS)

	# 4
	x=X_BASE
	y=LIP_HEIGHT
	z=Z_BASE
	bottom_verts_outer_top = Verts(x,y,z,4,DEFAULT_SHARPNESS)

	# 5
	x=X_BASE
	y=height*0.8
	z=Z_BASE
	top_verts_outer_bottom = Verts(x,y,z,5,DEFAULT_SHARPNESS)

	# 6
	x=X_BASE
	y=height*0.85
	z=Z_BASE
	top_verts_outer_middle_bottom = Verts(x,y,z,6,0.1)

	# 7
	x=X_BASE*1.01
	y=height*0.92
	z=Z_BASE*1.01
	top_verts_outer_middle_top = Verts(x,y,z,7,0.1)

	# 8
	x=X_BASE
	y=height
	z=Z_BASE
	top_verts_outer_top = Verts(x,y,z,8,0.1)

	# 9
	x=X_BASE * 0.9
	y=height
	z=Z_BASE * 0.9
	top_verts_inner = Verts(x,y,z,9,DEFAULT_SHARPNESS)

	# 10
	x=X_BASE*0.9
	y=LIP_HEIGHT*2
	z=Z_BASE*0.9
	bottom_verts_inner = Verts(x,y,z,10,3)
	
	verts_list = [
		bottom_verts_inner_top,
		bottom_verts_inner_bottom,
		bottom_verts_outer_bottom,
		bottom_verts_outer_middle,
		bottom_verts_outer_top,
		top_verts_outer_bottom,
		top_verts_outer_middle_bottom,
		top_verts_outer_middle_top,
		top_verts_outer_top,
		top_verts_inner,
		bottom_verts_inner
	]

	edgeloops  = [val for sublist in verts_list for val in sublist.edge_loop]
	verts = [val for sublist in verts_list for val in sublist.verts]

	indices = [
		0,1,2,3
	]
	for i in range(len(verts_list)-1):
		indices = indices + CreateFaceLoop(i)

	# Add final face for inside bottom.
	i = bottom_verts_inner.index * 4
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
	# ri.Bxdf('PxrSurface', 'plastic',{
    #       'color diffuseColor' : [1, 1, 1],
    #       'color clearcoatFaceColor' : [.5, .5, .5], 
    #       'color clearcoatEdgeColor' : [.25, .25, .25]
	# })
	# ri.Bxdf('PxrSurface', 'metal', {
    #       'float diffuseGain' : [0],
    #       'int specularFresnelMode' : [1],
    #       'color specularEdgeColor' : [1 ,1 ,1],
    #       'color specularIor' : [4.3696842, 2.916713, 1.654698],
    #       'color specularExtinctionCoeff' : [5.20643, 4.2313662, 3.7549689],
    #       'float specularRoughness' : [0.1], 
    #       'integer specularModelType' : [1] 
  	# })

	ri.TransformBegin()
	ri.Translate(-6,1,0)
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

filename = "Cube.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render") #filename)
ri.Integrator ('PxrPathTracer' ,'integrator',{})
ri.Option('searchpath', {'string texture':'./textures/:@'})
ri.Hider('raytrace' ,{'int incremental' :[1]})
ri.ShadingRate(10)
ri.PixelVariance (0.1)
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

# Camera transformation
ri.Translate(0,-3,0)
ri.Translate(0,0,20)
ri.Rotate(-20,1,0,0)

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
