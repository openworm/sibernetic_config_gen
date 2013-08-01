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
from generator.helper.point import Point
from generator.helper.collections import Vertices, Planes

def read_model(file_name, points = [], planes = []):
    model_doc = minidom.parse(file_name)
    '''
    TODO: add check 
    '''
    faces_list = model_doc.getElementsByTagName('IndexedFaceSet')[0].attributes['coordIndex'].value
    faces_list = faces_list.split('-1')
    faces_list = [face_s.split(' ') for face_s in faces_list if face_s != ' ']
    planes.extend(Planes([Plane(face) for face in faces_list]))
    v_c = model_doc.getElementsByTagName('IndexedFaceSet')[0].getElementsByTagName('Coordinate')[0].attributes['point'].value
    v_c = v_c.split(' ')
    points.extend(Vertices([Point(v_c[i],v_c[i+1],v_c[i+2],int(i/3),planes) for i in range(0,len(v_c) - 1,3)]))
    