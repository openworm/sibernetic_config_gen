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
import math

'''
Created on 13.02.2013

@author: Sergey Khayrulin
'''
from Const import Const
from Particle import Particle, Float4
from ElasticConnection import ElasticConnection
from helper.collections import Vertices, Planes
from helper.point import Point
import X3DReader


class Obj:
    boundary_box = 1
    elastic_box = 2
    liquid_box = 3

    def __init__(self, t=0):
        self.type = t
        self.transforms = []
        self.points = Vertices()
        self.planes = Planes()


class Generator(object):
    """
    Configuration Generator class: class generate configuration 
    for initial size of box
    """
    def __init__(self, f_name):
        """
        Constructor
        It's important that sizes of box are multiple with r0 = h * 0.5
        Because it should be integer number of boundary particles 
        TODO: more detailed comment...
        """
        self.objects = []
        self.particles = []
        self.elasticConnections = []
        X3DReader.read_model(f_name, self.objects)
        '''
        Translation to 0 0 0 
        '''
        try:
            for o in self.objects:
                # Get global coordinates of points
                for t in reversed(o.transforms):
                    t.make_transform(o.points)
                if o.type == Obj.boundary_box:
                    i_l = o.points.lowest_point()
                    i_h = o.points.higest_point()
                    v = o.points[i_h] - o.points[i_l]
                    Const.xmax = v.get_x()
                    Const.ymax = v.get_y()
                    Const.zmax = v.get_z()
                for p in o.planes:
                    p.set_normal(o.points)
        except ZeroDivisionError as ex:
            print ex

    def gen_configuration(self):
        """
        Main Algorithm
        """
        for o in self.objects:
            if o.type == Obj.boundary_box:
                self.__gen_boundary_p(o)
            if o.type == Obj.liquid_box:
                self.__gen_liquid_p(o)
            if o.type == Obj.elastic_box:
                self.__gen_elastic_p(o)

    def __gen_boundary_p(self, o):
        """
        On first step calculate normal for vertices
        On second step calc normal for point which should locate on edges
        """
        offset = 0
        for p in o.points:
            x = p.get_x() + Const.xmax / 2.0 + offset
            y = p.get_y() + Const.ymax / 2.0 + offset
            z = p.get_z() + Const.zmax / 2.0 + offset
            particle = Particle(x, y, z, Const.boundary_particle)
            particle.set_velocity(p.get_normal)
            self.particles.append(particle)
        # second Step Create point for all eges
        check_e = []
        # return
        for plane in o.planes:
            if len(plane.vertices) > 3:
                for e in plane.edges:
                    if not (((str(e[0]) + '\t' + str(e[1])) in check_e) or ((str(e[1]) + '\t' + str(e[0])) in check_e)):
                        v = o.points[e[1]] - o.points[e[0]]
                        l = (v.length() * float(Const.TRANF_CONST) * Const.r0)
                        v.normalize()
                        v *= l
                        for step in self.__my_range(Const.r0, l, Const.r0):
                            v1 = v * (step / l)
                            p = Point(v1.x + o.points[e[0]].get_x(), v1.y + o.points[e[0]].get_y(),
                                      v1.z + o.points[e[0]].get_z())
                            p.faces = Point.find_common_plane(o.points[e[0]], o.points[e[1]])
                            x = p.x + Const.xmax / 2.0 + offset # p.getX()
                            y = p.y + Const.ymax / 2.0 + offset # p.getY()
                            z = p.z + Const.zmax / 2.0 + offset # p.getZ()
                            particle = Particle(x, y, z, Const.boundary_particle)
                            particle.set_velocity(p.get_normal)
                            self.particles.append(particle)
                        check_e.append(str(e[0]) + '\t' + str(e[1]))
        #return
        # third step create particles for all planes
        for plane in o.planes:
            if len(plane.vertices) > 3: # for faces with only 3 vertices we now can not generate
                plane.calc_area(o.points)
                plane.getBigestEdges(o.points)
                e1 = plane.eX  # plane.edges[0]
                e2 = plane.eY  # plane.edges[len(plane.edges) - 1]
                if e1[0] == plane.start:
                    v1 = o.points[e1[1]] - o.points[e1[0]]
                else:
                    v1 = o.points[e1[0]] - o.points[e1[1]]
                if e2[0] == plane.start:
                    v2 = o.points[e2[1]] - o.points[e2[0]]
                else:
                    v2 = o.points[e2[0]] - o.points[e2[1]]
                l1 = (v1.length() * Const.TRANF_CONST * Const.r0)
                l2 = (v2.length() * Const.TRANF_CONST * Const.r0)
                v1_temp = v1.clone()
                v2_temp = v2.clone()
                v1.normalize()
                v2.normalize()
                v1 *= l1
                v2 *= l2
                for stepX in self.__my_range(Const.r0, l1, Const.r0):
                    for stepY in self.__my_range(Const.r0, l2, Const.r0):
                        alpha = (stepX / l1)
                        beta = (stepY / l2)
                        v_temp_1 = (v1_temp * alpha) + (v2_temp * beta)
                        p_temp = Point(v_temp_1.x + o.points[plane.start].x, v_temp_1.y + o.points[plane.start].y,
                                       v_temp_1.z + o.points[plane.start].z)
                        if plane.check_point(p_temp, o.points):
                            v_temp = (v1 * alpha) + (v2 * beta)
                            p = Point(v_temp.x + o.points[plane.start].get_x(), v_temp.y + o.points[plane.start].get_y(),
                                      v_temp.z + o.points[plane.start].get_z())
                            x = p.x + Const.xmax / 2.0 + offset
                            y = p.y + Const.ymax / 2.0 + offset
                            z = p.z + Const.zmax / 2.0 + offset
                            particle = Particle(x, y, z, Const.boundary_particle)
                            particle.set_velocity(plane.get_normal)
                            self.particles.append(particle)
        print "boundary particle %s" % len(self.particles)

    def __gen_liquid_p(self, o):
        i = o.points.lowest_point()
        localxmin = o.points[i].get_x()
        localymin = o.points[i].get_y()
        localzmin = o.points[i].get_z()
        adj_points = o.points[i].get_adj_points()
        start_num = len(self.particles)
        tempparticleslist = []
        if len(adj_points) == 3:
            ort1 = o.points[adj_points[0]] - o.points[i]
            ort2 = o.points[adj_points[1]] - o.points[i]
            ort3 = o.points[adj_points[2]] - o.points[i]
            for x in self.__my_range(localxmin, localxmin + ort1.length() * Const.TRANF_CONST * Const.r0, Const.r0):
                for y in self.__my_range(localymin, localymin + ort2.length() * Const.TRANF_CONST * Const.r0, Const.r0):
                    for z in self.__my_range(localzmin, localzmin + ort3.length() * Const.TRANF_CONST * Const.r0, Const.r0):
                        offset = Const.r0 / 2.0
                        particle = Particle(x + Const.xmax / 2.0 + offset, y + Const.ymax / 2.0 + offset, z + Const.zmax / 2.0 + offset,
                                            Const.liquid_particle)
                        tempparticleslist.append(particle)
		#Next several linea is needed for generation flowing into the pipe
        #R = Const.r0 * 10.5
        #centerP = Particle(Const.xmax / 2.0, Const.ymax / 2.0, Const.zmax / 2.0, Const.liquid_particle)
        #tt = filter(lambda p: math.sqrt((p.position.x - centerP.position.x)**2 + (p.position.z - centerP.position.z)**2)<R, tempparticleslist) #abs(p.position.x - centerP.position.x) < R and abs(p.position.z - centerP.position.z) < R
        #tt = filter(lambda p: abs(p.position.y - centerP.position.y) < 30.0 *Const.r0, tt) #abs(p.position.x - centerP.position.x) < R and abs(p.position.z - centerP.position.z) < R
        tt = tempparticleslist
        self.particles.extend(tt)
        print "generated liquid particles:%s" % (str(len(self.particles) - start_num))


    def __gen_elastic_p(self, o):
        i = o.points.lowest_point()
        localxmin = o.points[i].get_x()
        localymin = o.points[i].get_y()
        localzmin = o.points[i].get_z()
        adj_points = o.points[i].get_adj_points()
        _eparticles = []
        if len(adj_points) == 3:
            ort1 = o.points[adj_points[0]] - o.points[i]
            ort2 = o.points[adj_points[1]] - o.points[i]
            ort3 = o.points[adj_points[2]] - o.points[i]
            for x in self.__my_range(localxmin, localxmin + ort1.length() * Const.TRANF_CONST * Const.r0, Const.r0):
                for y in self.__my_range(localymin, localymin + ort2.length() * Const.TRANF_CONST * Const.r0, Const.r0):
                    for z in self.__my_range(localzmin, localzmin + ort3.length() * Const.TRANF_CONST * Const.r0, Const.r0):
                        offset = -7.0 * Const.r0 / 2.0
                        particle = Particle(x + Const.xmax / 2.0 + offset, y + Const.ymax / 2.0 , z + Const.zmax / 2.0,
                                            Const.elastic_particle)
                        _eparticles.append(particle)
        print "elastic particle:%s" % (len(_eparticles))
        _eparticles.extend(self.particles)
        self.particles = _eparticles
        self.__gen_connections()

    def __gen_connections(self, filter_type=[Const.boundary_particle, Const.liquid_particle]):
        elasticparticles = [p for p in self.particles if p.type == Const.elastic_particle]
        searchset = [p for p in self.particles if not(p.type in filter_type)]
        for p in elasticparticles:
            self.__gen_elastic_conn(p, searchset)
        print "generated elastic connections:%s" % (len(self.elasticConnections))

    def __my_range(self, start, end, step):
        while start < end:
            yield start
            start += step

    def __gen_elastic_conn(self, particle, elasticparticles):
        """
        Find elastc neighbour for particle
        extend elastic connections listS
        """
        neighbour_collection = [p for p in elasticparticles if
                                Particle.dot_particles(particle, p) <= Const.r0_squared * 3.05 and p != particle]
        neighbour_collection.sort(key=lambda p: Particle.dist_between_particles(particle, p))
        if len(neighbour_collection) > Const.MAX_NUM_OF_NEIGHBOUR:
            neighbour_collection = neighbour_collection[0:Const.MAX_NUM_OF_NEIGHBOUR]
        elastic_connections_collection = []
        for p in neighbour_collection:
            val1 = 1.1
            elastic_connections_collection.append(
                ElasticConnection(self.particles.index(p), Particle.dist_between_particles(p, particle), val1, 0))
        '''
        If number of elastic connection less that MAX_NUM_OF_NEIGHBOUR then 
        we extend collection of elastic connection with non particle value
        '''
        if len(neighbour_collection) < Const.MAX_NUM_OF_NEIGHBOUR:
            elastic_connections_collection.extend([ElasticConnection(Const.NO_PARTICEL_ID, 0, 0, 0)] * (
            Const.MAX_NUM_OF_NEIGHBOUR - len(neighbour_collection)))
        self.elasticConnections.extend(elastic_connections_collection)
