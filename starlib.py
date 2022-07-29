#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 12:54:45 2022

@author: richard
"""

import numpy as np
import math
from scipy.optimize import minimize

names = '''
OM-1
OM-2
OM-3
OM-4
OM-5
OM-6
New Babbage
Port Tressler
Comm Array ST4-22
Rayari Deltana Research Outpost
Shubin Mining Facility SM0-10
Shubin Mining Facility SM0-13
Shubin Mining Facility SM0-18
Shubin Mining Facility SM0-22
SM0-10
SM0-13
SM0-18
SM0-22
MT DataCenter 2UB-RB9-5
MT DataCenter 4HJ-LVE-A
MT DataCenter 5WQ-R2V-C
MT DataCenter 8FK-Q2X-K
MT DataCenter D79-ECG-R
MT DataCenter E2Q-NSG-Y
MT DataCenter QVX-J88-J
MT DataCenter TMG-XEV-2
MT DataCenter L8P-JUC-8
MT SecurityCenter DDV-6
MT DataCenter KH3-AAE-L
2UB-RB9-5
4HJ-LVE-A
5WQ-R2V-C
8FK-Q2X-K
D79-ECG-R
E2Q-NSG-Y
QVX-J88-J
TMG-XEV-2
L8P-JUC-8
DDV-6
KH3-AAE-L
Calhoun Pass Emergency Shelter
Clear View Emergency Shelter
Nuiqsut Emergency Shelter
Point Wain Emergency Shelter
Necropolis (Stash House)
Outpost 54 (Stash House)        
'''.strip().split('\n')


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

def xyz_to_degrees(xyz_vals):
    abs_origin = (0.0,0.0,0.0)
    x_origin = (1.0,0.0,0.0)
    y_origin = (0.0,1.0,0.0)
    z_origin = (0.0,0.0,1.0)
    
    dom_prime = y_origin

    oX, oY, oZ = xyz_vals

    
    r_vector = (oX, oY, oZ)    
    x_vector = [oX, oY, 0.0]
    x_degree = math.degrees(angle_between(x_vector, dom_prime))    
    
    #attempt western hemisphere adjustment here (see notes)
    #hard coded
    if oX >0:
        x_degree=x_degree*-1
    
    
    


    x_radian = math.radians(x_degree)
    # rz_matrix = Matrix([[math.cos(x_radian),-1*math.sin(x_radian),0],
    #                    [math.sin(x_radian), math.cos(x_radian),0],
    #                    [0,0,1]])
    rz_matrix = np.array([[math.cos(x_radian),-1*math.sin(x_radian),0],
                        [math.sin(x_radian), math.cos(x_radian),0],
                        [0,0,1]])
    
    new_x_vector = np.array(dom_prime)
        
    
    # proj_x_vector = rz_matrix@new_x_vector
    proj_x_vector = np.matmul(rz_matrix, new_x_vector)
    
    proj_y_degree = math.degrees(angle_between(proj_x_vector, r_vector))
    
    if oZ <0:
        proj_y_degree=proj_y_degree*-1

    # print(obj.name, '\t', x_degree, proj_y_degree)
    return x_degree, proj_y_degree

def gps_solve(distances_to_station, stations_coordinates, solver = 'Nelder-Mead'):
    def error(x, c, r):
        return sum([(np.linalg.norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])

    l = len(stations_coordinates)
    S = sum(distances_to_station)
    # compute weight vector for initial guess
    W = [((l - 1) * S) / (S - w) for w in distances_to_station]
    # get initial guess of point location
    x0 = sum([W[i] * stations_coordinates[i] for i in range(l)])
    # optimize distance from signal origin to border of spheres
    return minimize(error, x0, args=(stations_coordinates, distances_to_station), method='Nelder-Mead').x

#https://stackoverflow.com/questions/54873868/python-calculate-bearing-between-two-lat-long
def get_bearing(lat1, long1, lat2, long2):
    dLon = (long2 - long1)
    print(dLon)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    print('x',x)
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    print('y',y)
    brng = np.arctan2(x,y)
    brng = np.degrees(brng)
    
    #correct for compass...
    if brng < 0:
        brng = 360 + brng

    return brng