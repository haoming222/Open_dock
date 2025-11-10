from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsGeometry
)
from qgis.core import QgsProject, QgsFeature
# 加载图层
polygon_layer = QgsProject.instance().mapLayersByName('filter_onlyfd_300grid_port')[0]
line_layer = QgsProject.instance().mapLayersByName('changjiang_bridge')[0]
target_layer = QgsProject.instance().mapLayersByName('500grid_filter_by_relation_and_bridge')[0]
target_data_provider = target_layer.dataProvider()
n = 0
# 遍历多边形图层中的每一个要素
for poly_feature in polygon_layer.getFeatures():
    n = n + 1
    #if n > 100:
    #    break;
    
    poly_geom = poly_feature.geometry()
    intersect_flag = False  # 标记是否有相交的线条
    
    # 遍历线条图层中的每一个要素
    for line_feature in line_layer.getFeatures():
        line_geom = line_feature.geometry()
        
        # 检测是否相交
        if poly_geom.intersects(line_geom):
            intersect_flag = True
            print(f"多边形ID {poly_feature.id()} 与线条ID {line_feature.id()} 相交")
            break;
    
    # 如果没有与任何线条相交，可以输出其他信息
    if not intersect_flag:
        new_feature = QgsFeature()
        new_feature.setGeometry(poly_geom)
        new_feature.setAttributes(poly_feature.attributes())  # 保留原始属性
        target_data_provider.addFeature(new_feature)
        
        print(f"多边形ID {poly_feature.id()} 未与任何线条相交")
        
target_layer.updateExtents()
target_layer.triggerRepaint()
        
        
        
        
