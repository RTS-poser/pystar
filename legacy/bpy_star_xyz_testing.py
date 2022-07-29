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

codeScenePath = r'D:\Data\StarCitizen\star_geom_testing.blend'




#import reference objects
# assetPath = r'D:\Blender\Asset Library\StarCitizen\star_primitives.blend'
bpy.ops.wm.open_mainfile(filepath=codeScenePath)
# importObject = bpy.data.objects['Sphere']


sphObjects = []

for obj in bpy.data.objects:
    # print(obj.name)
    # print('Sphere' in obj.name)
    if 'Sphere' in obj.name:
        sphObjects.append(obj)







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

dom_prime = y_origin

e = 0
# for sys_name, waypoint,x,y,z,qt in new_data:

# print("rotation axis lookup from x_origin:  x-->Z, y-->Y")
print("rotation axis lookup from y_origin:  x-->Z, y-->X")
for obj in sphObjects:    
    oX, oY, oZ = obj.location

    
    r_vector = (oX, oY, oZ)    
    x_vector = [oX, oY, 0.0]
    x_degree = math.degrees(angle_between(x_vector, dom_prime))    
    
    #attempt western hemisphere adjustment here (see notes)
    #hard coded
    if oX >0:
        x_degree=x_degree*-1
    
    
    


    x_radian = math.radians(x_degree)
    rz_matrix = Matrix([[math.cos(x_radian),-1*math.sin(x_radian),0],
                       [math.sin(x_radian), math.cos(x_radian),0],
                       [0,0,1]])
    
    new_x_vector = Vector(dom_prime)
        
    
    proj_x_vector = rz_matrix@new_x_vector
    proj_y_degree = math.degrees(angle_between(proj_x_vector, r_vector))
    
    if oZ <0:
        proj_y_degree=proj_y_degree*-1

    print(obj.name, '\t', x_degree, proj_y_degree)        

'''
notes

Sphere 	 33.32511229066547 34.162922788702026          Correct as is                   - 33.32511229066547 34.162922788702026
Sphere.001 	 42.198513606083075 85.21980284392662      x needs negative, Y is WAY off  - correct w/ west!
Sphere.002 	 135.86375843983916 88.5420174129467       x needs negative, Y is WAY off  - correct w/ west!
Sphere.003 	 144.73942786554176 36.341911591282255     correct AS IS!   (??)           - 144.73942786554176 36.341911591282255
Sphere.004 	 46.448211118436994 32.078500861561615     x good, y needs negative        - still off, no worse...
Sphere.005 	 37.76006269346708 78.3348480455373        x needs negative, Y is WAY off? - x good, y needs negative
Sphere.006 	 148.34734766649342 67.33323888871018      x needs negative, Y is WAY off? - x good, y needs negative
Sphere.007 	 140.048127844526 28.26341268201537        x good, y needs negative        - still off, no worse...

#patterns and assessment

spheres 0 and 3 are correct, exist in x-degrees plus, y plus, on north/eastern quad

spheres 4, 7 are both iun south-eastern hemisphere...


spheres 1, 2, 5, 6 all have the same errors, with gross error on Y
    ALL exist on X minus
    all in western hemisphere

FIX ONE: adjust sign for western hemisphere, corrects worst Y issues, all X issues?

AFTER FIX ONE

if Z is negative, need to reverse Y angle, should fix

FIX TWO: if southern hemisphere (-Z) correct Y angles
    



'''
print('Done!')

