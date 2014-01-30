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
from membrane import membrane

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
        self.membranes = []
        self.particleMembranes = []
        X3DReader.read_model(f_name, self.objects)
        #i = self.objects.points.lowest_point()
        '''
        Translation to 0 0 0 
        '''
        for o in self.objects:
            if o.type ==  obj.boundary_box:
                for p in o.points:
                    p.x = int(round(p.x))
                    p.y = int(round(p.y))
                    p.z = int(round(p.z))
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
            if o.type == obj.elastic_box:
                self.__gen_elastic_p(o)
                #self.__gen_elastic_p_any_surface(o)
        
    
    def __gen_boundary_p(self, o):
        '''
        On first step calculate normales for vertices 
        On second step calc normales for point which should locate on edges
        '''
        before = len(self.particles)
        for p in o.points:
            x = p.getX() + Const.xmax / 2.0
            y = p.getY() + Const.zmax / 2.0
            z = p.getZ() + Const.zmax / 2.0
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
                        y = p.y + Const.zmax / 2.0#p.getY()
                        z = p.z + Const.zmax / 2.0#p.getZ()
                        particle = Particle(x,y,z, Const.boundary_particle)
                        particle.setVelocity(p.get_normal())
                        self.particles.append(particle)
                    check_e.append(str(e[0]) + '\t' + str(e[1]))
        #return
        #third step create particles for all planes
        for plane in o.planes:
            plane.calcBigArea(o.points)
            plane.getBigestEdges(o.points)
            e1 = plane.eX#plane.edges[0]
            e2 = plane.eY#plane.edges[len(plane.edges) - 1]
            if e1[0] == plane.start:
                v1 = o.points[e1[1]] - o.points[e1[0]]
            else:
                v1 = o.points[e1[0]] - o.points[e1[1]]
            if e2[0] == plane.start:
                v2 = o.points[e2[1]] - o.points[e2[0]]
            else:
                v2 = o.points[e2[0]] - o.points[e2[1]]
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
                    p_temp = Point(v_temp_1.x + o.points[plane.start].x,v_temp_1.y + o.points[plane.start].y,v_temp_1.z + o.points[plane.start].z)
                    if plane.checkPoint(p_temp,o.points):
                        v_temp = (v1 * alpha) + (v2 * beta)
                        p = Point(v_temp.x + o.points[plane.start].getX(),v_temp.y + o.points[plane.start].getY(),v_temp.z + o.points[plane.start].getZ())
                        x = p.x + Const.xmax / 2.0
                        y = p.y + Const.zmax / 2.0
                        z = p.z + Const.zmax / 2.0
                        particle = Particle(x,y,z, Const.boundary_particle)
                        particle.setVelocity(plane.getNormal())
                        self.particles.append(particle)
        print "boundary particle %s" %str(len(self.particles) - before) 
    
    def __gen_liquid_p(self, o):
        i = o.points.lowest_point()
        xmin = o.points[i].getX()
        ymin = o.points[i].getY()
        zmin = o.points[i].getZ()
        adj_points = o.points[i].get_adj_points()
        start_num = len(self.particles)
        if len(adj_points) == 3:
            ort1 = o.points[adj_points[0]] - o.points[i]
            ort2 = o.points[adj_points[1]] - o.points[i]
            ort3 = o.points[adj_points[2]] - o.points[i]
            for x in self.__my_range(xmin, xmin + ort1.length() * (Const.TRANF_CONST) * Const.r0, Const.r0):
                for y in self.__my_range(ymin, ymin + ort2.length() * (Const.TRANF_CONST) * Const.r0, Const.r0):
                    for z in self.__my_range(zmin, zmin + ort3.length() * (Const.TRANF_CONST) * Const.r0, Const.r0):
                        particle = Particle(x + Const.xmax / 2.0,y + Const.ymax / 2.0,z + Const.xmax / 2.0,Const.liquid_particle)
                        self.particles.append(particle)
        print "generated liquid particles:%s"%(str(len(self.particles) - start_num)) 
        
    def __gen_elastic_p(self,o):
        i = o.points.lowest_point()
        self.plane0 = []
        self.plane1 = []
        self.plane2 = []
        self.plane3 = []
        self.plane4 = []
        self.plane5 = []
        xmin = o.points[i].getX()
        ymin = o.points[i].getY()
        zmin = o.points[i].getZ()
        adj_points = o.points[i].get_adj_points()
        lparticle = []
        _eparticles = []
        index_i = False
        index_j = False
        index_k = False
        l_particle=[]
        if len(adj_points) == 3:
            ort1 = o.points[adj_points[0]] - o.points[i]
            ort2 = o.points[adj_points[1]] - o.points[i]
            ort3 = o.points[adj_points[2]] - o.points[i]
            o1_l = ort1.length() * (Const.TRANF_CONST) * Const.r0
            o2_l = ort2.length() * (Const.TRANF_CONST) * Const.r0
            o3_l = ort3.length() * (Const.TRANF_CONST) * Const.r0
            self.period1 = 11#int(ort1.length() * (Const.TRANF_CONST)) 
            self.period2 = 11#int(ort2.length() * (Const.TRANF_CONST)) 
            self.period3 = 11#int(ort3.length() * (Const.TRANF_CONST)) 
            ort1.normalize()
            ort2.normalize()
            ort3.normalize()
            ort1 *= o1_l
            ort2 *= o2_l
            ort3 *= o3_l

            for step_x in self.__my_range(0, o1_l, Const.r0):
                alpha = step_x / o1_l
                if step_x == 0 or (step_x < o1_l and step_x + Const.r0 >= o1_l):
                    index_i = True
                else:
                    index_i = False
                for step_y in self.__my_range(0, o2_l, Const.r0):
                    beta = step_y / o2_l
                    if step_y == 0 or (step_y < o2_l and step_y + Const.r0 >= o2_l):
                        index_j = True
                    else:
                        index_j = False
                    for step_z in self.__my_range(0, o3_l, Const.r0):
                        gamma = step_z / o3_l
                        if step_z == 0 or (step_z < o3_l and step_z + Const.r0 >= o3_l):
                            index_k = True
                        else:
                            index_k = False
                        v_temp = (ort1 * alpha) + (ort2 * beta) + (ort3 * gamma) 
                        x = xmin + v_temp.x
                        y = ymin + v_temp.y
                        z = zmin + v_temp.z
                        particle = Particle(x + Const.xmax / 2.0, y + Const.zmax / 2.0, z + Const.zmax / 2.0,Const.elastic_particle)
                        if index_i or index_j or index_k: 
                            particle.face_p = True
                            if (index_i and index_j) or (index_j and index_k) or (index_i and index_k) :
                                particle.edge = True
                            _eparticles.append(particle)
                            if step_x == 0:
                                self.plane0.append(len(_eparticles) - 1)
                            if (step_x < o1_l and step_x + Const.r0 >= o1_l):
                                self.plane1.append(len(_eparticles) - 1)
                            if step_y == 0 : 
                                self.plane2.append(len(_eparticles) - 1)
                            if step_y < o2_l and step_y + Const.r0 >= o2_l:
                                self.plane3.append(len(_eparticles) - 1)
                            if step_z == 0: 
                                self.plane4.append(len(_eparticles) - 1)
                            if step_z < o3_l and step_z + Const.r0 >= o3_l:
                                self.plane5.append(len(_eparticles) - 1)
                            
                        else: 
                            particle.type = Const.elastic_particle
                            l_particle.append(particle)
                        #if particle.face_p:
                        
        print "elastic particle:%s"%(len(_eparticles))
        _eparticles.extend(l_particle)
        _eparticles.extend(self.particles)
        self.particles = _eparticles
        elasticParticles = [p for p in self.particles if p.type == Const.elastic_particle ]
        for p in elasticParticles:
            self.__genElasticConn(p, elasticParticles)
        m_particles = [p for p in _eparticles if p.face_p]
        self.__genMembranes(m_particles)
        
        print "generated elastic connections:%s"%(len(self.elasticConnections))
    def __gen_elastic_p_any_surface(self,o):
        '''
        On first step calculate normales for vertices 
        On second step calc normales for point which should locate on edges
        '''
        _eparticles = []
        before = len(self.particles)
        d = self.__getmindist(o.points)
        for p in o.points:
            x = d * p.getX() + Const.xmax / 2.0
            y = d * p.getY() + Const.ymax / 2.0
            z = d * p.getZ() + Const.xmax / 2.0
            particle = Particle(x,y,z, Const.elastic_particle)
            #particle.setVelocity(p.get_normal())
            _eparticles.append(particle)
        #second Step Create point for all eges
#         check_e = []
#         addition_p = 0
#         for plane in o.planes:
#             for e in plane.edges:
#                 if not (((str(e[0]) + '\t' + str(e[1])) in check_e) or ((str(e[1]) + '\t' + str(e[0])) in check_e)):
#                     v = (o.points[e[1]] - o.points[e[0]])#.get_in_real_c()
#                     l = (v.length() * float(Const.TRANF_CONST) * Const.r0)
#                     if l > Const.r0:
#                         v.normalize()
#                         v *= l
#                         for step in self.__my_range( Const.r0, l, Const.r0 ):
#                             v1 = v * (step / l)
#                             p = Point( v1.x + o.points[e[0]].getX(), v1.y + o.points[e[0]].getY(), v1.z + o.points[e[0]].getZ() )
#                             x = p.x + Const.xmax / 2.0#p.getX() 
#                             y = p.y + Const.ymax / 2.0#p.getY()
#                             z = p.z + Const.xmax / 2.0#p.getZ()
#                             particle = Particle(x,y,z, Const.elastic_particle)
#                             _eparticles.append(particle)
#                         addition_p+=1
#                     check_e.append(str(e[0]) + '\t' + str(e[1]))
#         print "elastic particles is %s"%str(len(self.particles) - before)
        
#         #third step create particles for all planes
#         if addition_p > 0:
#             for plane in o.planes:
#                 plane.calcBigArea(o.points)
#                 plane.getBigestEdges(o.points)
#                 e1 = plane.eX#plane.edges[0]
#                 e2 = plane.eY#plane.edges[len(plane.edges) - 1]
#                 if e1[0] == plane.start:
#                     v1 = o.points[e1[1]] - o.points[e1[0]]
#                 else:
#                     v1 = o.points[e1[0]] - o.points[e1[1]]
#                 if e2[0] == plane.start:
#                     v2 = o.points[e2[1]] - o.points[e2[0]]
#                 else:
#                     v2 = o.points[e2[0]] - o.points[e2[1]]
#                 l1 = (v1.length() * (Const.TRANF_CONST) * Const.r0)
#                 l2 = (v2.length() * (Const.TRANF_CONST) * Const.r0)
#                 v1_temp = v1.clone()
#                 v2_temp = v2.clone()
#                 v1.normalize()
#                 v2.normalize()
#                 v1 *= l1
#                 v2 *= l2
#                 for stepX in self.__my_range(Const.r0,l1,Const.r0):
#                     for stepY in self.__my_range(Const.r0,l2,Const.r0):
#                         alpha = ( stepX / l1 )
#                         beta = ( stepY / l2 )
#                         v_temp_1 = (v1_temp * alpha) + (v2_temp * beta)
#                         p_temp = Point(v_temp_1.x + o.points[plane.start].x,v_temp_1.y + o.points[plane.start].y,v_temp_1.z + o.points[plane.start].z)
#                         if plane.checkPoint(p_temp,o.points):
#                             v_temp = (v1 * alpha) + (v2 * beta)
#                             p = Point(v_temp.x + o.points[plane.start].getX(),v_temp.y + o.points[plane.start].getY(),v_temp.z + o.points[plane.start].getZ())
#                             x = p.x + Const.xmax / 2.0
#                             y = p.y + Const.ymax / 2.0
#                             z = p.z + Const.xmax / 2.0
#                             particle = Particle(x,y,z, Const.elastic_particle)
#                             _eparticles.append(particle)
        #print "elastic particle %s" %len(_eparticles) 
        _eparticles.extend(self.particles)
        self.particles = _eparticles
        elasticParticles = [p for p in self.particles if p.type == Const.elastic_particle ]
        self.__init_empty_connection(len(elasticParticles))
        for p in elasticParticles:
            self.__genElasticConn_1(o.points[elasticParticles.index(p)], elasticParticles,p)
#             self.__genElasticConn(p, elasticParticles)
        print len(self.elasticConnections)
    
    def __getmindist(self,points):
        d = -1
        f_i = True
        for p in points:
            for p1 in points:
                if ( ( (p-p1).length() < d) or f_i) and  p != p1:
                    f_i = False
                    d = (p-p1).length()
        if Const.r0 >  float(float(d) * float(Const.TRANF_CONST) * Const.r0):
            d1 = d * float(Const.TRANF_CONST) * Const.r0
            print "d = " + str(d1 * Const.simulationScale)
            print "r0=" + str(Const.r0 * Const.simulationScale)
            print "r0/d=" + str(float(Const.r0 * Const.simulationScale) / float(d1 * Const.simulationScale))
            print d * float(Const.TRANF_CONST) * Const.r0
            d = Const.r0 / float(d * float(Const.TRANF_CONST) * Const.r0)
            print "d = " + str(d)
        return d
    def __normilazing_net(self, o):
        if not o.elastic_box:
            raise Exception("It's not elastic object")
        checked_point = []
        for point in o.points:
            if point in checked_point:
                for a_point in point.get_adj_points():
                    dist = Vector3D.dist(point, a_point) 
                    if dist * Const.TRANF_CONST * Const.r0 < Const.r0:
                        pass
                        
    def __my_range(self, start, end, step):
        while start < end:
            yield start
            start += step
    def __init_empty_connection(self, elasticparticle_num=0):
        self.elasticConnections = ([ElasticConnection(Const.NO_PARTICEL_ID,0,0,0)] * (Const.MAX_NUM_OF_NEIGHBOUR *  elasticparticle_num) )
    def __genElasticConn_1(self, particle, elasticParticles, p_t):
        #elastic_connections_collection = []        
        #elastic_connections_collection.extend([ElasticConnection(Const.NO_PARTICEL_ID,0,0,0)] * (Const.MAX_NUM_OF_NEIGHBOUR ) )
        non_zero = 0
        p_index = elasticParticles.index(p_t)
        val1 = 1.1
        for face in particle.faces_l:
            for e in face.edges:
                if particle.index == e[0]:
                    p = elasticParticles[e[1]]
                    dist = Particle.distBetween_particles(p,p_t)
                    #dist = dist >= Const.r0 and dist or Const.r0
                    self.elasticConnections[p_index * Const.MAX_NUM_OF_NEIGHBOUR + non_zero] = ElasticConnection(e[1], dist, val1, 0 )
                    non_zero += 1
                elif particle.index == e[1]:
                    p = elasticParticles[e[0]]
                    dist = Particle.distBetween_particles(p,p_t)
                    #dist = dist >= Const.r0 and dist or Const.r0
                    self.elasticConnections[p_index * Const.MAX_NUM_OF_NEIGHBOUR + non_zero] = ElasticConnection(e[0], dist, val1, 0 )
                    non_zero += 1
    def __genElasticConn(self, particle, elasticParticles):
        '''
        Find elastc neighbour for particle
        extend elastic connections listS
        '''
        neighbour_collection = [p for p in elasticParticles if Particle.dot_particles(particle, p) <= Const.r0_squared * 2.7 and p != particle ]
        neighbour_collection.sort(key=lambda p: Particle.distBetween_particles(particle, p))
        if len(neighbour_collection) > Const.MAX_NUM_OF_NEIGHBOUR:
            neighbour_collection = neighbour_collection[0:Const.MAX_NUM_OF_NEIGHBOUR]
        elastic_connections_collection = []
        for p in neighbour_collection:
            val1 = 1.1
            elastic_connections_collection.append( ElasticConnection(self.particles.index(p),Particle.distBetween_particles(p,particle) * Const.simulationScale * 0.95, val1, 0) )
        '''
        If number of elastic connection less that MAX_NUM_OF_NEIGHBOUR then 
        we extend collection of elastic connection with non particle value
        '''
        particle.connections = [e_c.particle_j for e_c in elastic_connections_collection]
        if len(neighbour_collection) < Const.MAX_NUM_OF_NEIGHBOUR:
            elastic_connections_collection.extend([ElasticConnection(Const.NO_PARTICEL_ID,0,0,0)] * (Const.MAX_NUM_OF_NEIGHBOUR - len(neighbour_collection)) )
        self.elasticConnections.extend( elastic_connections_collection )
    
    def __fillPlane(self,plane):
        try:
            for i in range(self.period2):
                if i != self.period2 - 1:
                    for j in range(self.period3):
                        if j != self.period3 - 1:
                            id1 = i * self.period2 + j 
                            jd1 = id1 + 1 
                            kd1 = id1 + self.period2 
                            id2 = kd1
                            jd2 = kd1 + 1
                            kd2 = jd1
                            m1 = membrane( plane[id1], plane[jd1], plane[kd1] )
                            m2 = membrane( plane[id2], plane[jd2], plane[kd2] )
                            self.membranes.append(m1)
                            self.particles[plane[id1]].insertMem(len(self.membranes) - 1)
                            self.particles[plane[jd1]].insertMem(len(self.membranes) - 1)
                            self.particles[plane[kd1]].insertMem(len(self.membranes) - 1)
                            self.membranes.append(m2)
                            self.particles[plane[id2]].insertMem(len(self.membranes) - 1)
                            self.particles[plane[jd2]].insertMem(len(self.membranes) - 1)
                            self.particles[plane[kd2]].insertMem(len(self.membranes) - 1)
                            
        except IndexError as ex:
            print ex
    def __genMembranes(self,particles):
        #for p1 in range(self.period1):
        self.__fillPlane(self.plane0)
        self.__fillPlane(self.plane1)
        self.__fillPlane(self.plane2)
        self.__fillPlane(self.plane3)
        self.__fillPlane(self.plane4)
        self.__fillPlane(self.plane5)
        print "Membranes: " + str(len(self.membranes))

                     