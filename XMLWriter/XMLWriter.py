'''
Created on 20.06.2013

@author: Serg
'''
from xml.dom.minidom import Document
from Generator.Const import Const
class XMLWriter(object):
    '''
    classdocs
    '''

    def __init__(self, doc_name=''):
        '''
        Constructor
        '''
        self.docname = doc_name
        self.out_doc = Document()
        self.out_doc.version = "1.0"
        self.out_doc.doctype = "xml"
        self.out_doc.standalone = "yes"
        self.sph_element = self.out_doc.createElement('SPHModel')
        self.sph_element.setAttribute('zMin',str(Const.zmin))
        self.sph_element.setAttribute('zMax',str(Const.zmax))
        self.sph_element.setAttribute('xMin',str(Const.xmin))
        self.sph_element.setAttribute('xMax',str(Const.xmax))
        self.sph_element.setAttribute('yMin',str(Const.ymin))
        self.sph_element.setAttribute('yMax',str(Const.ymax))
        self.sph_element.setAttribute('xmlns',"http://www.example.org/SPHSchema")
        self.out_doc.appendChild(self.sph_element)
    def add_particle(self, particle):
        particle_ellement = self.out_doc.createElement('particles')
        particle_ellement.setAttribute('mass', str(Const.mass))
        p_pos_ellement = self.out_doc.createElement('positionVector')
        p_pos_ellement.setAttribute('p', str(particle.type))
        p_pos_ellement.setAttribute('z', str(particle.position.z))
        p_pos_ellement.setAttribute('y', str(particle.position.y))
        p_pos_ellement.setAttribute('x', str(particle.position.x))
        p_vel_ellement = self.out_doc.createElement('velocityVector')
        p_vel_ellement.setAttribute('p', str(particle.type))
        p_vel_ellement.setAttribute('z', str(particle.position.z))
        p_vel_ellement.setAttribute('y', str(particle.position.y))
        p_vel_ellement.setAttribute('x', str(particle.position.x))
        particle_ellement.appendChild(p_pos_ellement)
        particle_ellement.appendChild(p_vel_ellement)
        self.sph_element.appendChild(particle_ellement)
    def add_connection(self, connection):
        connection_ellement = self.out_doc.createElement('connections')
        jd_ellement = self.out_doc.createElement('p1')
        ptext = self.out_doc.createTextNode(str(connection.particle_j))
        jd_ellement.appendChild(ptext)
        distance_ellemtn = self.out_doc.createElement('distance')
        ptext = self.out_doc.createTextNode(str(connection.r_ij))
        distance_ellemtn.appendChild(ptext)
        val1_ellemnt = self.out_doc.createElement('mysteryValue')
        ptext = self.out_doc.createTextNode(str(connection.val1))
        val1_ellemnt.appendChild(ptext)
        connection_ellement.appendChild(jd_ellement)
        connection_ellement.appendChild(distance_ellemtn)
        connection_ellement.appendChild(val1_ellemnt)
        self.sph_element.appendChild(connection_ellement)
        
    def printtoFile(self):
        try:
            f = open('./configurations/' + self.docname + '.xml', 'w')
            f.write(self.out_doc.toprettyxml(encoding='utf-8'))
            f.close()
            print 'Configuration was save in file % s in flder configuration', self.docname + '.xml'
        except IOError as ex:
            print 'Configuration  wasn''t saved because : %s' % ex.strerror