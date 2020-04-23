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
	# 0
	x=X_BASE*0.5
	y=LIP_HEIGHT*0.25
	z=Z_BASE*0.5
	bottom_verts_inner_top = Verts(x,y,z,i,0)
	i += 1

	# 1
	x=X_BASE*0.7
	y=0
	z=Z_BASE*0.7
	bottom_verts_inner_bottom = Verts(x,y,z,i,DEFAULT_SHARPNESS)
	i += 1

	# 2
	x=X_BASE*0.85
	y=0
	z=Z_BASE*0.85
	bottom_verts_outer_bottom = Verts(x,y,z,i,DEFAULT_SHARPNESS)
	i += 1

	x=X_BASE*0.89
	y=LIP_HEIGHT*0.25
	z=Z_BASE*0.89
	bottom_verts_outer_middle_lower = Verts(x,y,z,i,0)
	i += 1

	# 3
	x=X_BASE*0.95
	y=LIP_HEIGHT*0.5
	z=Z_BASE*0.95
	bottom_verts_outer_middle = Verts(x,y,z,i,DEFAULT_SHARPNESS)
	i += 1

	# 4
	x=X_BASE*0.96
	y=LIP_HEIGHT*0.75
	z=Z_BASE*0.96
	bottom_verts_outer_middle_upper = Verts(x,y,z,i,0)
	i += 1

	# 5
	x=X_BASE
	y=LIP_HEIGHT
	z=Z_BASE
	bottom_verts_outer_top = Verts(x,y,z,i,DEFAULT_SHARPNESS)
	i += 1

		# 5
	x=X_BASE
	y=LIP_HEIGHT*2
	z=Z_BASE
	bottom_verts_outer_top_above = Verts(x,y,z,i,DEFAULT_SHARPNESS)
	i += 1

	# 6
	x=X_BASE
	y=height*0.8
	z=Z_BASE
	top_verts_outer_bottom = Verts(x,y,z,i,DEFAULT_SHARPNESS)
	i += 1

	# 7
	x=X_BASE
	y=height*0.85
	z=Z_BASE
	top_verts_outer_middle_bottom = Verts(x,y,z,i,0.1)
	i += 1

	# 8
	x=X_BASE*1.01
	y=height*0.92
	z=Z_BASE*1.01
	top_verts_outer_middle_top = Verts(x,y,z,i,0.1)
	i += 1

	# 9
	x=X_BASE
	y=height
	z=Z_BASE
	top_verts_outer_top = Verts(x,y,z,i,0.1)
	i += 1

	# 10
	x=X_BASE * 0.85
	y=height
	z=Z_BASE * 0.85
	top_verts_inner = Verts(x,y,z,i,DEFAULT_SHARPNESS)
	i += 1

	# 11
	x=X_BASE * 0.85
	y=(height-LIP_HEIGHT*2)/2.0
	z=Z_BASE * 0.85
	middle_verts_inner = Verts(x,y,z,i,DEFAULT_SHARPNESS)
	i += 1

	x=X_BASE*0.85
	y=LIP_HEIGHT*2
	z=Z_BASE*0.85
	bottom_verts_inner_middle = Verts(x,y,z,i,3)
	i += 1

	# 12
	x=X_BASE*0.5
	y=LIP_HEIGHT*2
	z=Z_BASE*0.5
	bottom_verts_inner_center = Verts(x,y,z,i,0)
	i += 1
	
	verts_list = [
		bottom_verts_inner_top,
		bottom_verts_inner_bottom,
		bottom_verts_outer_bottom,
		bottom_verts_outer_middle_lower,
		bottom_verts_outer_middle,
		bottom_verts_outer_middle_upper,
		bottom_verts_outer_top,
		bottom_verts_outer_top_above,
		top_verts_outer_bottom,
		top_verts_outer_middle_bottom,
		top_verts_outer_middle_top,
		top_verts_outer_top,
		top_verts_inner,
		middle_verts_inner,
		bottom_verts_inner_middle,
		bottom_verts_inner_center
	]

	edgeloops  = [val for sublist in verts_list for val in sublist.edge_loop]
	verts = [val for sublist in verts_list for val in sublist.verts]

	indices = [
		0,1,2,3
	]
	for i in range(len(verts_list)-1):
		indices = indices + CreateFaceLoop(i)

	# Add final face for inside bottom.
	i = bottom_verts_inner_center.index * 4
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
	# ri.Bxdf( 'PxrDisney','ceramic', {
	# 	'color baseColor' : [ 0.8, 0.8, 0.8],
	# 	'float specularRoughness': [0.01],
	# })
	# ri.Bxdf('PxrSurface', 'greenglass',{ 
	# 	'color refractionColor' : [0,0.9,0],
	# 	'color diffuseColor' : [1, 1, 1],
	# 	'float diffuseGain' : 0,
	# 	'color specularEdgeColor' : [0.2, 1 ,0.2],
	# 	'float refractionGain' : [1.0],
	# 	'float reflectionGain' : [1.0],
	# 	'float glassRoughness' : [0.01],
	# 	'float glassIor' : [1.5],
	# 	'color extinction' : [0.0, 0.2 ,0.0],	
	# })
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

filename = "Cube.rib"
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
ri.Display("Cube.exr", "it", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,576,1)
# ri.Format(1024, 720, 1)
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

# height = 4.5
# radius = 2

# ri.AttributeBegin()
# ri.Attribute( 'identifier',{ 'name' :'cylinder'})
# # ri.Bxdf( 'PxrDisney','ceramic', {
# # 	'color baseColor' : [ 0.8, 0.8, 0.8],
# # 	'float specularRoughness': [0.01],
# # })
# ri.Bxdf('PxrSurface', 'greenglass',{ 
# 	'color refractionColor' : [0,0.9,0],
# 	'color diffuseColor' : [1, 1, 1],
# 	'float diffuseGain' : 0,
# 	'color specularEdgeColor' : [0.2, 1 ,0.2],
# 	'float refractionGain' : [1.0],
# 	'float reflectionGain' : [1.0],
# 	'float glassRoughness' : [0.01],
# 	'float glassIor' : [1.5],
# 	'color extinction' : [0.0, 0.2 ,0.0],	
# })
# ri.TransformBegin()
# ri.Translate(0,0,0)
# Cylinder(height=height, radius=radius)
# ri.TransformEnd()
# ri.AttributeEnd()

MultipleCyliders()
Table()

ri.WorldEnd()
ri.End()
