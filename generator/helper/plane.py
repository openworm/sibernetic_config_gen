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
Created on Jul 29, 2013

@author: serg
'''
from point import Vector3D

class Plane(object):
    '''
    classdocs
    '''
    def __init__(self, vertices=[], points=None):
        '''
        Constructor
        '''
        self.vertices = [ int(v) for v in vertices if v != '']
        '''
        List of all edges for current plane
        '''
        self.edges = []
        for i in range(len(self.vertices)):
            j = (i + 1) <= len(self.vertices) - 1 and i + 1 or 0  
            item = [self.vertices[i],self.vertices[j]]
            self.edges.append(item) 
            
            #[[self.vertices[i], (i + 1) <= len(self.vertices) - 1 and self.vertices[i + 1] or self.vertices[0]] for i in range(len(self.vertices))] 
    def getNormal(self):
        '''
        TODO: check of definition of normal
        '''
        return self.normal
    def calc_normal(self,points):
        a = points[self.vertices[1]] - points[self.vertices[0]]
        b = points[self.vertices[len(self.vertices)-1]] - points[self.vertices[0]]
        self.normal = Vector3D.cross_prod(a, b)
        self.normal.normalize()