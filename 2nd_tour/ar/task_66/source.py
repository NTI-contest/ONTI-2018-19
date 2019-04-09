# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 00:33:33 2019
@author: DNS
"""

import math
#import matplotlib.pyplot as plt

import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in degrees between vectors 'v1' and 'v2':
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return math.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

def get_vectors(pA, pB, center):
    AO = [center[0] - pA[0], center[1] - pA[1]]
    BO = [center[0] - pB[0], center[1] - pB[1]]
    return AO, BO
    
    
def haversine(coord1, coord2):
    lon1 = coord1[0]
    lon2 = coord2[0]
    lat1 = coord1[1]
    lat2 = coord2[1]
    EARTH_RADIUS = 6371000
    
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    dec_m = EARTH_RADIUS * c
    return dec_m


def points_in_rad(center_coord, arr, radius = 2000):
    sorted_arr = sorted(arr)
    
    pointsInRadius = []
    
    for i in range(0, len(sorted_arr)):
        if(haversine((center_coord), sorted_arr[i]) <= radius):
            pointsInRadius.append(sorted_arr[i])
    return pointsInRadius





arr =  [(104.2607150000, 52.2509700000), 
        (104.3047200000, 52.2876890000), 
        (104.2963780000, 52.2908390000), 
        (104.2807670000, 52.2834890000), 
        (104.2899250000, 52.2738040000), 
        (104.2899250000, 52.2738040000), 
        (104.2920600000, 52.2732450000), 
        (104.2672810000, 52.2513130000), 
        (104.2921130000, 52.2742630000), 
        (104.2852950000, 52.2773480000), 
        (104.2805530000, 52.2779920000), 
        (104.2992640000, 52.2784380000), 
        (104.2987450000, 52.2785310000), 
        (104.2839000000, 52.2787930000), 
        (104.2839430000, 52.2784510000), 
        (104.2934170000, 52.2985000000), 
        (104.2866900000, 52.2892410000), 
        (104.2831170000, 52.2918110000), 
        (104.2945860000, 52.3006260000), 
        (104.2776020000, 52.2751160000), 
        (104.2884280000, 52.2935860000)]


sorted_arr = sorted(arr)
max_points_in_radius = 0

max_coord_r = ()


max_lon = max(list(zip(*arr))[0])
     

lon = min(list(zip(*arr))[0])
lat = min(list(zip(*arr))[1])
center_coord = (lon, lat)

   
for i in range(0, 1000):
    if lon - max_lon > 0.1:
        break
    lon += 0.001
    lat = 52.23
    points_in_radius = 0
    ps = 0
    for j in range(0, 1000):
        lat += 0.001
        center_coord = (lon, lat)
        
        if center_coord in arr:
            pass
        else:
            points_in_radius = len(points_in_rad(center_coord, arr))
           
        if points_in_radius > max_points_in_radius:
            max_points_in_radius = points_in_radius
            max_coord_r = center_coord


max_lon = max(list(zip(*arr))[0])
max_lat = max(list(zip(*arr))[1])

print(max_coord_r)
print(max_points_in_radius)