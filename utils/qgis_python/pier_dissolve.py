from qgis.core import (
    QgsProject,
    QgsVectorLayer
)

pier_layer = QgsProject.instance().mapLayersByName(
"FD_pier_dissolve_5buffer2")[0]
pier_layer.startEditing()
field_index = pier_layer.fields().indexOf("dissolveid")
#print(field_index)
check_num = 1
dissolve_id_counter = 1
dissolve_id_list = []

#print(pier_layer.getFeature(758).geometry().intersects(pier_layer.getFeature(772).geometry()))

#print(pier_layer.getFeature(0).geometry().intersects(pier_layer.getFeature(1).geometry()))
for feature in pier_layer.getFeatures():
    check_num = check_num + 1
    #if check_num > 50:
    #    break;
    #print(check_num)
    f_geom = feature.geometry()
    if len(dissolve_id_list)==0:
        
        dissolve_id_list.append(dissolve_id_counter)
        dissolve_id_counter += 1
    else:
        for c in range(len(dissolve_id_list)):
            c_f = pier_layer.getFeature(c)
            c_f_geom = c_f.geometry()
            intersects_time = 0
            if f_geom.intersects(c_f_geom):
                print("香蕉了")
                dissolve_id_list.append(dissolve_id_list[c])
                break;
                
            else:
                if (c==len(dissolve_id_list)-1):
                    dissolve_id_list.append(dissolve_id_counter)
                    dissolve_id_counter += 1

print(dissolve_id_list)
print(len(dissolve_id_list))
counter = 0
for feature in pier_layer.getFeatures():
    #if counter>50:
    #    break;
    feature.setAttribute(field_index, dissolve_id_list[counter])
    pier_layer.updateFeature(feature)
    counter += 1

pier_layer.commitChanges()





