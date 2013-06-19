'''
Created on 13.02.2013

@author: Serg
'''

class Const(object):
    '''
    Const 
    '''
    h = 3.34
    r0 = h * 0.5
    r0_squared = r0 * r0
    mass = 3.25e-14
    #PROPERTY OF BOX
    xmin = 0
    ymin = 0
    zmin = 0
    xmax = 0
    ymax = 0    
    zmax = 0
    simulationScale = 0.004 * pow(mass,1.0/3.0)/pow(0.00025,1.0/3.0);
    #PROPERTY FIELDS
    liquid_particle = 1.1
    elastic_particle = 2.1
    boundary_particle = 3.1 
    #CONFIGURATION PARTICLE COUNT
    MAX_NUM_OF_NEIGHBOUR = 32
    LIQUID_PARTICLE_COUNT = 0
    ELASTIC_PARTICLE_COUNT = 0
    PARTICLE_COUNT = LIQUID_PARTICLE_COUNT + ELASTIC_PARTICLE_COUNT
    NO_PARTICEL_ID = -1.0
    '''
    Number of boundary particles depends from sizes of box.
    So I think don't include their in PARTICLE_COUNT
    '''
    BOUNDARY_PARTICLE_COUNT = 0 
    TOTAL_PARTICLE_COUNT = BOUNDARY_PARTICLE_COUNT + PARTICLE_COUNT 
    