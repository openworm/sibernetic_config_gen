# The MIT License (MIT)
#
# Copyright (c) 2011, 2013 OpenWorm.
# http://openworm.org
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the MIT License
# which accompanies this distribution, and is available at
# http://opensource.org/licenses/MIT
#
# Contributors:
#      OpenWorm - http://openworm.org/people.html
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
# USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import with_statement
'''
Created on 13.02.2013

@author: Serg
'''

class Const(object):
    '''
    Const 
    '''
    h = 3.34
    r0 = h * 0.5
    r0_squared = r0 * r0
    mass = 0.0003#3.25e-14
    #PROPERTY OF BOX
    xmin = 0
    ymin = 0
    zmin = 0
    xmax = 0
    ymax = 0    
    zmax = 0
    simulationScale = 0.004 * pow(mass,1.0/3.0)/pow(0.00025,1.0/3.0);
    #PROPERTY FIELDS
    liquid_particle = 1.1
    elastic_particle = 2.1
    boundary_particle = 3.1 
    #CONFIGURATION PARTICLE COUNT
    MAX_NUM_OF_NEIGHBOUR = 32
    LIQUID_PARTICLE_COUNT = 0
    ELASTIC_PARTICLE_COUNT = 0
    PARTICLE_COUNT = LIQUID_PARTICLE_COUNT + ELASTIC_PARTICLE_COUNT
    NO_PARTICEL_ID = -1.0
    '''
    Number of boundary particles depends from sizes of box.
    So I think don't include their in PARTICLE_COUNT
    '''
    BOUNDARY_PARTICLE_COUNT = 0 
    TOTAL_PARTICLE_COUNT = BOUNDARY_PARTICLE_COUNT + PARTICLE_COUNT 
    TRANF_CONST = 10
    
