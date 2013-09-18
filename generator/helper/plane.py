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
eps = 0.000000001
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
    def calcBigArea(self,points):
        s1 = self.__getArea(points[self.edges[0][1]] - points[self.edges[0][0]], points[self.edges[3][1]] - points[self.edges[3][0]])
        s2 = self.__getArea(points[self.edges[1][1]] - points[self.edges[1][0]], points[self.edges[2][1]] - points[self.edges[2][0]]) 
        self.area = s1 + s2 
    def __getArea(self,a,b):
        ab = Vector3D.cross_prod(a, b)
        return ab.length()/2.0
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
    def checkPoint(self, p, points):
        b_s = 0
#        if abs(self.area - 3.0) <= eps:
#            print '======================='
#            print str(p.x) + "\t" + str(p.y) + "\t" + str(p.z)
#            e1 = self.edges[0]
#            e2 = self.edges[len(self.edges) - 1]
#            v1 = points[e2[0]] - points[e2[1]]
#            v2 = points[e1[1]] - points[e1[0]]
#            print self.area
#            print v1.length()
#            print v2.length()
#            #v1.normalize()
#            #v2.normalize()
#            print str(v1.x) + "\t" + str(v1.y) + "\t" + str(v1.z)
#            print str(v2.x) + "\t" + str(v2.y) + "\t" + str(v2.z)
#            print str(points[e1[0]].x) + "\t" + str(points[e1[0]].y) + "\t" + str(points[e1[0]].z)
        for e in self.edges:
            a = Vector3D(points[e[0]].x - p.x, points[e[0]].y - p.y, points[e[0]].z - p.z)
            b = Vector3D(points[e[1]].x - p.x, points[e[1]].y - p.y, points[e[1]].z - p.z)
            b_s += self.__getArea(a, b)
        if abs(b_s - self.area) <= eps:
            return True
        return False
            
        