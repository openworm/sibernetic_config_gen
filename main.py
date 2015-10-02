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

@author: Serg Khayrulin
@email: skhayrulin@openworm.org
'''
from generator.Generator import Generator
from generator.Const import Const
from XMLWriter.XMLWriter import XMLWriter


def make_config_file(g, filename="/configurations/v_test_liquid"):
    """
    Create configuration file and put information
    about particle position, velocity and elastic
    connections.
    TODO: create more check
    """
    output_f = open(filename, 'w')
    output_f.write(str(Const.xmin) + '\n')
    output_f.write(str(Const.xmax) + '\n')
    output_f.write(str(Const.ymin) + '\n')
    output_f.write(str(Const.ymax) + '\n')
    output_f.write(str(Const.zmin) + '\n')
    output_f.write(str(Const.zmax) + '\n')
    output_f.write("[position]\n")
    for p in g.particles:
        s_temp = "%s\t%s\t%s\t%s\n" % (p.position.x, p.position.y, p.position.z, p.type)
        output_f.write(s_temp)
    output_f.write("[velocity]\n")
    for p in g.particles:
        s_temp = "%s\t%s\t%s\t%s\n" % (p.velocity.x, p.velocity.y, p.velocity.z, p.velocity.val)
        output_f.write(s_temp)
    output_f.write("[connection]\n")
    for e_c in g.elasticConnections:
        s_temp = "%s\t%s\t%s\t%s\n" % (e_c.particle_j, e_c.r_ij, e_c.val1, e_c.val2)
        output_f.write(s_temp)
    output_f.write("[membranes]\n")
    output_f.write("[particleMemIndex]\n")
    output_f.write("[end]\n")
    output_f.close()
    print "Generation have Finished result in file %s" % (filename)


def create_xml_file(filename, generator):
    xml_writer = XMLWriter(filename)
    for p in generator.particles:
        xml_writer.add_particle(p)
    for c in generator.elasticConnections:
        xml_writer.add_connection(c)
    xml_writer.printtoFile()


if __name__ == '__main__':
    g = Generator('./3DModels/cube_incube.x3d')
    g.gen_configuration()
    make_config_file(g)
    #put_configto_file_temp(g, "./configurations/position_muscle.txt","./configurations/velocity_muscle.txt","./configurations/connection_muscle.txt")