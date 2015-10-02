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

@author: Sergey Khayrulin
'''
from point import Vector3D

eps = 0.000000001


class PlaneException(Exception):
    def __init__(self, message):
        self.message = message


class Plane(object):
    """
    classdocs
    """
    def __init__(self, vertices=[], points=None):
        if len(vertices) < 3:
            raise PlaneException('Plane could not contain less than 3 vertices. Check your configuration file.')
        self.vertices = [int(v) for v in vertices if v != '']
        '''
        List of all edges for current plane
        '''
        self.edges = []
        for i in range(len(self.vertices)):
            j = (i + 1) <= len(self.vertices) - 1 and i + 1 or 0
            item = [self.vertices[i], self.vertices[j]]
            self.edges.append(item)

    def calc_area(self, points):
        if len(self.vertices) == 4:
            self.area = self.__get_area(points[self.edges[0][1]] - points[self.edges[0][0]],
                             points[self.edges[-1][1]] - points[self.edges[-1][0]])
            self.area += self.__get_area(points[self.edges[1][1]] - points[self.edges[1][0]],
                             points[self.edges[2][1]] - points[self.edges[2][0]])
        else:
            self.area = self.__get_area(points[self.edges[0][1]] - points[self.edges[0][0]],
                             points[self.edges[-1][1]] - points[self.edges[-1][0]])

    def __get_area(self, a, b):
        ab = Vector3D.cross_prod(a, b)
        return ab.length() / 2.0

    @property
    def get_normal(self):
        return self.normal

    def set_normal(self, points):
        """
        Calculating of normal vector to current plane
        :param points:
        """
        a = points[self.vertices[1]] - points[self.vertices[0]]
        b = points[self.vertices[-1]] - points[self.vertices[0]]
        self.normal = Vector3D.cross_prod(a, b)
        self.normal.normalize()

    def check_point(self, p, points):
        """
        Checking point it is on a current plain
        :param p: point with coordinates
        :param points: collection of all points
        :return: True or False
        """
        b_s = 0
        for e in self.edges:
            a = Vector3D(points[e[0]].x - p.x, points[e[0]].y - p.y, points[e[0]].z - p.z)
            b = Vector3D(points[e[1]].x - p.x, points[e[1]].y - p.y, points[e[1]].z - p.z)
            b_s += self.__get_area(a, b)
        # return True
        if abs(b_s - self.area) <= eps:
            return True
        return False

    def __get_edges_for_point(self, point):
        """
        Get collection of edges for specific point
        :param point: point
        :return: collection of edges which contains this point
        """
        ed = []
        for e in self.edges:
            if e[0] == point.index or e[1] == point.index:
                ed.append(e)
        return ed

    def getBigestEdges(self, points):
        bigestLen = 0
        for p in points:
            ed = self.__get_edges_for_point(p)
            if len(ed) == 2:
                v1 = points[ed[0][1]] - points[ed[0][0]]
                v2 = points[ed[1][1]] - points[ed[1][0]]
                temp_len = v1.length() + v2.length()
                if temp_len > bigestLen:
                    self.eX = ed[0]
                    self.eY = ed[1]
                    self.start = p.index
                    bigestLen = temp_len
