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
Created on 14.08.2013

@author: Serg
'''
import math
from point import Vector3D
class TransformException(Exception):
    def __init__(self, message):
        self.message = message
class transformation(object):
    rotation = "rotation"
    scale = "scale"
    translation = "translation"
    @staticmethod
    def factory(**kwargs):
        try:
            if'name' in kwargs:
                name = kwargs['name']
                if name == transformation.rotation: 
                    return rotation(**kwargs)
                if name == transformation.translation:
                    return translation(**kwargs)
                if name == transformation.scale:
                    return scale(**kwargs)
                else: return None      
            else:
                raise TransformException('Could not create transform object because it has no name')
        except TransformException as ex:
            print ex.massage
            raise Exception('Could not create transform object')  
    def make_transform(self, vertices=None):
        pass
    
class rotation(transformation):
    def __init__(self, **kwargs):
        if 'property' in kwargs:
            property = kwargs['property'][0].split(' ')
            if len(property) == 4:
                x = float(property[0])
                y = float(property[1])
                z = float(property[2])
                angle = float(property[3])
                self.vector = Vector3D(x,y,z).unit()
                self.angle = angle
            else:
                raise TransformException('Too small number of input data it should contain vectro(x,y,z) and angle')
        else:
            raise TransformException('Transformation data about rotation is not available')
    def make_transform(self, vertices=None):
        for v in vertices:
            x = (math.cos(self.angle) + (1.0 - math.cos(self.angle)) * self.vector.x ** 2) * v.x + \
                  ((1.0 - math.cos(self.angle)) * self.vector.x * self.vector.y - math.sin(self.angle) * self.vector.z) * v.y + \
                  ((1.0 - math.cos(self.angle)) * self.vector.x * self.vector.z + math.sin(self.angle) * self.vector.y) * v.z
                   
            y = ((1.0 - math.cos(self.angle)) * self.vector.x * self.vector.y + math.sin(self.angle) * self.vector.z) * v.x + \
                  (math.cos(self.angle) + (1.0 - math.cos(self.angle)) * self.vector.y ** 2) * v.y + \
                  ((1.0 - math.cos(self.angle)) * self.vector.y * self.vector.z - math.sin(self.angle) * self.vector.x) * v.z
                  
            z = ((1.0 - math.cos(self.angle)) * self.vector.z * self.vector.x - math.sin(self.angle) * self.vector.y) * v.x + \
                  ((1.0 - math.cos(self.angle)) * self.vector.y * self.vector.z + math.sin(self.angle) * self.vector.x) * v.y + \
                  (math.cos(self.angle) + (1.0 - math.cos(self.angle)) * self.vector.z ** 2) * v.z
            v.x = x
            v.y = y
            v.z = z
            
class translation(transformation):
    def __init__(self, **kwargs):
        if 'property' in kwargs:
            property = kwargs['property'][0].split(' ')
            if len(property) == 3:
                x = float(property[0])
                y = float(property[1])
                z = float(property[2])
                self.vector = Vector3D(x,y,z)
            else:
                raise TransformException('Too small number of input data it should contain vectro(x,y,z)')
        else:
            raise TransformException('Transformation data about translation is not available')
    def make_transform(self, vertices=None):
        for v in vertices:
            v.x = v.x + self.vector.x
            v.y = v.y + self.vector.y
            v.z = v.z + self.vector.z
                        
class scale(transformation):
    def __init__(self, **kwargs):
        if 'property' in kwargs:
            property = kwargs['property'][0].split(' ')
            if len(property) == 3:
                x = float(property[0])
                y = float(property[1])
                z = float(property[2])
                self.vector = Vector3D(x,y,z)
            else:
                raise TransformException('Too small number of input data it should contain vectro(x,y,z)')
        else:
            raise TransformException('Transformation data about translation is not available')
        
    def make_transform(self, vertices=None):
        for v in vertices:
            v.x = v.x * self.vector.x
            v.y = v.y * self.vector.y
            v.z = v.z * self.vector.z