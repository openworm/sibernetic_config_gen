'''
Created on 13.02.2013

@author: Serg
'''
from Const import Const
import math

class Float4(object):
    '''
    For good vectorization on OpenCL device we need to use 4 dimension vectors
    '''
    def __init__(self, x, y, z, val = 0.0):
        self.x = x
        self.y = y
        self.z = z
        self.val = val
    @staticmethod
    def getZeroVector():
        return Float4( 0.0, 0.0, 0.0, 0.0 )
    
    @staticmethod
    def dist(v1, v2):
        return math.sqrt( (v1.x - v2.x) * (v1.x - v2.x) + (v1.y - v2.y) * (v1.y - v2.y) + (v1.z - v2.z) * (v1.z - v2.z) )
    @staticmethod
    def dot(v1, v2): 
        return (v1.x - v2.x) * (v1.x - v2.x) + (v1.y - v2.y) * (v1.y - v2.y) + (v1.z - v2.z) * (v1.z - v2.z)
class Particle(object):
    def __init__(self, pos_x, pos_y, pos_z, p_type):
        self.position = Float4(pos_x,pos_y,pos_z, type)
        self.type = p_type
        if self.type == Const.liquid_particle or self.type == Const.elastic_particle:
            self.velocity = Float4(0.0,0.0,0.0,self.type)
    def setVelocity(self, velocity):
        self.velocity = velocity
    @staticmethod
    def distBetween_particles(p1,p2):
        return Float4.dist( p1.position, p2.position )
    @staticmethod
    def dot_particles(p1,p2):
        return Float4.dot( p1.position, p2.position )