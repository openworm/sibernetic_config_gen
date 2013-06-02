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
import math
from ElasticConnection import ElasticConnection

class Generator(object):
    '''
    Configuration Generator class: class generate configuration 
    for initial size of box
    '''
    def __init__(self, boxsizeX, boxsizeY, boxsizeZ, particle_count = 1024 * 16):
        '''
        Constructor
        It's important that sizes of box are multiple with r0 = h * 0.5
        Because it should be integer number of boundary particles 
        TODO: more detailed comment...
        '''
        self.p_count = particle_count
        Const.xmax = ( boxsizeX % Const.r0 == 0 ) and boxsizeX or ( int( boxsizeX / Const.r0 ) + 1 ) * Const.r0 # if boxsizeX divides on r0 without rest than XMAX = boxsizeX  
        Const.ymax = ( boxsizeY % Const.r0 == 0 ) and boxsizeY or ( int( boxsizeY / Const.r0 ) + 1 ) * Const.r0 # same
        Const.zmax = ( boxsizeZ % Const.r0 == 0 ) and boxsizeZ or ( int( boxsizeZ / Const.r0 ) + 1 ) * Const.r0 # same
        self.particles = []
        self.elasticConnections = []
    
    def genConfiguration(self):
        print "generating configuration"
        print "\tgenerating Boundary Particles"
        self.__generateBoundaryParticles()
        print "\tgenerating Elastic Particles"
        self.__generateElasticCube()
        print "\tgenerating Elastic Connections"
        elasticParticles = [p for p in self.particles if p.type == Const.elastic_particle ]
#        for e_p in elasticParticles:
#            self.__findNeighbour(e_p, elasticParticles)
#        print len(self.elasticConnections)
        print "\tgenerate Liquid Particles"
        self.__generateLiquidCube(self.p_count - len(elasticParticles)) 
        print "TotalNumber of particle is:%s"%(len(self.particles))
        print "Finish"
    def __generateLiquidCube(self, numOfCreatedParticles):
        '''
        This Method is generating cub of liquid
        coeff should be 0.2325 because need generate 
        volume of liquid with density 1000, this important for 
        modeling incompressible liquid.
        We generate liquid matter after elastic particles
        So liquid 
        TODO: generate more detailed Comment
        '''
        coeff = 0.2325
        x = Const.h *  coeff;
        y = Const.h *  coeff + Const.r0 * 10
        z = Const.h *  coeff + Const.r0 * 2
        i = 0
        while i < numOfCreatedParticles:
            particle = Particle(x,y,z,Const.liquid_particle)
            x += 2 * Const.h * coeff
            if x > Const.xmax / 3:
                x = Const.h * coeff + Const.r0 * 2
                z += 2 * coeff * Const.h
            if z > Const.zmax / 3:
                x = Const.h * coeff + Const.r0 * 2
                z = Const.h * coeff + Const.r0 * 2
                y += 2 * coeff * Const.h
            self.particles.append(particle)
            i += 1
    def __my_range(self, start, end, step):
        while start <= end:
            yield start
            start += step
    def __generateLiquidCube1(self, numOfCreatedParticles):
        '''
        This Method is generating cub of liquid
        coeff should be 0.2325 because need generate 
        volume of liquid with density 1000, this important for 
        modeling incompressible liquid.
        We generate liquid matter after elastic particles
        So liquid 
        TODO: generate more detailed Comment
        '''
        x = 15 * Const.r0 / 2
        y = 3 * Const.r0 / 2
        z = 3 * Const.r0 / 2 + (Const.zmax - Const.zmin)
        i = 0
        for x in self.__my_range(15 * Const.r0 / 2, (Const.xmax-Const.xmin)/5 + 3*Const.r0/2, Const.r0):
            for y in self.__my_range(3 * Const.r0 / 2, (Const.ymax-Const.ymin) - 3*Const.r0/2, Const.r0):
                for z in self.__my_range(3 * Const.r0 / 2 + (Const.zmax - Const.zmin), (Const.zmax-Const.zmin) * 7 / 10 - 3 * Const.r0 / 2, Const.r0):
                   particle = Particle(x,y,z,Const.liquid_particle)
                   self.particles.append(particle) 
    def __generateBoundaryParticles(self):
        '''
        Generate boundary particles: Boundary particles can locate 
        in three different places first it can be at box corner, 
        second at box edge and third at box face. We should take it into account 
        when calculating a velocity for boundary particle because a velocity should 
        have a length == 1 also vector vector of velocity should have direction ??
        TODO: generate better comment
        '''
        n = int( ( Const.xmax - Const.xmin ) / Const.r0 )  # Numbers of boundary particles on X-axis  
        m = int( ( Const.ymax - Const.ymin ) / Const.r0 )  # Numbers of boundary particles on Y-axis 
        k = int( ( Const.zmax - Const.zmin ) / Const.r0 )  # Numbers of boundary particles on Z-axis
        x = Const.xmin
        z = Const.zmin
        y = Const.ymin
        speed = 1.0
        normCorner = 1/math.sqrt(3.0)
        normBoundary = 1/math.sqrt(2.0)
        isBoundary = True
        y1 = Const.ymax
        i = 0
        '''
        In this loop we create simultaneously particles in all corners of box
        and on two faces Y = 0 and Y = ymax
        '''
        while i <= 2 * ( k * n + n + k ):
            particle1 = Particle( x , y , z, Const.boundary_particle)
            particle2 = Particle( x, y1, z, Const.boundary_particle)
            x += Const.r0
            if i == 0 :
                particle1.setVelocity( Float4(normCorner,normCorner,normCorner) )
                particle2.setVelocity( Float4(normCorner,-normCorner,normCorner) )
                isBoundary = True
            if x >= Const.xmax and z == Const.zmin and not isBoundary:
                particle1.setVelocity( Float4(-normCorner,normCorner,normCorner) )
                particle2.setVelocity( Float4(-normCorner,-normCorner,normCorner) )
                isBoundary = True
            if x >= Const.xmax and z >= Const.zmax - Const.r0 and not isBoundary:
                particle1.setVelocity( Float4(-normCorner,normCorner,-normCorner) )
                particle2.setVelocity( Float4(-normCorner,-normCorner,-normCorner) )
                isBoundary = True
            if x - Const.r0 == Const.xmin and z >= Const.zmax - Const.r0 and not isBoundary:
                particle1.setVelocity( Float4(normCorner,normCorner,-normCorner) )
                particle2.setVelocity( Float4(normCorner,-normCorner,-normCorner) )
                isBoundary = True
            if x >= Const.xmax and not isBoundary:
                particle1.setVelocity( Float4(-normBoundary,normBoundary,0.0) )
                particle2.setVelocity( Float4(-normBoundary,-normBoundary,0.0) )
                isBoundary = True
            if z == Const.zmin and not isBoundary:
                particle1.setVelocity( Float4(0.0, normBoundary, normBoundary) )
                particle2.setVelocity( Float4(0.0,-normBoundary,normBoundary) )
                isBoundary = True
            if x - Const.r0 == Const.xmin and not isBoundary:
                particle1.setVelocity( Float4(normBoundary,normBoundary, 0.0) )
                particle2.setVelocity( Float4(normBoundary,-normBoundary,0.0) )
                isBoundary = True
            if z >= Const.zmax - Const.r0 and not isBoundary:
                particle1.setVelocity( Float4(0.0,normBoundary,-normBoundary) )
                particle2.setVelocity( Float4(0.0,-normBoundary,-normBoundary) )
                isBoundary = True
            if isBoundary == False:
                particle1.setVelocity( Float4( 0.0, speed, 0.0) )
                particle2.setVelocity( Float4( 0.0,-speed, 0.0) )
            isBoundary = False
            if x > Const.xmax:
                x = Const.xmax
                z += Const.r0
            self.particles.append(particle1)
            self.particles.append(particle2)
            i += 2
        x = Const.xmin
        y = Const.ymin + Const.r0
        z = Const.zmin 
        x1 = Const.xmax
        isBoundary = False
        count = 2 *( k * ( m - 2 )  + k + m - 2) + i
        '''
        In this loop we generate boundary particle for faces X = XMIN and X = XMAX
        '''
        while i <= count:
            particle1 = Particle( x, y, z, Const.boundary_particle)
            particle2 = Particle( x1, y, z, Const.boundary_particle)
            if z == Const.zmin:
                particle1.setVelocity( Float4(normBoundary, 0.0, normBoundary) )
                particle2.setVelocity( Float4(-normBoundary,0.0,normBoundary) )
                isBoundary = True
            if z >= Const.zmax - Const.r0 and not isBoundary:
                particle1.setVelocity( Float4(normBoundary, 0.0, -normBoundary) )
                particle2.setVelocity( Float4(-normBoundary,0.0,-normBoundary) )
                isBoundary = True
            if isBoundary == False:
                particle1.setVelocity( Float4( speed, 0.0, 0.0) )
                particle2.setVelocity( Float4( -speed, 0.0, 0.0) )
            isBoundary = False
            y += Const.r0
            if y > Const.ymax - Const.r0:
                y = Const.ymin + Const.r0
                z += Const.r0
            self.particles.append(particle1)
            self.particles.append(particle2)
            i += 2
        x = Const.xmin + Const.r0;
        y = Const.ymin + Const.r0;
        z = Const.zmin;
        z1 = Const.zmax;
        count = 2 *( ( n - 2 ) * ( m - 2 )  + n + m - 4) + i;
        '''
        In this loop we generate boundary particle for faces Z = ZMIN and Z = ZMAX
        '''
        while i <= count:
            particle1 = Particle( x, y, z, Const.boundary_particle)
            particle2 = Particle( x, y, z1, Const.boundary_particle)
            particle1.setVelocity(Float4(0.0, 0.0, speed))
            particle2.setVelocity(Float4(0.0, 0.0, -speed))
            y += Const.r0
            if y > Const.ymax - Const.r0:
                y = Const.ymin + Const.r0
                x += Const.r0
            self.particles.append(particle1)
            self.particles.append(particle2)
            i+=2
        Const.BOUNDARY_PARTICLE_COUNT = i #???
        
    def __generateElasticWorm(self):
        '''
        In this function we generate elastic worm 
        '''
        coeff = 0.2325
        x = Const.xmax * 4.0 / 8.0 + Const.h * coeff
        y = Const.ymax * 2.0 / 9.0 + Const.h * coeff + Const.r0 * 10
        z = Const.zmax * 4.0 / 8.0 + Const.h * coeff
        segmentCount = 50
        alpha = 2.0 * math.pi / segmentCount
        wormBodyRadius = Const.h * coeff / math.sin( alpha/2 )
        j = -39
        while j <= 39 :
            segmentCount = int( math.sqrt( 40.0 * 40.0 - float( j * j ) ) )
            alpha = 2.0 * math.pi / segmentCount
            wormBodyRadius = Const.h * coeff / math.sin( alpha/2 )
            if wormBodyRadius >= 1.7 * Const.h *coeff:
                cylinderLayers = 1
                while cylinderLayers <= 9 :
                    pdist_coeff = 2.0
                    for i in range(segmentCount):
                        p_x = x + wormBodyRadius * math.sin(alpha * float(i))
                        p_y = y + wormBodyRadius * math.cos(alpha * float(i))
                        p_z = z + pdist_coeff * Const.h * coeff * float(j)
                        particle = Particle(p_x,p_y,p_z,Const.elastic_particle)
                        self.particles.append(particle)
                    if wormBodyRadius < 1.9 * 2.0 * Const.h * coeff:
                        break
                    segmentCount *= (wormBodyRadius - pdist_coeff * Const.h * coeff)
                    segmentCount /= (wormBodyRadius)
                    segmentCount = int(segmentCount)
                    wormBodyRadius -= pdist_coeff * Const.h * coeff
                    alpha = 2.0 * math.pi / segmentCount
                    cylinderLayers += 1
            j += 1 
    def __generateElasticCub(self):
        '''
        In this function we generate elastic worm 
        '''
        nx = (int)( ( Const.xmax - Const.xmin ) / Const.r0 ); #X
        ny = (int)( ( Const.ymax - Const.ymin ) / Const.r0 ); #Y
        nz = (int)( ( Const.zmax - Const.zmin ) / Const.r0 ); #Z
    
        nEx = 9;
        nEy = 5;
        nEz = 35;
        for x in range(nEx):
            for y in range(nEy):
                for z in range(nEz):
                    p_x = Const.xmax/2 + x * Const.r0 - nEx * Const.r0 / 2
                    p_y = Const.ymax/2 + y * Const.r0 - nEy * Const.r0 / 2 + Const.ymax * 3 / 8
                    p_z = Const.zmax/2 + z * Const.r0 - nEz * Const.r0 / 2;
                    particle = Particle(p_x,p_y,p_z,Const.elastic_particle)
                    particle.setVelocity(Float4(0.0,0.0,0.0,Const.elastic_particle))
                    
    def __findNeighbour(self, particle, elasticParticles):
        '''
        Find elastc neighbour for particle
        extend elastic connections list
        '''
        neighbour_collection = [p for p in elasticParticles if Particle.dot_particles(particle, p) < Const.r0_squared * 3.05 and p != particle ]
        neighbour_collection.sort(key=lambda p: Particle.distBetween_particles(particle, p))
        if len(neighbour_collection) > Const.MAX_NUM_OF_NEIGHBOUR:
            neighbour_collection = neighbour_collection[0:Const.MAX_NUM_OF_NEIGHBOUR]
        elastic_connections_collection = [ElasticConnection(self.particles.index(particle),self.particles.index(p),Particle.distBetween_particles(p,particle)) for p in neighbour_collection]
        self.elasticConnections.extend( elastic_connections_collection )
    