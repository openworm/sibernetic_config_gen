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
Created on 20.06.2013

@author: Serg
'''
from xml.dom.minidom import Document
from generator.Const import Const
class XMLWriter(object):
    '''
    classdocs
    '''

    def __init__(self, doc_name=''):
        '''
        Constructor
        '''
        self.docname = doc_name
        self.out_doc = Document()
        self.out_doc.version = "1.0"
        self.out_doc.doctype = "xml"
        self.out_doc.standalone = "yes"
        self.sph_element = self.out_doc.createElement('SPHModel')
        self.sph_element.setAttribute('zMin',str(Const.zmin))
        self.sph_element.setAttribute('zMax',str(Const.zmax))
        self.sph_element.setAttribute('xMin',str(Const.xmin))
        self.sph_element.setAttribute('xMax',str(Const.xmax))
        self.sph_element.setAttribute('yMin',str(Const.ymin))
        self.sph_element.setAttribute('yMax',str(Const.ymax))
        self.sph_element.setAttribute('xmlns',"http://www.example.org/SPHSchema")
        self.out_doc.appendChild(self.sph_element)
        
    def add_particle(self, particle):
        particle_ellement = self.out_doc.createElement('particles')
        particle_ellement.setAttribute('mass', str(Const.mass))
        p_pos_ellement = self.out_doc.createElement('positionVector')
        p_pos_ellement.setAttribute('p', str(particle.type))
        p_pos_ellement.setAttribute('z', str(particle.position.z))
        p_pos_ellement.setAttribute('y', str(particle.position.y))
        p_pos_ellement.setAttribute('x', str(particle.position.x))
        p_vel_ellement = self.out_doc.createElement('velocityVector')
        p_vel_ellement.setAttribute('p', str(particle.type))
        p_vel_ellement.setAttribute('z', str(particle.velocity.z))
        p_vel_ellement.setAttribute('y', str(particle.velocity.y))
        p_vel_ellement.setAttribute('x', str(particle.velocity.x))
        particle_ellement.appendChild(p_pos_ellement)
        particle_ellement.appendChild(p_vel_ellement)
        self.sph_element.appendChild(particle_ellement)
        del particle_ellement
        
    def add_connection(self, connection):
        connection_ellement = self.out_doc.createElement('connections')
        jd_ellement = self.out_doc.createElement('p1')
        ptext = self.out_doc.createTextNode(str(connection.particle_j))
        jd_ellement.appendChild(ptext)
        distance_ellemtn = self.out_doc.createElement('distance')
        ptext = self.out_doc.createTextNode(str(connection.r_ij))
        distance_ellemtn.appendChild(ptext)
        val1_ellemnt = self.out_doc.createElement('mysteryValue')
        ptext = self.out_doc.createTextNode(str(connection.val1))
        val1_ellemnt.appendChild(ptext)
        connection_ellement.appendChild(jd_ellement)
        connection_ellement.appendChild(distance_ellemtn)
        connection_ellement.appendChild(val1_ellemnt)
        self.sph_element.appendChild(connection_ellement)
        
    def add_membrane(self, membrane):
        membrane_ellement = self.out_doc.createElement('membranes')
        particle_i_ellement = self.out_doc.createElement('particle_i')
        ptext = self.out_doc.createTextNode(str(membrane.id))
        particle_i_ellement.appendChild(ptext)
        particle_j_ellement = self.out_doc.createElement('particle_j')
        ptext = self.out_doc.createTextNode(str(membrane.jd))
        particle_j_ellement.appendChild(ptext)
        particle_k_ellement = self.out_doc.createElement('particle_k')
        ptext = self.out_doc.createTextNode(str(membrane.kd))
        particle_k_ellement.appendChild(ptext)  
        membrane_ellement.appendChild(particle_i_ellement)
        membrane_ellement.appendChild(particle_j_ellement)
        membrane_ellement.appendChild(particle_k_ellement)
        self.sph_element.appendChild(membrane_ellement)
        
    def add_membraneIndex(self, index):
        particleMembranesList = self.out_doc.createElement('particleMembranesList')  
        ptext = self.out_doc.createTextNode(str(index))
        particleMembranesList.appendChild(ptext)
        self.sph_element.appendChild(particleMembranesList)
        
    def printtoFile(self):
        try:
            f = open('./configurations/geppetto/' + self.docname + '.xml', 'w')
            f.write(self.out_doc.toprettyxml(encoding='utf-8'))
            f.close()
            print 'Configuration was save in file % s in flder configuration', self.docname + '.xml'
        except IOError as ex:
            print 'Configuration  wasn''t saved because : %s' % ex.strerror