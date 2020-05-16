#!/usr/bin/python
import prman
import math
import argparse

NUM_CYLINDER_VERTS=4

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
	faces = [i+(startindex*NUM_CYLINDER_VERTS) for i in faces]
	return faces

def CreateEdgeLoop(startindex=0):
	edges = [0,1,2,3,0]
	edges = [i+(startindex*NUM_CYLINDER_VERTS) for i in edges]
	return edges

def Square(x,y,z,angle):
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
	voffset = 0.0

	def __init__(self, x, y, z, index, sharpness, voffset=0.5):
		self.index = index
		self.y = y
		self.verts = Square(x,y,z,10)
		self.index = index
		self.indices = [(index*NUM_CYLINDER_VERTS + i) for i in range(NUM_CYLINDER_VERTS)]
		self.edge_loop = [(index*NUM_CYLINDER_VERTS + i) for i in (range(NUM_CYLINDER_VERTS)+[0])]
		self.sharpness = sharpness
		self.voffset = voffset

	def __str__(self):
		return str("Verts\n") + \
			"\tverts: " + str(self.verts) + \
			"\n\tindices: " + str(self.indices) + \
			"\n\ty: " + str(self.y) + \
			"\n\tindex: " + str(self.index) + \
			"\n\tedge_loop: " + str(self.edge_loop) + \
			"\n\tsharpness: " + str(self.sharpness) + \
			"\n\tvoffset: " + str(self.voffset)

	def v(self, i):
		return self.verts[i]

def distance(v1,v2):
	x_dist = v2[0]-v1[0]
	y_dist = v2[1]-v1[1]
	z_dist = v2[2]-v1[2]
	return math.sqrt(x_dist**2 + y_dist**2 + z_dist**2)

def getUVCoords(verts=None):
	full_dist = 0.0
	v1 = []
	v2 = []
	for i in range(0,len(verts)-1):
		va = verts[i]
		vb = verts[i+1]
		v1 = [va.verts[0],va.verts[1],va.verts[2]]
		v2 = [vb.verts[0],vb.verts[1],vb.verts[2]]
		full_dist+=distance(v1,v2)

	uvs=[]
	uvs.append([
		[0.0,0.0],
		[0.25,0.0],
		[0.5,0.0],
		[0.75,0.0]
	])
	distance_so_far = 0
	for i in range(1,len(verts)-1):
		va = verts[i]
		vb = verts[i-1]
		v1 = [va.verts[0],va.verts[1],va.verts[2]]
		v2 = [vb.verts[0],vb.verts[1],vb.verts[2]]
		distance_so_far+=distance(v1,v2)
		f = distance_so_far/full_dist
		uvs.append([
			[0.0,f],
			[0.25,f],
			[0.5,f],
			[0.75,f]])
	uvs.append([
		[0.0,1.0],
		[0.25,1.0],
		[0.5,1.0],
		[0.75,1.0]
	])

	new_uvs=[]
	new_uvs.append([0.0,0.0])
	new_uvs.append([0.25,0.0])
	new_uvs.append([0.5,0.0])
	new_uvs.append([0.75,0.0])
	for i in range(0,len(uvs)-1):
		for j in range(0,3):
			new_uvs.append(uvs[i][0+j])
			new_uvs.append(uvs[i+1][0+j])
			new_uvs.append(uvs[i+1][1+j])
			new_uvs.append(uvs[i][1+j])
		new_uvs.append(uvs[i][3])
		new_uvs.append(uvs[i+1][3])
		new_uvs.append([1.0,uvs[i+1][3][1]])
		new_uvs.append([1.0,uvs[i][3][1]])

	new_uvs.append([0.0,1.0])
	new_uvs.append([0.25,1.0])
	new_uvs.append([0.5,1.0])
	new_uvs.append([0.75,1.0])

	uvs = []
	for uv in new_uvs:
		uvs+=uv

	return uvs

def Cylinder(radius=2, height=4.5):
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
	uvs = getUVCoords(verts_list)

	indices = [
		0,1,2,3
	]
	nverts = [4]
	for i in range(len(verts_list)-1):
		indices = indices + CreateFaceLoop(i)
		nverts += [4]*4

	# Add final face for inside bottom.
	i = verts_list[len(verts_list)-1].index * NUM_CYLINDER_VERTS
	indices += [i+1,i,i+3,i+2]
	nverts += [4]

	num = len(verts_list)
	tags = [ri.CREASE]*num
	nargs = [NUM_CYLINDER_VERTS+1,1]*num
	floatargs = [v.sharpness for v in verts_list]

	return Component(nverts, indices, tags, nargs, edgeloops, floatargs, verts, uvs)

class Component():
	nverts = []
	indices = []
	tags = []
	nargs = []
	intargs = []
	floatargs = []
	verts = []
	uvs = []

	def __init__(self, nverts, indices, tags, nargs, intargs, floatargs, verts, uvs):
		self.nverts = nverts
		self.indices = indices
		self.tags = tags
		self.nargs = nargs
		self.intargs = intargs
		self.floatargs = floatargs
		self.verts = verts
		self.uvs = uvs

	def draw(self):
		ri.SubdivisionMesh("catmull-clark",
			self.nverts, self.indices, self.tags,
			self.nargs, self.intargs, self.floatargs,
			{ri.P: self.verts, 'facevarying float[2] st' : self.uvs})

	def add(self, other):
		self.nverts += other.nverts
		start_index = len(self.verts)/3
		self.indices += [i+start_index for i in other.indices]
		self.tags += other.tags
		self.nargs += other.nargs
		self.intargs += [i+start_index for i in other.intargs]
		self.floatargs += other.floatargs
		self.verts += other.verts
		self.uvs += other.uvs

def MultipleCyliders():
	height = 4.5
	radius = 2

	ri.AttributeBegin()
	ri.Attribute( 'identifier',{ 'name' :'cylinders'})
	ri.Bxdf('PxrSurface', 'plastic',{
			'color diffuseColor' : [.8, .8, .8],
			'color specularEdgeColor' : [1, 1, 1],
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

	def __edge_loop__(self,x1,y1,x2,y2,z1,z2):
		return [
			x1, y1, z1,
			x2, y2, z2,
			x2, y2, -z2,
			x1, y1, -z1
		]

	def __init__(self, x1, y1, x2, y2, z1, z2, index, sharpness, z_fan=1.0):
		z2 = z1*z_fan
		self.index = index
		self.verts = self.__edge_loop__(x1,y1,x2,y2,z1,z2)
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

def Mug(height=4.5, radius=2):
	ri = prman.Ri()
	ri.AttributeBegin()
	ri.Attribute( 'identifier',{ 'name' :'mug'})
	
	ri.Pattern('PxrVoronoise', 'voronoise',
	{
		'float jitter': [1.0],
		'float smoothness': [0.0],
		'float frequency': [40.0]
	})

	colorVarience = """
	$val=noise($P);
	$color=ccurve($val,  
		0.000, $base, 4,  
		0.590, $base*$fraction, 4);
	$color
	"""
	ri.Pattern('PxrSeExpr', 'seColorVariance',
	{
		'color base' : [1.0,1.0,1.0],
		'float fraction' : [0.9], 
		'string expression' : [colorVarience]
	})
	ri.Pattern('smudge', 'smudge', {'color Cin': [1.0,1.0,1.0]})
	ri.Pattern('logo', 'logo',
		{
			'color Cin': [1.0,1.0,1.0],
			'reference float chips' : ['voronoise:resultF'],
		}
	)
	ri.Pattern('scratch', 'scratch',
		{
			'color Cin': [0.15,0.15,0.15],
			'reference color logo': ['logo:Cout']
		}
	)

	# ri.Displace('PxrDisplace', 'displaceTexture',
	# {   
	# 	'reference float dispScalar' : ['voronoise:resultF'],
	# 	'uniform float dispAmount' : [0.001],
	# })

	ri.AttributeBegin()
	ri.Displace('PxrDisplace', 'displaceTexture',
	{   
		'reference float dispScalar' : ['logo:mag'],
		'uniform float dispAmount' : [0.005],
	})
	ri.Attribute("dice",{"float micropolygonlength":1}) # Smaller number reduces tearing.
	ri.Bxdf('PxrSurface', 'plastic',{
		# 'reference color diffuseColor' : ['seColorVariance:resultRGB'],
		# 'reference color diffuseColor' : ['logo:Cout'],
		'reference color diffuseColor' : ['scratch:Cout'],
		# 'reference color diffuseColor' : ['seScratch:resultRGB'],
		'color clearcoatFaceColor' : [.1, .1, .1], 
		'color clearcoatEdgeColor' : [.1, .1, .1],
		'reference float clearcoatRoughness' : ['smudge:mag'],
		'float clearcoatThickness' : 1,
	})
	cylinder = Cylinder()
	cylinder.draw()
	ri.AttributeEnd()
	ri.AttributeBegin()
	ri.TransformBegin()
	ri.Rotate(-90,0,1,0)
	ri.Translate(2.1,2.4,0)
	ri.Bxdf('PxrSurface', 'plastic',{
		'reference color diffuseColor' : ['seColorVariance:resultRGB'],
		'color clearcoatFaceColor' : [.1, .1, .1], 
		'color clearcoatEdgeColor' : [.1, .1, .1],
		'reference float clearcoatRoughness' : ['smudge:mag'],
		'float clearcoatThickness' : 1,
	})
	Handle(height=height/5)
	ri.TransformEnd()
	ri.AttributeEnd()
	ri.AttributeEnd()

def HalfHandle(x,y,z,sharpness,thickness,sign=1,start_index=0,reverse=False,height=2):
	X_BASE = x
	Y_BASE = y
	Z_BASE = z
	SHARPNESS=10
	THICKNESS=thickness

	verts_list = []
	i = start_index

	x=X_BASE*0.4*-1
	y=(Y_BASE*0.8)*sign
	z=Z_BASE*0.7
	verts_list.append(HandleVerts(x,y,x-3*THICKNESS,y,z,-z,i,SHARPNESS,z_fan=1.2))
	i += 1

	x=X_BASE*0.5*-1
	y=(Y_BASE+0.8*height)*sign
	z=Z_BASE
	verts_list.append(HandleVerts(x,y,x-2.6*THICKNESS,y+2.8*THICKNESS*sign,z,-z,i,SHARPNESS,z_fan=1.2))
	i += 1

	x=X_BASE*0.2
	y=(Y_BASE+1.2*height)*sign
	z=Z_BASE
	verts_list.append(HandleVerts(x,y,x,y+1.5*THICKNESS*sign,z,-z,i,SHARPNESS))
	i += 1

	x=X_BASE*0.7
	y=(Y_BASE+0.7*height)*sign
	z=Z_BASE
	verts_list.append(HandleVerts(x,y,x+THICKNESS,y+THICKNESS*sign,z,-z,i,SHARPNESS))
	i += 1

	if reverse:
		for i in range(len(verts_list)/2):
			a = verts_list[i].verts
			b = verts_list[len(verts_list)-i-1].verts
			verts_list[len(verts_list)-i-1].verts = a
			verts_list[i].verts = b

	return verts_list

def Handle(width=1, height=2, center_y=0.5):

	X_BASE=width
	Y_BASE=height/2.0
	Z_BASE=0.3
	SHARPNESS=0.0
	THICKNESS=height/4.7

	verts_list = HalfHandle(X_BASE, Y_BASE, Z_BASE, SHARPNESS, thickness=THICKNESS, height=height)

	i = len(verts_list)
	x=width
	y=0
	z=Z_BASE
	verts_list.append(HandleVerts(x,y,x+THICKNESS,y,z,-z,i,SHARPNESS))
	i += 1

	other_verts = HalfHandle(X_BASE, Y_BASE, Z_BASE, SHARPNESS, thickness=THICKNESS, sign=-1, start_index=i, reverse=True, height=height)
	for v in other_verts:
		verts_list.append(v)

	verts = [val for sublist in verts_list for val in sublist.verts]

	# TODO: Change this to take sharpness from edges.

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
	# return Component(nverts, indices, tags, nargs, tmpedgeloops, floatargs, verts)

def MultipleHandles():
	ri.TransformBegin()
	ri.Translate(-2,3,0)
	Handle(height=2, width=1.5)
	ri.TransformEnd()
	ri.TransformBegin()
	ri.Translate(2,2,0)
	ri.Rotate(70,0,1,0)
	Handle()
	ri.TransformEnd()

def MultipleMugs():
	ri.TransformBegin()
	ri.Translate(-1,0,0)
	ri.Rotate(90,0,1,0)
	Mug()
	ri.TransformEnd()

	ri.TransformBegin()
	ri.Translate(4,0,0)
	ri.Rotate(-20,0,1,0)
	Mug()
	ri.TransformEnd()

	ri.TransformBegin()
	ri.Translate(-6,1.5,2)
	ri.Rotate(-110,0,1,0)
	ri.Rotate(-110,1,0,0)
	ri.Rotate(100,0,0,1)
	Mug()
	ri.TransformEnd()

parser = argparse.ArgumentParser(description='Render a mug.')
parser.add_argument('-d', dest='debug', action='store_true')
parser.add_argument('-p', dest='prod', action='store_true')
parser.add_argument('-f', dest='rib', action='store_true')
parser.add_argument('-i', dest='image', action='store_true')
args = parser.parse_args()

ri = prman.Ri()
ri.Option("rib", {"string asciistyle": "indented"})

filename = "Mug.rib"

if args.rib:
	ri.Begin(filename)
else:
	ri.Begin("__render")

if args.debug:
	ri.Integrator("PxrVisualizer" ,"integrator", {"string style" : "st"}, {"normalCheck": 0})
else:
	ri.Integrator('PxrPathTracer' ,'integrator')

ri.Declare("st","facevarying float[2]")

ri.Attribute('displacementbound', {'float sphere' : [0.1], ri.COORDINATESYSTEM:"object"})
ri.Option('searchpath', {'string texture':'./textures/:@'})
ri.Hider('raytrace' ,{'int incremental' :[1]})

if args.prod:
	ri.ShadingRate(0.1)
	ri.PixelVariance(0.01)
	ri.Format(1920,1080,1)
else:
	ri.ShadingRate(10)
	ri.PixelVariance(1)
	ri.Format(720,576,1)

if args.image:
	ri.Display("Mug.exr", "file", "rgba")
else:
	ri.Display("Mug.exr", "it", "rgba")
	
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 
ri.WorldBegin()

# Camera transformation
ri.Translate(0,-1.5,0)
ri.Translate(0,0,10)
ri.Rotate(-20,1,0,0)

# Lighting
ri.TransformBegin()
ri.AttributeBegin()
ri.Declare('domeLight' ,'string')
ri.Translate(0,0,40)
ri.Rotate(-90,1,0,0)
ri.Rotate(100,0,0,1)
ri.Light( 'PxrDomeLight', 'domeLight', { 
		  'string lightColorMap'  : 'lebombo_4k.tex'
  })
ri.AttributeEnd()
ri.TransformEnd()

Table()
MultipleMugs()

ri.WorldEnd()
ri.End()