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
@contact: s.khayrulin@gmail.com
'''
from xml.dom import minidom
from generator.Const import Const
from generator.helper.plane import Plane
from generator.helper.point import Point, Vector3D
from generator.helper.collections import Vertices, Planes
from generator.helper.transformation import transformation
#from generator.Generator import obj
import generator
def read_model(file_name, objects):
    model_doc = minidom.parse(file_name)
    '''
    TODO: add check 
    '''
    for element in model_doc.getElementsByTagName('Transform'):
        o = generator.Generator.obj()
        ok = False
        if element.attributes['DEF'].value == 'cube_world_TRANSFORM':
            o.type = generator.Generator.obj.boundary_box
            ok = True
        if element.attributes['DEF'].value == 'cube_liquid_TRANSFORM':
            o.type = generator.Generator.obj.liquid_box
            ok = True
        if element.attributes['DEF'].value == 'cube_elastic_TRANSFORM':
            o.type = generator.Generator.obj.elastic_box
            ok = True
        if ok:
            faces_list = element.getElementsByTagName('IndexedFaceSet')[0].attributes['coordIndex'].value
            
            faces_list = prepare_v_list(faces_list).strip(' ')
            
            faces_list = faces_list.split('-1')
            
            faces_list = [face_s.split(' ') for face_s in faces_list if face_s != ' ' and face_s != '']
            o.planes.extend(Planes([Plane(face) for face in faces_list]))
            v_c = element.getElementsByTagName('IndexedFaceSet')[0].getElementsByTagName('Coordinate')[0].attributes['point'].value
            v_c = v_c.split(' ')
            p_s = []
            for i in range(0,len(v_c) - 1, 3):
                p = Point(v_c[i],v_c[i+1],v_c[i+2],int((i)/3),o.planes, 0)
                if(int((i)/3) < 0):
                    print "ddd"
                p_s.append(p)
            v = Vertices(p_s)
            o.points.extend(v)
            #o.points.pop(0)
            for atr in element.attributes.items():
                t = transformation.factory(name = atr[0], property = atr[1:])
                if t != None: 
                    o.transforms.extend([t])
            objects.extend([o])
    print "Read %s object from file"%len(objects)

def prepare_v_list(v_list):
    '''
    Vertices list can start not from 0 but and from 1
    we should correctly work with it
    '''
    _v_list = v_list.split(' ')
    zero_v = int(_v_list[0])
    for v in _v_list:
        if v != '-1' and v != '':
            v = int(v)
            if v < zero_v:
                zero_v = v
    result_str = ''
    if zero_v != 0:
        for v in _v_list:
            if v != '-1' and v != '':
                v = int(v)
                result_str += str(v - zero_v) + ' '
            else:
                result_str += v + ' '
    else:
        result_str = v_list
    return result_str
        