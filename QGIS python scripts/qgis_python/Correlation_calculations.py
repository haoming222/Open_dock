from qgis.core import QgsProject, QgsGeometry
# 获取图层
coorelation = 0.5
layer1 = QgsProject.instance().mapLayersByName("size1280_yolov11_500notbuffer_pier_polygons")[0]
layer2 = QgsProject.instance().mapLayersByName("size1280_yolov11_500buffer500_pier_polygons")[0]
copy_layer = QgsProject.instance().mapLayersByName("size1280_yolov11_"+str(coorelation)+"relation_filter_500notbuffer_pier_polygons")[0]
copy_layer.startEditing()
# 遍历两个图层的每个多边形要素
n = 0
for feature1 in layer1.getFeatures():
    geom1 = feature1.geometry()
    n = n + 1
    #if n >= 10:
    #   break;
    
    relations = []
    for feature2 in layer2.getFeatures():
        geom2 = feature2.geometry()
        
        # 计算交集
        intersection = geom1.intersection(geom2)
        # 检查交集是否存在
        if not intersection.isEmpty():
            # 获取重叠区域的面积
            f1attributes = feature1.attributes()
            f2attributes = feature2.attributes()
            print(f1attributes)
            #if(feature1.attributes()[2] == feature2.attributes()[2]):
            if(feature1.attributes()[1] == feature2.attributes()[1]):
                overlap_area = intersection.area()
                r = overlap_area/geom1.area()
                print(f"{f1attributes[0]}_{f1attributes[1]}和{f2attributes[0]}_{f2attributes[1]}")
                print(f"重叠面积: {overlap_area}相似度为{r}")
                relations.append(r)
                
                #new_feature = QgsFeature(copy_layer.fields())
                #new_feature.setGeometry(geom1)
                #new_feature.setAttributes(f1attributes+[r])
                #copy_layer.addFeature(new_feature)
    print(relations,"\n")
    
    
    
    print(feature1.attributes()[2] == 0)
    if(feature1.attributes()[2] == 0):
        new_feature = QgsFeature(copy_layer.fields())
        new_feature.setGeometry(geom1)
        new_feature.setAttributes(f1attributes+[1])
        copy_layer.addFeature(new_feature)
    else:
        #if(len(relations) and max(relations)>=0.5):
        if(len(relations) and max(relations)>=coorelation):
            new_feature = QgsFeature(copy_layer.fields())
            new_feature.setGeometry(geom1)
            new_feature.setAttributes(f1attributes+[max(relations)])
            copy_layer.addFeature(new_feature)
    
    #if((feature1.attributes()[2] == "0" or (feature1.attributes()[2] == "1" and max(relations)>=0.5)) and len(relations)):
    #    new_feature = QgsFeature(copy_layer.fields())
    #    new_feature.setGeometry(geom1)
    #    new_feature.setAttributes(f1attributes+[max(relations)])
    #    copy_layer.addFeature(new_feature)

    
copy_layer.commitChanges()   
                
                