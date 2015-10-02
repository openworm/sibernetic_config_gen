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
Created on Jul 29, 2013

@author: serg
'''
import math
from generator.Const import Const


class Vector3D(object):
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __sub__(self, p1):
        return Point(self.x - p1.x, self.y - p1.y, self.z - p1.z)

    def __add__(self, p1):
        x = self.x + p1.x
        y = self.y + p1.y
        z = self.z + p1.z
        return Vector3D(x, y, z)

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def length(self):
        l = self.x ** 2 + self.y ** 2 + self.z ** 2
        return math.sqrt(l)

    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y*scalar, self.z*scalar)

    def __call__(self):
        return self

    def clone(self):
        return Vector3D(self.x, self.y, self.z)

    @staticmethod
    def dot_prod(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def cross_prod(a, b):
        """
        As I understood we're using left side system of coordinates
        """
        return Vector3D(a.z * b.y - a.y * b.z, a.x * b.z - a.z * b.x, a.y * b.x - a.x * b.y)

    def normalize(self):
        l = self.__len__()
        if l != 0:
            self.x /= l
            self.y /= l
            self.z /= l
        else:
            raise ZeroDivisionError('Length of vector is equal to zero')

    def unit(self):
        l = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        return Vector3D(self.x / l, self.y / l, self.z / l)

    @staticmethod
    def rotate_v1_around_v2(v1, v2, angle):
        angle *= float(math.pi / 180.0)
        ort1 = v2.unit()
        ort2 = (Vector3D.cross_prod(v2, v1)).unit()
        ort3 = (Vector3D.cross_prod(ort1, ort2)).unit()
        return ort1 * (Vector3D.dot_prod(v1, ort1)) + (ort2 * (Vector3D.dot_prod(v1, ort3))) * math.sin(angle) + (ort3*(Vector3D.dot_prod(v1, ort3))) * math.cos(angle)


class Point(Vector3D):
    """
    classdocs
    """
    def __init__(self, x, y, z, index=-1, planes=None, step=0):
        Vector3D.__init__(self, x, y, z)
        self.index = int(index) - step
        if planes is not None:
            self.faces = filter(lambda p: self.index in p.vertices, planes)

    def get_x(self):
        return self.x * Const.TRANF_CONST * Const.r0

    def get_y(self):
        return self.y * Const.TRANF_CONST * Const.r0

    def get_z(self):
        return self.z * Const.TRANF_CONST * Const.r0

    @property
    def get_normal(self):
        self.n = self.faces[0].get_normal()
        if len(self.faces) > 1:
            for f in self.faces[1:]:
                self.n = self.n + f.get_normal()
        self.n.normalize()
        return self.n

    def get_adj_points(self):
        adj_points = []
        for f in self.faces:
            for e in f.edges:
                if self.index in e:
                    i = (e[0] == self.index) and e[1] or e[0]
                    if not(i in adj_points) and i != self.index:adj_points.append(i)
        return adj_points

    @staticmethod
    def find_common_plane(p1, p2):
        common_faces = []
        for p in p1.faces:
            if p in p2.faces:
                common_faces.append(p)
        return common_faces

