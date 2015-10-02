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
Created on 27.02.2013

@author: Serg
'''
import sys


class connection(object):
    def __init__(self, jd, rij0, val1=0.0, val2=0.0):
        self.jd = jd
        self.rij0 = rij0
        self.val1 = val1
        self.val2 = val2

    def __str__(self, *args, **kwargs):
        return '%s\t%s\t%s\t%s\n' % (self.jd, self.rij0, self.val1, self.val2)

    @staticmethod
    def get_empty():
        return connection(-1, -1, -1, -1)


ELASTIC_PARTICLE_COUNT = 7327
NEIGHBOUR_COUNT = 32
BOUNDARY_PARTICLE_COUNT = 33074

elasticConnectionData = [-1] * ELASTIC_PARTICLE_COUNT * NEIGHBOUR_COUNT * 4
next_empty_cell = [0] * ELASTIC_PARTICLE_COUNT

elasticConnnection = [[]] * ELASTIC_PARTICLE_COUNT


def fill():
    f = open('./source/elasticconnections.txt', 'r')
    currentid = 0
    firstiteration = True
    local_arr = []
    steps = 0
    for line in f:
        linearr = line.strip('\n').split('\t')
        id = int(float(linearr[0]))
        if id == 38074:
            # print str(steps)
            pass
        if firstiteration:
            currentid = id
            firstiteration = False
        if currentid == id:
            local_arr.append(connection(float(linearr[1]), float(linearr[2])))
        else:
            steps += 1
            elasticConnnection[currentid - BOUNDARY_PARTICLE_COUNT] = local_arr  # append(local_arr)
            local_arr = []
            currentid = id
            local_arr.append(connection(float(linearr[1]), float(linearr[2])))
    if local_arr:
        elasticConnnection[currentid - BOUNDARY_PARTICLE_COUNT] = local_arr
    f.close()


def extend():
    for l in elasticConnnection:
        if len(l) < NEIGHBOUR_COUNT:
            l.extend([connection.get_empty()] * (NEIGHBOUR_COUNT - len(l)))
            # elif len(l) > NEIGHBOUR_COUNT:
            #    print len(l)
            # sys.exit(0)


def put_to_file():
    f = open('./configurations/elasticconnections_1.txt', 'w')
    for l in elasticConnnection:
        for c in l:
            f.write(str(c))  # str(elasticConnnection.index(l)) + '\t' +
    f.close()


if __name__ == '__main__':
    # readFormFile()
    fill()
    extend()
    put_to_file()
    print "finish"
