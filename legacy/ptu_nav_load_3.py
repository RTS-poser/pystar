# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 16:29:39 2022

@author: Richard
"""

in_file = r'PU Nav Guide.csv'

import csv
import numpy as np
import math 

import bpy
from mathutils import Vector, Matrix

import json

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

keep_cols = [0,3,5,6,7,12]

new_header = ['sys_name','waypoint','x','y','z','qt']

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

new_data = [x for x in new_data if x[-1] == 'TRUE']

abs_origin = (0.0,0.0,0.0)
x_origin = (1.0,0.0,0.0)
# x_origin = (-1.0,0.0,0.0)
y_origin = (0.0,1.0,0.0)
z_origin = (0.0,0.0,1.0)

dom_axis = x_origin


counter_1 = 0

print("x-->Z, y-->Y")

out_data = {}


for row in new_data:
    counter_1 = counter_1 + 1
    x,y,z = float(row[2])*1000,float(row[3])*1000,float(row[4])*1000
    place_name = row[1]
    
    out_data[place_name]= [x,y,z]
    print(place_name)



with open(r'\\Chronos\NasDataStore\Projects\StarCitizen\microtech.json', 'w') as temp:
    temp.write(json.dumps(out_data, indent=4))
print('Done')

    # # print(place_name, x,y,z)
    
    # #get degrees from vecotr math?
    
    # r_vector = [x,y,z]

    # #view is top down
    # #this is CORRECT, for X+ reference marker only!
    # x_vector = [x,y,0.0]
    
    # x_degree = math.degrees(angle_between(x_vector, x_origin))
    

    
    
    
    # #NEW method, not yet right, but better option!?!
    # #old method may be wrong, need to shift frame of reference by x_degrees first!?!
    # #try Matrix and a rotation matrix based off of x_degree?
    
    # #adjust x_degree BEFORE you use it for derived math...
    
    # if y<0:
    #     x_degree=x_degree*-1
    
    
    
    
        
    
    # x_radian = math.radians(x_degree)
    # rz_matrix = Matrix([[math.cos(x_radian),-1*math.sin(x_radian),0],
    #                    [math.sin(x_radian), math.cos(x_radian),0],
    #                    [0,0,1]])
    
    # new_x_vector = Vector(x_origin)
        
    
    # proj_x_vector = rz_matrix@new_x_vector
    # proj_y_degree = math.degrees(angle_between(proj_x_vector, r_vector))
    
    # # print('actual x degrees?', x_degree)
    # # print()
    # # print('projected y degrees:', proj_y_degree)



    # # print('''
    # #       you need to figure out the 3d equivelent of quadrants
          
    # #       basically when do you use native angles and when do you have to correct?  for example 90-angle, or 180-angle?
          
    # #       you're getting closer...
          
          
    # #       test each [octant] of the sphere?  or try quadrants?
    # #       ''')
          
    # #this part is WRONG or INCOMPLETE
    # # if z>0:
    # #     proj_y_degree=proj_y_degree*-1.0
    # # if y<0:
    # #     x_degree=x_degree*-1.0
    
    
    # # #OLD METHOD, PROBABLY wrong
    # # #view is Y axis
    # # y_vector = [0.0,y,z]
    # # y_degree = math.degrees(angle_between(y_vector, y_origin))
    # # print('orig y degrees:', y_degree)
          
    # # if x<0:
    # #     y_degree=y_degree*-1.0
    # # if z<0:
    # #     x_degree=x_degree*-1.0
    
    # print_line = [place_name, x_degree,proj_y_degree,x,y,z]
    # print_line = [place_name, x_degree, proj_y_degree]
    
    # print('\t'.join([str(x1) for x1 in print_line]))

    # if place_name == 'Nuiqsut Emergency Shelter':
    #     break
