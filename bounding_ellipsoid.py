# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 15:11:11 2019

@author: DFSCHMIDT
"""

#!/usr/bin/env python3

import numpy as np
import basic_functions as bf
import test_image_ellipsoid as tie
import bounding_box as bbox
import plot

# Creating ellipsoidal test image
test_image_coord = tie.ellipsoid_test_image(10000, 100., 50., 30., 5., np.pi/7., np.pi/6.)
plot.bbox_plot(tie.ellipsoid_test_image(10000, 100., 50., 30., 0., 0., 0.), 0., 0., 2)

def bounding_ellipsoid_optim(coord, tol):
    """
    Compute the smallest bounding ellidpsoid of a cloud of points
    Needs the required precision (tol) 
    and the coordinates (3D array) of the cloud of points
    """
    # finding optimal bounding box
    bbox_initial_guess =  [0., 0.]
    bbox_res = bbox.bbox_optim(coord, bbox_initial_guess)
    plot.bbox_plot(coord, bbox_res.x[0], bbox_res.x[1], 100)
        
    # rotation of the cloud of oints in the main direction of the bbox    
    M = bf.rotation(bbox_res.x[0], bbox_res.x[1], 'xy')
    coord_rot = np.dot(coord, M)
    #plot.bbox_plot(coord_rot, 0., 0., 2)
    
    # initial a, b, c
    a = np.sqrt((max(coord_rot[:, 0])-min(coord_rot[:, 0]))**2)/2.
    b = np.sqrt((max(coord_rot[:, 1])-min(coord_rot[:, 1]))**2)/2.
    c = np.sqrt((max(coord_rot[:, 2])-min(coord_rot[:, 2]))**2)/2.      

    volume_before = 0.
    volume = 4./3.*np.pi*a*b*c
     
    while abs(volume - volume_before) > tol:
        volume_before = volume
        # test if points outside the bounded ellipsoid 
        for i in range(len(coord)):
            if (coord[i,0]**2/a**2+coord[i,1]**2/b**2+coord[i,2]**2/c**2)>1:        
                point_outside = 'true'
                break
            else:
                point_outside = 'false'
                      
        if point_outside == 'true':
            a_before = a
            b_before = b
            c_before = c
            a = a*1.05
            b = b*1.05
            c = c*1.05
        elif point_outside == 'false':
            a1 = a_before
            b1 = b_before
            c1 = c_before
            a_before = a
            b_before = b
            c_before = c
            a = a + abs(a1-a)/2.
            b = b + abs(b1-b)/2.
            c = c + abs(c1-c)/2. 
        volume = 4./3.*np.pi*a*b*c
        """
        print(point_outside)
        print('before =', volume_before)
        """
        
    print('volume =', volume)
    print('a = ', a,'b = ', b,'c = ', c)
    plot.fit_ellipsoid_plot(coord_rot, a, b, c, 10000)
    return volume, a, b, c

"""
optim = bounding_ellipsoid_optim(test_image_coord, 1e-3)
print(optim)

plot.fit_ellipsoid_plot(coord_rot, optim[1], optim[2], optim[3], 10000)
"""    



