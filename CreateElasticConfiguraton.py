'''
Created on 27.02.2013

@author: Serg
'''
import sys
class connection(object):
    def __init__(self,jd,rij0,val1=0.0,val2=0.0):
        self.jd = jd
        self.rij0 = rij0
        self.val1 = val1
        self.val2 = val2
    def __str__(self, *args, **kwargs):
        return '%s\t%s\t%s\t%s\n'%(self.jd,self.rij0,self.val1,self.val2)
    @staticmethod
    def get_empty():
        return connection(-1,-1,-1,-1)
ELASTIC_PARTICLE_COUNT = 7327
NEIGHBOUR_COUNT = 32
BOUNDARY_PARTICLE_COUNT = 33074

elasticConnectionData = [-1] * ELASTIC_PARTICLE_COUNT * NEIGHBOUR_COUNT * 4
next_empty_cell = [0] * ELASTIC_PARTICLE_COUNT

elasticConnnection = [[]] * ELASTIC_PARTICLE_COUNT
def fill():
    f = open('./source/elasticconnections.txt','r')
    currentId = 0
    firstIteration = True
    local_arr = []
    steps = 0
    for line in f:
        lineArr = line.strip('\n').split('\t')
        id = int(float(lineArr[0]))
        if id == 38074:
            #print str(steps)
            pass
        if firstIteration:
            currentId = id
            firstIteration = False
        if currentId == id:
            local_arr.append(connection(float(lineArr[1]),float(lineArr[2])))
        else:
            steps += 1
            elasticConnnection[currentId - BOUNDARY_PARTICLE_COUNT] = local_arr#append(local_arr)
            local_arr =[]
            currentId = id
            local_arr.append(connection(float(lineArr[1]),float(lineArr[2])))
    if local_arr != []:
        elasticConnnection[currentId - BOUNDARY_PARTICLE_COUNT] = local_arr
    f.close()
      
def extend():
    for l in elasticConnnection:
        if len(l) < NEIGHBOUR_COUNT:
            l.extend([connection.get_empty()]*(NEIGHBOUR_COUNT - len(l)))
        #elif len(l) > NEIGHBOUR_COUNT:
        #    print len(l)
            #sys.exit(0)
    
def put_to_file():
    f = open('./configurations/elasticconnections_1.txt','w')
    for l in elasticConnnection:
        for c in l:
            f.write(str(c)) #str(elasticConnnection.index(l)) + '\t' +
    f.close()


if __name__ == '__main__':
    #readFormFile()
    fill()
    extend()
    put_to_file()
    print "finish"