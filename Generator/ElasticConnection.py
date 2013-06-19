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


    def __init__(self,particle_j_id, distance, val1=0, val2=0):
        '''
        Constructor
        '''
        self.particle_j = (particle_j_id > 0) and (particle_j_id + 0.1) or particle_j_id
        self.r_ij = distance * Const.simulationScale
        self.val1 = val1
        self.val2 = val2
    