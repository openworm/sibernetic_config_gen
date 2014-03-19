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
from Const import Const
import math
from helper.point import Point

class Float4(object):
    '''
    For good vectorization on OpenCL device we need to use 4 dimension vectors
    '''
    def __init__(self, x, y, z, val = 0.0):
        self.x = x
        self.y = y
        self.z = z
        self.val = val
    def __str__(self):
        return str(self.x) +" " + str(self.y) + " " + str(self.z)
    @staticmethod
    def getZeroVector():
        return Float4( 0.0, 0.0, 0.0, 0.0 )
    @staticmethod
    def dist(v1, v2):
        return math.sqrt( (v1.x - v2.x) * (v1.x - v2.x) + (v1.y - v2.y) * (v1.y - v2.y) + (v1.z - v2.z) * (v1.z - v2.z) )
    @staticmethod
    def dot(v1, v2): 
        return (v1.x - v2.x) * (v1.x - v2.x) + (v1.y - v2.y) * (v1.y - v2.y) + (v1.z - v2.z) * (v1.z - v2.z)
class Particle(object):
    def __init__(self, pos_x, pos_y, pos_z, p_type,face_p=False):
        self.position = Float4(pos_x,pos_y,pos_z, type)
        self.face_p = face_p
        self.type = p_type
        self.membranesIndex = [-1]*Const.MAX_MEMBRANES_INCLUDING_SAME_PARTICLE
        self.last_non_zero_val = 0
        if self.type == Const.liquid_particle or self.type == Const.elastic_particle:
            self.velocity = Float4(0.0,0.0,0.0,self.type)
    def ismemindexempty(self):
        isempty = len([l for l in self.membranesIndex if l != -1])
        if isempty == 0:
            return True
        return False
    def insertMem(self,value):
        self.membranesIndex[self.last_non_zero_val] = value
        self.last_non_zero_val += 1
    def setVelocity(self, v):
        self.velocity = Float4(v.x,v.y,v.z)
        self.velocity.val = self.type
    @staticmethod
    def distBetween_particles(p1,p2):
        return Float4.dist( p1.position, p2.position )
    @staticmethod
    def dot_particles(p1,p2):
        return Float4.dot( p1.position, p2.position )
    def  __sub__(self, p1):
        return Point(self.position.x - p1.position.x, self.position.y - p1.position.y, self.position.z - p1.position.z)
    def get_normal(self, membranes, particles):
        #print len(self.faces_l)
        try:
            if not self.ismemindexempty():
                self.n = membranes[self.membranesIndex[0]].get_normal(particles)
                for i in range(1,len(self.membranesIndex),1):
                    self.n = self.n + membranes[self.membranesIndex[i]].get_normal(particles)
                self.n.normalize()
                return self.n
        except ZeroDivisionError as e:
            print str(e)
            print "Problem in point %s because it counldn't be normalize"%(self.index)
