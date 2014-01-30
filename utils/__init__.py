from generator.Particle import Particle,Float4
from generator.Const    import Const
from generator.ElasticConnection import ElasticConnection
def to_int_array(array):
    l = []
    for v in array:
        l.append(float(v))
    return l
def read_config_from_file(filename):
    config = {"position":[],"velocity":[],"econn":[]}
    in_file = open(filename, 'r')
    is_p_block = False
    is_v_block = False
    is_ec_block = False
    p_c = 0
    v_c = 0
    ec_c = 0
    for l in in_file:
        l = l.strip('\n')
        if l == "Position":
            is_p_block = True
            is_v_block = False
            is_ec_block = False
        if l == "Velocity":
            is_p_block = False
            is_v_block = True
            is_ec_block = False
        if l == "ElasticConnection":
            is_p_block = False
            is_v_block = False
            is_ec_block = True
        l_ = l.split('\t')
        if len(l_) == 4:
            l_t = to_int_array(l_)
            if is_p_block:
                config["position"].append(Particle( l_t[0], l_t[1],l_t[2], l_t[3] ) )
                p_c+=1
            if is_v_block:
                if int(l_t[3]) == int(Const.boundary_particle):
                    config["position"][v_c].setVelocity( Float4( l_t[0], l_t[1], l_t[2] ) )
                v_c+=1
            if is_ec_block:
                config["econn"].append( ElasticConnection( l_t[0], l_t[1], l_t[2], l_t[3]) )
                
    return config