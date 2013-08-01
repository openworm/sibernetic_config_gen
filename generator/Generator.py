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

@author: Sergey Khayrulin
'''
from Const import Const
from Particle import Particle, Float4
from ElasticConnection import ElasticConnection
from helper.collections import Vertices, Planes
from helper.point import Point
import math
import X3DReader


class Generator(object):
    '''
    Configuration Generator class: class generate configuration 
    for initial size of box
    '''
    def __init__(self, f_name):
        '''
        Constructor
        It's important that sizes of box are multiple with r0 = h * 0.5
        Because it should be integer number of boundary particles 
        TODO: more detailed comment...
        '''
        self.particles = []
        self.elasticConnections = []
        self.points = Vertices()
        self.planes = Planes()
        X3DReader.read_model(f_name, self.points, self.planes)
        i = self.points.lowest_point()
        '''
        Translation to 0 0 0 
        '''
        for p in self.points:
            p.x = int(round(p.x))
            p.y = int(round(p.y))
            p.z = int(round(p.z))
        for p in self.planes:
            p.calc_normal(self.points)
        
        
    def genConfiguration(self, gen_muscle=False,gen_elastic=False,gen_liquid=True):
        '''
        Main Algorithm
        '''
        self.__gen_boundary_p()
        pass
    
    def __gen_boundary_p(self):
        '''
        On first step calculate normales for vertices 
        On second step calc normales for point which should locate on edges
        '''
        for p in self.points:
            x = p.getX()
            y = p.getY()
            z = p.getZ()
            particle = Particle(x,y,z, Const.boundary_particle)
            particle.setVelocity(p.get_normal())
            self.particles.append(particle)
        #second Step Create point for all eges
        check_e = []
        #return
        for plane in self.planes:
            for e in plane.edges:
                if not (((str(e[0]) + '\t' + str(e[1])) in check_e) or ((str(e[1]) + '\t' + str(e[0])) in check_e)):
                    v = self.points[e[1]] - self.points[e[0]]
                    l = (len(v) * (Const.TRANF_CONST) * Const.r0)
                    v.normalize()
                    v *= l
                    for step in self.__my_range(Const.r0,l - Const.r0,Const.r0):
                        v1 = v * (step / l)
                        p = Point( v1.x + self.points[e[0]].getX(), v1.y + self.points[e[0]].getY(), v1.z + self.points[e[0]].getZ() )
                        p.faces_l = Point.find_common_plane(self.points[e[0]], self.points[e[1]])
                        x = p.x#p.getX() 
                        y = p.y#p.getY()
                        z = p.z#p.getZ()
                        particle = Particle(x,y,z, Const.boundary_particle)
                        particle.setVelocity(p.get_normal())
                        self.particles.append(particle)
                    check_e.append(str(e[0]) + '\t' + str(e[1]))
        #return
        #third step create particles for all planes
        for plane in self.planes:
            e1 = plane.edges[0]
            e2 = plane.edges[len(plane.edges) - 1]
            v1 = self.points[e2[0]] - self.points[e2[1]]
            v2 = self.points[e1[1]] - self.points[e1[0]]
            l1 = (len(v1) * (Const.TRANF_CONST) * Const.r0)
            l2 = (len(v2) * (Const.TRANF_CONST) * Const.r0)
            v1.normalize()
            v2.normalize()
            v1 *= l1
            v2 *= l2
            for stepX in self.__my_range(Const.r0,l1 - Const.r0,Const.r0):
                for stepY in self.__my_range(Const.r0,l2 - Const.r0,Const.r0):
                    v_temp = (v1 * ( stepX / l1 )) + (v2 * ( stepY / l2 ))
                    p = Point(v_temp.x + self.points[e1[0]].getX(),v_temp.y + self.points[e1[0]].getY(),v_temp.z + self.points[e1[0]].getZ())
                    #p.faces_l.append(plane)
                    x = p.x
                    y = p.y
                    z = p.z
                    particle = Particle(x,y,z, Const.boundary_particle)
                    particle.setVelocity(plane.getNormal())
                    self.particles.append(particle)
    def __my_range(self, start, end, step):
        while start < end:
            yield start
            start += step     
    def __genElasticConn(self, particle, elasticParticles):
        '''
        Find elastc neighbour for particle
        extend elastic connections list
        '''
        nMi = elasticParticles.index(particle)*self.nMuscles/len(elasticParticles);
        neighbour_collection = [p for p in elasticParticles if Particle.dot_particles(particle, p) <= Const.r0_squared * 3.05 and p != particle ]
        neighbour_collection.sort(key=lambda p: Particle.distBetween_particles(particle, p))
        if len(neighbour_collection) > Const.MAX_NUM_OF_NEIGHBOUR:
            neighbour_collection = neighbour_collection[0:Const.MAX_NUM_OF_NEIGHBOUR]
        elastic_connections_collection = []
        for p in neighbour_collection:
            nMj = elasticParticles.index(p) * self.nMuscles / len(elasticParticles)
            val1 = 0
            if self.nMuscles > 0:
                if nMj == nMi:
                    dx2 = particle.position.x - p.position.x
                    dy2 = particle.position.y - p.position.y
                    dz2 = particle.position.z - p.position.z
                    dx2 *= dx2
                    dy2 *= dy2
                    dz2 *= dz2 
                    val1 = (1.1+nMi)*float((dz2 > 100*dx2)and(dz2 > 100*dy2))  
            elastic_connections_collection.append( ElasticConnection(self.particles.index(p),Particle.distBetween_particles(p,particle), val1, 0) )
        '''
        If number of elastic connection less that MAX_NUM_OF_NEIGHBOUR then 
        we extend collection of elastic connection with non particle value
        '''
        if len(neighbour_collection) < Const.MAX_NUM_OF_NEIGHBOUR:
            elastic_connections_collection.extend([ElasticConnection(Const.NO_PARTICEL_ID,0,0,0)] * (Const.MAX_NUM_OF_NEIGHBOUR - len(neighbour_collection)) )
        self.elasticConnections.extend( elastic_connections_collection )
    
