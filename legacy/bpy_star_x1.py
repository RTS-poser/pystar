# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 20:12:53 2022

@author: Richard
"""

import bpy
import bmesh
#https://mmas.github.io/linear-transformations-numpy

import numpy as np
import math
from mathutils import Vector, Matrix

codeScenePath = r'D:\Data\StarCitizen\star_x2.blend'

def add_material(obj, material_name, h):
    material = bpy.data.materials.get(material_name)
    if material is None:
        material = bpy.data.materials.new(material_name)
    material.use_nodes = True
    principled_bsdf = material.node_tree.nodes['Principled BSDF']
    if principled_bsdf is not None:
        principled_bsdf.inputs[0].default_value = (*hex_to_rgb(h), 1)  
    
    obj.active_material = material
    obj.material_slots[0].link = 'OBJECT'
    obj.material_slots[0].material = material
    

def hex_to_rgb(value):
    if value[0]=='#':
        value=value[1:]
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

#hello world
#--------------------------------------
#patch code
in_file = r'PU Nav Guide.csv'
import csv
keep_cols = [0,3,5,6,7,12]
new_data = []

with open(in_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        new_row = [row[x] for x in keep_cols]
        try:
            if new_row[0].lower().split()[0] == 'microtech':
                new_data.append(new_row)
        except:
            pass

new_data = [x for x in new_data if x[-1] == 'TRUE'][1:]


#--------------------------------------


#import reference objects
assetPath = r'D:\Blender\Asset Library\StarCitizen\star_primitives.blend'
bpy.ops.wm.open_mainfile(filepath=assetPath)
importObject = bpy.data.objects['Sphere']


#set up user data
xyzOrigin = [-3.0,2.5,3.5]
objName = 'test_string_name'

#template to follow
#copy, modify objects
new_obj = importObject.copy()
new_obj.name = objName
new_obj.location = Vector(xyzOrigin)

#-------------------------
#scaling info

blenderGridSpace = [-10000.0, 10000.0]

all_x = []
all_y = []
all_z = []

#get extents for transform

for sys_name, waypoint,x,y,z,qt in new_data:

#for x,y,z,name in data_rows:
    x = float(x)*1000#-off_x
    y = float(y)*1000#-off_y
    z = float(z)*1000#-off_z
    all_x.append(x)
    all_y.append(y)
    all_z.append(z)

max_x = max(all_x)
max_y = max(all_y)
max_z = max(all_z)
# max_val = max([max_x, max_y, max_z])

min_x = min(all_x)
min_y = min(all_y)
min_z = min(all_z)


max_axis = max([abs(max_x),abs(max_y),abs(max_z),abs(min_x),abs(min_y),abs(min_z)])

starGridSpace = [-1*max_axis, max_axis]

#-------------------------
objLinkList = []

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

abs_origin = (0.0,0.0,0.0)
x_origin = (1.0,0.0,0.0)
y_origin = (0.0,1.0,0.0)
z_origin = (0.0,0.0,1.0)


e = 0
for sys_name, waypoint,x,y,z,qt in new_data:
    oX, oY, oZ = [float(x) for x in [x,y,z]]
    pX = np.interp(oX, starGridSpace, blenderGridSpace)
    pY = np.interp(oY, starGridSpace, blenderGridSpace)
    pZ = np.interp(oZ, starGridSpace, blenderGridSpace)
    
    r_vector = (pX,pY,pZ)
    
    print(pX,pY,pZ)
    
    # #think this is needed for adjusted center point?
    objCenter  = Vector([pX,pY,pZ])
    
    x_angle = math.degrees(angle_between(r_vector, x_origin))
    y_angle = math.degrees(angle_between(r_vector, y_origin))
    z_angle = math.degrees(angle_between(r_vector, z_origin))    
    
    #copy sphere here...
    print('attempting copy here')
    xyzOrigin = Vector(r_vector)
    new_obj = importObject.copy()
    new_obj.name = waypoint
    new_obj.location = Vector(xyzOrigin)
    mat_name = waypoint.split()[0]
    print(mat_name)
    add_material(new_obj, mat_name, '#919191')
    objLinkList.append(new_obj)

# emptyScenePath = r'D:\Temp\empty.blend'  
# bpy.ops.wm.open_mainfile(filepath=emptyScenePath)
# # # build the scene...
C = bpy.context


#   
scene = C.scene

# # 
 





#link objects, from list
for ob in objLinkList:
    C.collection.objects.link(ob)

#save scene...
print('updating scene')
C.view_layer.update()

# #set environment render stuff
bpy.data.scenes['Scene'].view_settings.view_transform = "Standard"

bpy.ops.wm.save_as_mainfile(filepath=codeScenePath)

print(codeScenePath)

print('Done!')



'''

bm = bmesh.new()
bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=0.25)
bm.to_mesh(mesh)




try:
    objName = newName
    mesh = bpy.data.meshes.new(objName)
    obj = bpy.data.objects.new(mesh.name, mesh)
    
    objCenter  = Vector(xyzOrigin)
    blendPoints = []
    for vertCo in targObj.data.vertices:
        blendPoints.append(vertCo.co)
except:
    blendPoints=targObj



verts = blendPoints
edges=[]
faces=[[i for i in range(len(verts))]]
mesh.from_pydata(verts, edges, faces)

#set up metadata for ease of use later...
# attempt update object origin
# objData = obj.data #should already be same thing as mesh???
# https://blender.stackexchange.com/questions/35825/changing-object-origin-to-arbitrary-point-without-origin-set
#note for later, you have to set the origin AFTER linking the object to the scene, otherwise the mesh coordiants are based on local origin and scale outward
mw = obj.matrix_world
imw = mw.inverted()
me = obj.data

origin = objCenter #scene.cursor.location
local_origin = imw @ origin
me.transform(Matrix.Translation(-local_origin))
mw.translation += (origin - mw.translation)
obj['customAlpha']=0.0
'''