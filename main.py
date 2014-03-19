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

@author: Serg
'''
from generator.Generator import Generator
from generator.Const import Const
from XMLWriter.XMLWriter import XMLWriter
from XMLWriter import colladawriter
import sys
import utils

def put_configto_file(generator, filename="./configurations/configuration.txt"):
	'''
	Create configuration file and put information
	about particle position, velocity and elastic 
	connections.
	TODO: create more check 
	'''
	output_f = open(filename,"w")
	output_f.write("Position\n")
	for  p in generator.particles:
		s_temp = "%s\t%s\t%s\t%s\n"%(p.position.x,p.position.y,p.position.z,p.type)
		output_f.write(s_temp)
	output_f.write("Velocity\n")
	for  p in generator.particles:
		s_temp = "%s\t%s\t%s\t%s\n"%(p.velocity.x,p.velocity.y,p.velocity.z,p.velocity.val)
		output_f.write(s_temp)
	output_f.write("ElasticConnection\n")
	output_f.write(str(len(generator.elasticConnections)) + '\n')
	for  e_c in generator.elasticConnections:
		s_temp = "%s\t%s\t%s\t%s\n"%(e_c.particle_j,e_c.r_ij, e_c.val1, e_c.val2)
		output_f.write(s_temp)
	output_f.close()
	print "Generation have Finished result in file %s"%(filename)
def put_configto_file_temp(generator, pos_file="./configurations/position.txt",vel_file="./configurations/velocity.txt", con_file="./configurations/connection.txt", mem_file="./configurations/membranes.txt", mem_index_file="./configurations/particleMembraneIndex.txt"):
	'''
	Create configuration file and put information
	about particle position, velocity and elastic 
	connections.
	TODO: create more check 
	'''
	output_f_p = open(pos_file,"w")
	for  p in generator.particles:
		s_temp = "%s\t%s\t%s\t%s\n"%(p.position.x,p.position.y,p.position.z,p.type)
		output_f_p.write(s_temp)
	output_f_v = open(vel_file,"w")
	for  p in generator.particles:
		s_temp = "%s\t%s\t%s\t%s\n"%(p.velocity.x,p.velocity.y,p.velocity.z,p.velocity.val)
		output_f_v.write(s_temp)
	output_f_v.close()
	output_f_conn = open(con_file, "w")
	#output_f_conn.write(str(len(generator.elasticConnections)) + '\n')
	for  e_c in generator.elasticConnections:
		s_temp = "%s\t%s\t%s\t%s\n"%(e_c.particle_j,e_c.r_ij, e_c.val1, e_c.val2)
		output_f_conn.write(s_temp)
	output_f_conn.close()
	output_f_m = open(mem_file, "w")
	for  m in generator.membranes:
		s_temp = "%s\t%s\t%s\n"%(m.id,m.jd, m.kd)
		output_f_m.write(s_temp)
	output_f_m.close()
	output_f_mi = open(mem_index_file, "w")
	i=0
	for  p in generator.particles:
		if p.type == Const.elastic_particle:
			for m_i in p.membranesIndex:
				s_temp = "%s\n"%(m_i)
				output_f_mi.write(s_temp)
				i+=1
	print i
	output_f_mi.close()
	print "Generation have Finished result in file %s"%(pos_file)
	print "Generation have Finished result in file %s"%(vel_file)
	print "Generation have Finished result in file %s"%(con_file)

def create_xml_file(filename,generator):
	xml_writer = XMLWriter(filename)
	for p in generator.particles:
		xml_writer.add_particle(p)
	for c in generator.elasticConnections:
		xml_writer.add_connection(c)
	for m in generator.membranes:
		xml_writer.add_membrane(m)
	for  p in generator.particles:
		if p.type == Const.elastic_particle:
			for m_i in p.membranesIndex:
				xml_writer.add_membraneIndex(m_i)
	xml_writer.printtoFile()
def create_xml_file_1(filename,config):
	xml_writer = XMLWriter(filename)
	for p in config["position"]:
		xml_writer.add_particle(p)
	for c in config["econn"]:
		xml_writer.add_connection(c)
	xml_writer.printtoFile()
def create_collada_file(filename, g):
	colladawriter.writeheader(filename)
	pos_array = [p.position for p in g.particles if (p.type == Const.elastic_particle and not(p.ismemindexempty()))]
	normal_array = [p.get_normal(g.membranes, g.particles) for p in g.particles if (p.type == Const.elastic_particle and not(p.ismemindexempty()))] 
	colladawriter.writepositions(filename, "cube", pos_array)
	colladawriter.writenormales(filename, normal_array)
	triangles = [str(m) for m in g.membranes]
	colladawriter.writetriangles(filename, triangles)
	colladawriter.writefooter(filename)
	pass
if __name__ == '__main__':
	g = Generator('./3DModels/simple_cube_scene_for_gravity_test.x3d')#('./3DModels/simple_cube_now.x3d')#cube_with_elastic_cube2.x3d')
	g.genConfiguration()
	#create_collada_file("./configurations/colladafiles/collada_test_file.dae", g)
 	put_configto_file_temp(g,"./configurations/position.txt","./configurations/velocity.txt","./configurations/connection.txt", "./configurations/membranes.txt", "./configurations/particleMembraneIndex.txt")
 	#config = utils.read_config_from_file("./temp/out_config_step_0.txt")
 	#create_xml_file_1("friction_test_1", config)
 	#create_xml_file("friction_test_cube", g)
 	#create_xml_file("cube_with_membranes", g)
 	#create_xml_file("cube_with_liquid", g)
	
