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
from helper.point import Point, Vector3D
import math
import X3DReader

class obj:
    boundary_box = 1
    elastic_box = 2
    liquid_box = 3
    def __init__(self, type=0):
        self.type = type
        self.transforms = []
        self.points = Vertices()
        self.planes = Planes()

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
        self.objects = []
        self.particles = []
        self.elasticConnections = []
        X3DReader.read_model(f_name, self.objects)
        #i = self.objects.points.lowest_point()
        '''
        Translation to 0 0 0 
        '''
        for o in self.objects:
            for p in o.points:
                p.x = int(round(p.x))
                p.y = int(round(p.y))
                p.z = int(round(p.z))
            if o.type ==  obj.boundary_box:
                i_l = o.points.lowest_point()
                i_h = o.points.higest_point()
                v = o.points[i_h] - o.points[i_l]
                Const.xmax =  v.getX()
                Const.ymax =  v.getY()
                Const.zmax =  v.getZ() 
                print Const.xmax
                print Const.ymax
                print Const.zmax 
#                v = Point(-o.points[i_l].x, -o.points[i_l].y, -o.points[i_l].z)
#                for p in o.points:
#                    p.x += v.x
#                    p.y += v.y
#                    p.z += v.z
#                    print str(p.x) + '\t' + str(p.y) + '\t' + str(p.z)
            #Get global coordinates of points
            for t in reversed(o.transforms):
                t.make_transform(o.points)
            #Calculate norm vectors for each plane
            for p in o.planes:
                p.calc_normal(o.points)

#        for p in self.points:
#            trans_v = Vector3D.rotate_v1_around_v2( p, self.world_rot_vector, self.world_rot_vector.angle)
#            p.x = trans_v.x
#            p.y = trans_v.y
#            p.z = trans_v.z
#            print str(p.x) + '\t' + str(p.y) + '\t' + str(p.z)
            
        
    def genConfiguration(self, gen_muscle=False,gen_elastic=False,gen_liquid=True):
        '''
        Main Algorithm
        '''
        for o in self.objects:
            if o.type == obj.boundary_box:
                self.__gen_boundary_p(o)
            if o.type == obj.liquid_box:
                self.__gen_liquid_p(o)
        
    
    def __gen_boundary_p(self, o):
        '''
        On first step calculate normales for vertices 
        On second step calc normales for point which should locate on edges
        '''
        for p in o.points:
            x = p.getX() + Const.xmax / 2.0
            y = p.getY() + Const.ymax / 2.0
            z = p.getZ() + Const.xmax / 2.0
            particle = Particle(x,y,z, Const.boundary_particle)
            particle.setVelocity(p.get_normal())
            self.particles.append(particle)
        #second Step Create point for all eges
        check_e = []
        #return
        for plane in o.planes:
            for e in plane.edges:
                if not (((str(e[0]) + '\t' + str(e[1])) in check_e) or ((str(e[1]) + '\t' + str(e[0])) in check_e)):
                    v = o.points[e[1]] - o.points[e[0]]
                    l = (v.length() * float(Const.TRANF_CONST) * Const.r0)
                    v.normalize()
                    v *= l
                    for step in self.__my_range(Const.r0,l ,Const.r0):
                        v1 = v * (step / l)
                        p = Point( v1.x + o.points[e[0]].getX(), v1.y + o.points[e[0]].getY(), v1.z + o.points[e[0]].getZ() )
                        p.faces_l = Point.find_common_plane(o.points[e[0]], o.points[e[1]])
                        x = p.x + Const.xmax / 2.0#p.getX() 
                        y = p.y + Const.ymax / 2.0#p.getY()
                        z = p.z + Const.xmax / 2.0#p.getZ()
                        particle = Particle(x,y,z, Const.boundary_particle)
                        particle.setVelocity(p.get_normal())
                        self.particles.append(particle)
                    check_e.append(str(e[0]) + '\t' + str(e[1]))
        #return
        #third step create particles for all planes
        for plane in o.planes:
            plane.calcBigArea(o.points)
            e1 = plane.edges[0]
            e2 = plane.edges[len(plane.edges) - 1]
            v1 = o.points[e2[0]] - o.points[e2[1]]
            v2 = o.points[e1[1]] - o.points[e1[0]]
            l1 = (v1.length() * (Const.TRANF_CONST) * Const.r0)
            l2 = (v2.length() * (Const.TRANF_CONST) * Const.r0)
            v1_temp = v1.clone()
            v2_temp = v2.clone()
            v1.normalize()
            v2.normalize()
            v1 *= l1
            v2 *= l2
            for stepX in self.__my_range(Const.r0,l1,Const.r0):
                for stepY in self.__my_range(Const.r0,l2,Const.r0):
                    alpha = ( stepX / l1 )
                    beta = ( stepY / l2 )
                    v_temp_1 = (v1_temp * alpha) + (v2_temp * beta)
                    p_temp = Point(v_temp_1.x + o.points[e1[0]].x,v_temp_1.y + o.points[e1[0]].y,v_temp_1.z + o.points[e1[0]].z)
                    if plane.checkPoint(p_temp,o.points):
                        v_temp = (v1 * alpha) + (v2 * beta)
                        p = Point(v_temp.x + o.points[e1[0]].getX(),v_temp.y + o.points[e1[0]].getY(),v_temp.z + o.points[e1[0]].getZ())
                        x = p.x + Const.xmax / 2.0
                        y = p.y + Const.ymax / 2.0
                        z = p.z + Const.xmax / 2.0
                        particle = Particle(x,y,z, Const.boundary_particle)
                        particle.setVelocity(plane.getNormal())
                        self.particles.append(particle)
        print "boundary particle %s" %len(self.particles) 
    
    def __gen_liquid_p(self, o):
        i = o.points.lowest_point()
        xmin = o.points[i].getX()
        ymin = o.points[i].getY()
        zmin = o.points[i].getZ()
        adj_points = o.points[i].get_adj_points()
        if len(adj_points) == 3:
            ort1 = o.points[adj_points[0]] - o.points[i]
            ort2 = o.points[adj_points[1]] - o.points[i]
            ort3 = o.points[adj_points[2]] - o.points[i]
            for x in self.__my_range(xmin, ort1.length() * (Const.TRANF_CONST) * Const.r0, Const.r0):
                for y in self.__my_range(ymin, ort2.length() * (Const.TRANF_CONST) * Const.r0, Const.r0):
                    for z in self.__my_range(zmin, ort3.length() * (Const.TRANF_CONST) * Const.r0, Const.r0):
                        particle = Particle(x + Const.xmax / 2.0,y + Const.ymax / 2.0,z + Const.zmax / 2.0,Const.liquid_particle)
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
    
