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
        Const.xmax = boxsizeX#( boxsizeX % Const.r0 == 0 ) and boxsizeX or ( int( boxsizeX / Const.r0 ) + 1 ) * Const.r0 # if boxsizeX divides on r0 without rest than XMAX = boxsizeX  
        Const.ymax = boxsizeY#( boxsizeY % Const.r0 == 0 ) and boxsizeY or ( int( boxsizeY / Const.r0 ) + 1 ) * Const.r0 # same
        Const.zmax = boxsizeZ#( boxsizeZ % Const.r0 == 0 ) and boxsizeZ or ( int( boxsizeZ / Const.r0 ) + 1 ) * Const.r0 # same
        self.particles = []
        self.elasticConnections = []
        self.nMuscles = 5;
    
    def genConfiguration(self):
        print "generating configuration"
        print "\tgenerating Elastic Particles"
        i = 0
        self.__generateNMuscle()
        i = len(self.particles) - i
        i_e = len(self.particles)
        print "\t elastic particle = %s"%(i)
        print "\tgenerated"
        print "\tgenerated"
        print "\tgenerate Liquid Particles"
        self.__generateLiquidCube()
        i = len(self.particles) - i
        print "\t liquid particle = %s"%(i)
        print "\tgenerated"
        print "\tgenerating Elastic Connections"
#        elasticParticles = [p for p in self.particles if p.type == Const.elastic_particle ]
#        for e_p in elasticParticles:
#            self.__genElasticConn(e_p, elasticParticles)
        print len(self.elasticConnections)
        print "\tgenerating Boundary Particles"        
        self.__generateBoundaryParticles()
        i = len(self.particles) - i - i_e
        print "\t boundary particle = %s"%(i)
        print "\tgenerated"
        print "TotalNumber of particle is:%s"%(len(self.particles))
        print "Finish"
    def __generateLiquidCube(self):
        '''
        This Method is generating cub of liquid
        coeff should be 0.2325 because need generate 
        volume of liquid with density 1000, this important for 
        modeling incompressible liquid.
        We generate liquid matter after elastic particles
        So liquid 
        TODO: generate more detailed Comment
        '''
        for x in self.__my_range(Const.r0*23.0, (Const.xmax - Const.xmin) - Const.r0 * 23.0, Const.r0):
            for y in self.__my_range(Const.r0*3.0, (Const.ymax - Const.ymin) * 0.0 + 9.0 * Const.r0, Const.r0):
                for z in self.__my_range(Const.r0*23.0, (Const.zmax - Const.zmin) - 23.0 * Const.r0, Const.r0):
                    particle = Particle(x,y,z,Const.liquid_particle)
                    self.particles.append(particle)
                    
    def __my_range(self, start, end, step):
        while start < end:
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
        nx = int( ( Const.xmax - Const.xmin ) / Const.r0 )  # Numbers of boundary particles on X-axis  
        ny = int( ( Const.ymax - Const.ymin ) / Const.r0 )  # Numbers of boundary particles on Y-axis 
        nz = int( ( Const.zmax - Const.zmin ) / Const.r0 )  # Numbers of boundary particles on Z-axis
        # 1 - top and bottom 
        for ix in range(nx):
            for iy in range(ny):
                if ( ( ix == 0 ) or ( ix == nx - 1) ) or ( (iy == 0) or (iy == ny - 1 ) ) :
                    if ( ( ix == 0 ) or ( ix == nx - 1 ) ) and ( ( iy == 0 ) or ( iy == ny - 1 ) ): #corners
                        x = ix * Const.r0 + Const.r0 / 2.0
                        y = iy * Const.r0 + Const.r0 / 2.0
                        z = 0.0 * Const.r0 + Const.r0 / 2.0
                        vel_x = ( 1.0 * float( ix == 0 ) - 1.0 * float( ix == nx - 1 ) ) / math.sqrt( 3.0 )
                        vel_y = ( 1.0 * float( iy == 0 ) - 1.0 * float( iy == ny - 1 ) ) / math.sqrt( 3.0 )
                        vel_z = 1.0 / math.sqrt( 3.0 )
                        particle1 = Particle(x,y,z, Const.boundary_particle)
                        particle1.setVelocity(Float4(vel_x, vel_y, vel_z))
                        x = ix * Const.r0 + Const.r0 / 2.0
                        y = iy * Const.r0 + Const.r0 / 2.0
                        z = (nz - 1.0) * Const.r0 + Const.r0 / 2.0
                        vel_x = ( 1.0 * float( ix == 0 ) - 1.0 * float( ix == nx - 1 ) ) / math.sqrt( 3.0 )
                        vel_y = ( 1.0 * float( iy == 0 ) - 1.0 * float( iy == ny - 1 ) ) / math.sqrt( 3.0 )
                        vel_z = -1.0 / math.sqrt( 3.0 )
                        particle2 = Particle(x,y,z, Const.boundary_particle)
                        particle2.setVelocity(Float4(vel_x, vel_y, vel_z))
                        self.particles.append(particle1)
                        self.particles.append(particle2)
                    else: #edges
                        x = ix * Const.r0 + Const.r0 / 2.0
                        y = iy * Const.r0 + Const.r0 / 2.0
                        z = 0.0 * Const.r0 + Const.r0 / 2.0
                        vel_x = ( 1.0 * ( float( ix == 0 ) - float( ix == nx - 1 ) ) ) / math.sqrt( 2.0 )
                        vel_y = ( 1.0 * ( float( iy == 0 ) - float( iy == ny - 1 ) ) ) / math.sqrt( 2.0 )
                        vel_z = 1.0 / math.sqrt( 2.0 )
                        particle1 = Particle(x,y,z, Const.boundary_particle)
                        particle1.setVelocity(Float4(vel_x, vel_y, vel_z))
                        x = ix * Const.r0 + Const.r0 / 2.0
                        y = iy * Const.r0 + Const.r0 / 2.0
                        z = (nz - 1.0) * Const.r0 + Const.r0 / 2.0
                        vel_x = ( 1.0 * ( float( ix == 0 ) - float( ix == nx - 1 ) ) ) / math.sqrt( 2.0 )
                        vel_y = ( 1.0 * ( float( iy == 0 ) - float( iy == ny - 1 ) ) ) / math.sqrt( 2.0 )
                        vel_z = -1.0 / math.sqrt( 2.0 )
                        particle2 = Particle(x,y,z, Const.boundary_particle)
                        particle2.setVelocity(Float4(vel_x, vel_y, vel_z))
                        self.particles.append(particle1)
                        self.particles.append(particle2)
                else: #planes
                    x = ix * Const.r0 + Const.r0 / 2.0
                    y = iy * Const.r0 + Const.r0 / 2.0
                    z = 0.0 * Const.r0 + Const.r0 / 2.0
                    vel_x = 0.0
                    vel_y = 0.0
                    vel_z = 1.0
                    particle1 = Particle(x,y,z, Const.boundary_particle)
                    particle1.setVelocity(Float4(vel_x, vel_y, vel_z))
                    x = ix * Const.r0 + Const.r0 / 2.0
                    y = iy * Const.r0 + Const.r0 / 2.0
                    z = (nz - 1.0) * Const.r0 + Const.r0 / 2.0
                    vel_x = 0.0
                    vel_y = 0.0
                    vel_z = -1.0
                    particle2 = Particle(x,y,z, Const.boundary_particle)
                    particle2.setVelocity(Float4(vel_x, vel_y, vel_z))
                    self.particles.append(particle1)
                    self.particles.append(particle2)
        #2 - side walls OX-OZ and opposite
        for ix in range(nx):
            for iz in range(1,nz - 1):
                if (ix == 0) or (ix == nx - 1):
                    x = ix * Const.r0 + Const.r0 / 2.0
                    y = 0.0 * Const.r0 + Const.r0 / 2.0
                    z = iz * Const.r0 + Const.r0 / 2.0
                    vel_x = 0.0
                    vel_y = 1.0 / math.sqrt(2.0)
                    vel_z = 1.0 * ( float( iz == 0 ) - float(iz == nz - 1 ) ) / math.sqrt(2.0)
                    particle1 = Particle(x,y,z, Const.boundary_particle)
                    particle1.setVelocity(Float4(vel_x, vel_y, vel_z))
                    x = ix * Const.r0 + Const.r0 / 2.0
                    y = ( ny - 1 ) * Const.r0 + Const.r0 / 2.0
                    z = iz * Const.r0 + Const.r0 / 2.0
                    vel_x = 0.0
                    vel_y = -1.0 / math.sqrt(2.0)
                    vel_z = 1.0 * (float(iz == 0) - float(iz == nz - 1)) / math.sqrt(2.0)
                    particle2 = Particle(x,y,z, Const.boundary_particle)
                    particle2.setVelocity(Float4(vel_x, vel_y, vel_z))
                    self.particles.append(particle1)
                    self.particles.append(particle2)
                else:
                    x = ix * Const.r0 + Const.r0 / 2.0
                    y = 0.0 * Const.r0 + Const.r0 / 2.0
                    z = iz * Const.r0 + Const.r0 / 2.0
                    vel_x = 0.0
                    vel_y = 1.0
                    vel_z = 0.0
                    particle1 = Particle(x,y,z, Const.boundary_particle)
                    particle1.setVelocity(Float4(vel_x, vel_y, vel_z))
                    x = ix * Const.r0 + Const.r0 / 2.0
                    y = ( ny - 1 ) * Const.r0 + Const.r0 / 2.0
                    z = iz * Const.r0 + Const.r0 / 2.0
                    vel_x = 0.0
                    vel_y = -1.0
                    vel_z = 0.0 
                    particle2 = Particle(x,y,z, Const.boundary_particle)
                    particle2.setVelocity(Float4(vel_x, vel_y, vel_z))
                    self.particles.append(particle1)
                    self.particles.append(particle2)
            #3 - side walls OY-OZ and opposite
        for iy in range(1,ny - 1):
            for iz in range(1,nz - 1):
                x = 0.0 * Const.r0 + Const.r0 / 2.0
                y = iy * Const.r0 + Const.r0 / 2.0
                z = iz * Const.r0 + Const.r0 / 2.0
                vel_x = 1.0
                vel_y = 0.0
                vel_z = 0.0
                particle1 = Particle(x,y,z, Const.boundary_particle)
                particle1.setVelocity(Float4(vel_x, vel_y, vel_z))
                x = (nx - 1) * Const.r0 + Const.r0 / 2.0
                y = iy * Const.r0 + Const.r0 / 2.0
                z = iz * Const.r0 + Const.r0 / 2.0
                vel_x = -1.0
                vel_y = 0.0
                vel_z = 0.0 
                particle2 = Particle(x,y,z, Const.boundary_particle)
                particle2.setVelocity(Float4(vel_x, vel_y, vel_z))
                self.particles.append(particle1)
                self.particles.append(particle2)


     
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
    
    def __generateNMuscle(self):
        '''
        Generate nMuscles connected muscle
        '''
        nEx = 7
        nEy = 4
        nEz = 25
        for nM in range(self.nMuscles):
            for x in range(nEx):
                for y in range(nEy):
                    for z in range(nEz):
                        p_x = Const.xmax / 2.0 + float(x) * Const.r0 - nEx * Const.r0 / 2.0 - Const.r0 * (nEx)/2.0 + Const.r0*(nEx+0.4)*float(nM>2)
                        p_y = Const.ymax / 2.0 + y * Const.r0 - nEy * Const.r0 / 2.0
                        p_z = Const.zmax / 2.0 + z * Const.r0 - nEz * Const.r0 / 2.0  - (nM<=2)*(nM-1)*(nEz*Const.r0) - float(nM>2)*(Const.r0/2+(nM-4)*Const.r0)*nEz - (nM==1)*Const.r0/2.5 - (nM==2)*Const.r0*2/2.5 + (nM==4)*Const.r0/2.5;
                        particle = Particle(p_x,p_y,p_z,Const.elastic_particle)
                        particle.setVelocity(Float4(0.0,0.0,0.0,Const.elastic_particle))
                        self.particles.append(particle)

    def __genElasticConn(self, particle, elasticParticles):
        '''
        Find elastc neighbour for particle
        extend elastic connections list
        '''
        nMi = elasticParticles.index(particle)*self.nMuscles/len(elasticParticles);
        neighbour_collection = [p for p in elasticParticles if Particle.dot_particles(particle, p) < Const.r0_squared * 3.05 and p != particle ]
        neighbour_collection.sort(key=lambda p: Particle.distBetween_particles(particle, p))
        if len(neighbour_collection) > Const.MAX_NUM_OF_NEIGHBOUR:
            neighbour_collection = neighbour_collection[0:Const.MAX_NUM_OF_NEIGHBOUR]
        elastic_connections_collection = []
        for p in neighbour_collection:
            nMj = elasticParticles.index(particle) * self.nMuscles / len(elasticParticles)
            val1 = 0
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
    
