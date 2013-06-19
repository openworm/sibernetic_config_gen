'''
Created on 13.02.2013

@author: Serg
'''
from Generator.Generator import Generator
from Generator.Const import Const
import sys

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
def put_configto_file_temp(generator, filename="./configurations/configuration.txt"):
	'''
	Create configuration file and put information
	about particle position, velocity and elastic 
	connections.
	TODO: create more check 
	'''
	output_f_p = open("./configurations/position_test_for_Giovanni.txt","w")
	#output_f_p.write("Position\n")
	for  p in generator.particles:
		s_temp = "%s\t%s\t%s\t%s\n"%(p.position.x,p.position.y,p.position.z,p.type)
		output_f_p.write(s_temp)
	output_f_v = open("./configurations/velocity_test_for_Giovanni.txt","w")
	for  p in generator.particles:
		s_temp = "%s\t%s\t%s\t%s\n"%(p.velocity.x,p.velocity.y,p.velocity.z,p.velocity.val)
		output_f_v.write(s_temp)
	output_f_v.close()
	print "Generation have Finished result in file %s"%(filename)
if __name__ == '__main__':
	#g = Generator(120.24, 80.16, 180.36, particle_count = 1024*16)
	h = 40.0 * Const.h
	w = 24.0 * Const.h
	d = 54.0 * Const.h
	g = Generator(h, w, d)
	g.genConfiguration()
	put_configto_file(g)
	#put_configto_file_temp(g)