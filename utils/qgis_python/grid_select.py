from qgis.core import QgsCoordinateTransform, QgsProject, QgsGeometry


# 假设你要写入相交信息
output_file = "G:/数据集/changjiangtrunk_454/1/grid_select/demo1.txt"

for i in range(6):
    n = 0
    i = i+1

    layer1 = QgsProject.instance().mapLayersByName('changjiang_cilp'+str(i)+'_1000grid')[0]
    #layer1 = QgsProject.instance().mapLayersByName('changjiang_cilp4_1000grid')[0]
    layer2 = QgsProject.instance().mapLayersByName('changjiang_pier')[0]
    # 获取图层的坐标参考系统（CRS）
    source_fields = layer1.fields()

    layer = QgsProject.instance().mapLayersByName('grid1000_select'+str(i))[0]  # 替换为目标图层名称
    #layer = QgsProject.instance().mapLayersByName('grid1000_select4'[0])  # 替换为目标图层名称
    layer.startEditing()

    target_fields = layer.fields()
    layer.dataProvider().deleteAttributes(list(range(len(target_fields))))
    layer.updateFields()

    layer.dataProvider().addAttributes(source_fields)
    layer.updateFields()
    layer.commitChanges()
    layer.triggerRepaint()


    crs_layer1 = layer1.crs()  # EPSG:3857
    crs_layer2 = layer2.crs()  # EPSG:4326

    transformer = QgsCoordinateTransform(crs_layer2, crs_layer1, QgsProject.instance())


    # 创建坐标转换器，将图层2的几何转换为图层1的坐标系
    transformer = QgsCoordinateTransform(crs_layer2, crs_layer1, QgsProject.instance())
    # 遍历图层1和图层2中的要素
    for feature1 in layer1.getFeatures():
        geom1 = feature1.geometry()
        n = n + 1
        if n==30:
            break
        num = 0
        for feature2 in layer2.getFeatures():
            geom2 = feature2.geometry()
            
            # 将图层2的几何形状转换为与图层1相同的坐标系 (EPSG:3857)
            geom2_transformed = QgsGeometry(geom2)
            geom2_transformed.transform(transformer)
            
            # 检测两个几何形状是否相交
            if geom1.intersects(geom2_transformed) and num == 0:
                # 将信息写入文件，而不是打印
                print('1')
                
                layer.startEditing()
                new_feature = QgsFeature()
                new_feature.setGeometry(geom1)
                new_feature.setAttributes(feature1.attributes())
                layer.addFeature(new_feature)
                
                
                layer.commitChanges()
                layer.triggerRepaint()
                num = num + 1
                    
                
print('ok')
                

