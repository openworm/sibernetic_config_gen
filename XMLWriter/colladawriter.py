import time
header= "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
        <COLLADA xmlns=\"http://www.collada.org/2005/11/COLLADASchema\" version=\"1.4.1\">\n\
         <asset>\n\
          <contributor>\n\
           <authoring_tool>SceneKit Collada Exporter v1.0</authoring_tool>\n\
          </contributor>\n\
          <created>%s</created>\n\
          <modified>%s</modified>\n\
          <up_axis>Z_UP</up_axis>\n\
         </asset>\n\
         <library_materials>\n\
          <material id=\"Cube\" name=\"Cube\">\n\
           <instance_effect url=\"#Cube\"/>\n\
          </material>\n\
         </library_materials>\n\
         <library_effects>\n\
          <effect id=\"cube-effect\">\n\
           <profile_COMMON>\n\
            <technique sid=\"common\">\n\
             <phong>\n\
              <ambient>\n\
               <color>0 0 0 1</color>\n\
              </ambient>\n\
              <diffuse>\n\
               <color>0.16 0.32 0 1</color>\n\
              </diffuse>\n\
              <specular>\n\
               <color>0 0 0 1</color>\n\
              </specular>\n\
              <shininess>\n\
               <float>50</float>\n\
              </shininess>\n\
              <reflective>\n\
               <color>0 0 0 1</color>\n\
              </reflective>\n\
              <reflectivity>\n\
               <float>1</float>\n\
              </reflectivity>\n\
              <transparent opaque=\"A_ONE\">\n\
               <color>1 1 1 1</color>\n\
              </transparent>\n\
              <transparency>\n\
               <float>0.95</float>\n\
              </transparency>\n\
              <index_of_refraction>\n\
               <float>1</float>\n\
              </index_of_refraction>\n\
             </phong>\n\
            </technique>\n\
           </profile_COMMON>\n\
           <extra>\n\
            <technique profile=\"SceneKit\">\n\
             <double_sided>1</double_sided>\n\
             <litPerPixel>1</litPerPixel>\n\
            </technique>\n\
           </extra>\n\
          </effect>\n\
         </library_effects>\n\
         <library_geometries>"%(time.strftime("%x") + " " + time.strftime("%X"),time.strftime("%x") + " " + time.strftime("%X"))
         
         
footer = "</library_geometries>\n\
             <library_visual_scenes>\n\
              <visual_scene id=\"1\">\n\
               <node id=\"cube\" name=\"cube\">\n\
                <matrix>1 0 0 -0.0570503 0 1 0 3.54154 0 0 1 -0.116046 0 0 0 1 </matrix>\n\
                <instance_geometry url=\"#geometry1\">\n\
                 <bind_material>\n\
                  <technique_common>\n\
                   <instance_material symbol=\"geometryElement4\" target=\"#cube-material\"/>\n\
                  </technique_common>\n\
                 </bind_material>\n\
                </instance_geometry>\n\
               </node>\n\
               </visual_scene>\n\
             </library_visual_scenes>\n\
             <scene>\n\
              <instance_visual_scene url=\"#scene381\"/>\n\
             </scene>\n\
            </COLLADA>"
def writeheader(filename):
    colladafile = open(filename, "w")
    colladafile.write(header)
    colladafile.close()
def writepositions(filename,ob_name, position_array):
    colladafile = open(filename, "a")
    colladafile.write("<geometry id=\"geometry1\">\n")
    colladafile.write("<mesh>")
    colladafile.write("<cube-positions>")
    colladafile.write("<float_array id=\"%s\" count=\"%s\">"%("cube-poss-arr", len(position_array) * 3))
    posstring= ""
    for p in position_array:
        posstring += str(p) + " "
    colladafile.write(posstring)
    colladafile.write("</float_array>\n")
    colladafile.write("<technique_common>\n\
                      <accessor source=\"#ID2-array\" count=\"%s\" stride=\"3\">\n\
                       <param name=\"X\" type=\"float\"/>\n\
                       <param name=\"Y\" type=\"float\"/>\n\
                       <param name=\"Z\" type=\"float\"/>\n\
                      </accessor>\n\
                     </technique_common>\n\
                    </source>\n"%(len(position_array)))
    colladafile.close()
def writenormales(filename, normales_list):
    colladafile = open(filename, "a")
    colladafile.write("<source id=\"cube-mesh-normals\">")
    colladafile.write("<float_array id=\"%s\" count=\"%s\">"%("cube-normal-array", len(normales_list) * 3))
    n_list =  ""
    for n in normales_list:
        n_list += str(n.x) + " " + str(n.y) + " " + str(n.z) + " "
    colladafile.write(n_list)
    colladafile.write("</float_array>\n")
    colladafile.write("<technique_common>\n\
                      <accessor source=\"%s\" count=\"%s\" stride=\"3\">\n\
                       <param name=\"X\" type=\"float\"/>\n\
                       <param name=\"Y\" type=\"float\"/>\n\
                       <param name=\"Z\" type=\"float\"/>\n\
                      </accessor>\n\
                     </technique_common>\n\
                    </source>\n\
                    <vertices id=\"cube-mesh-positions-vertices\">\n\
                     <input semantic=\"POSITION\" source=\"#cube-mesh-positions\"/>\n\
                    </vertices>\n"%("cube-normal-array", len(normales_list)))
    colladafile.close()
def writetriangles(filename, triangles):
    colladafile = open(filename, "a")
    colladafile.write("<triangles count=\"%s\" material=\"geometryElement4\">\n\
                      <input semantic=\"VERTEX\" offset=\"0\" source=\"#cube-mesh-positions-vertices\"/>\n\
                      <input semantic=\"NORMAL\" offset=\"0\" source=\"#cube-mesh-normals\"/>")
    colladafile.write("<p>")
    t_str = ""
    for t in triangles:
        t_str += t
    colladafile.write(t_str)
    colladafile.write("</p>\n")
    colladafile.write(    "</triangles>\n\
                       </mesh>\n\
                      </geometry>\n")
    colladafile.close()
    
def writefooter(filename):
    colladafile = open(filename, "a")
    colladafile.write(footer)
    colladafile.close()
    
    
    
    
    
    
    
    