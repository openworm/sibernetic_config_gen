'''
Created on 18.02.2013

@author: Serg
'''
from Particle import Particle
from Const import Const

class ElasticConnection(object):
    '''
    classdocs
    '''


    def __init__(self,particle_i_id, particle_j_id, distance):
        '''
        Constructor
        '''
        self.particle_i = particle_i_id 
        self.particle_j = particle_j_id
        self.distance = Const.simulationScale * distance
    