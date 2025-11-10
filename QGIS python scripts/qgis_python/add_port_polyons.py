from qgis.core import (
    QgsProject, 
    QgsFeature, 
    QgsGeometry, 
    QgsPointXY, 
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform
)

from qgis.core import (
    QgsProject,
    QgsGeometry,
    QgsFeature,
    QgsRectangle,
)  
import shutil
import os
import chardet
import re



def add_point(layer_name,point_id,coord_x,coord_y,class_index):
    # 获取指定图层（假设图层名称为 'my_layer'）
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]

    # 检查图层的坐标系
    layer_crs = layer.crs()
    #print(f"Layer CRS: {layer_crs.authid()}")

    # 如果图层坐标系不是 EPSG:3857，则需要进行坐标转换
    target_crs = QgsCoordinateReferenceSystem('EPSG:3857')
    if layer_crs != target_crs:
        transform = QgsCoordinateTransform(target_crs, layer_crs, QgsProject.instance())
    else:
        transform = None

    # 假设要添加的点的坐标（在 EPSG:3857 下）
    point_3857 = QgsPointXY(coord_x,coord_y)

    # 如果需要进行坐标转换
    if transform:
        point_layer_crs = transform.transform(point_3857)
    else:
        point_layer_crs = point_3857

    # 开始编辑图层
    layer.startEditing()

    # 创建一个新的点要素
    feature = QgsFeature()

    # 创建几何对象并设置为点要素的几何属性
    geometry = QgsGeometry.fromPointXY(point_layer_crs)
    feature.setGeometry(geometry)

    # 设置要素的属性值（假设图层有一个属性字段 'name'）
    feature.setAttributes([point_id,class_index])

    # 将要素添加到图层中
    layer.addFeature(feature)

    # 提交编辑
    layer.commitChanges()

    # 刷新图层以显示新添加的要素
    layer.triggerRepaint()



def grid_layer_attrList(layer_name):
    grid_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    attributes = []
    for feature in grid_layer.getFeatures():
        attr = feature.attributes()
        attributes.append(attr)
    return attributes
    

def get_point_relative_coord(select_path):
    subfiles_and_subfolders = os.listdir(select_path)
    names_without_extension = [os.path.splitext(name)[0] for name in subfiles_and_subfolders]
    names_without_extension = sorted(list(map(int,names_without_extension)))
    #print(len(names_without_extension))
    i = 0
    point_info = []
    for n in names_without_extension:
        with open(select_path + str(n)+'.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        center_relative_coord = re.findall(r'中心点的坐标为：\((\d+\.\d+),(\d+\.\d+)\)，类别id为(\d+)', content)
        #print(center_relative_coord)
        info = ['0','0','0','0']
        for c in center_relative_coord:
            info = [n,float(c[0]),float(c[1]),float(c[2])]
            point_info.append(info)
    print(len(point_info))
    return point_info
    

def get_point_absolute_coord(jpg_size,relative_coord,grid_attrList,buffer,relative_h_w):
    for r_c in range(len(relative_coord)):
        grid_w = grid_attrList[relative_coord[r_c][0]][3] - grid_attrList[relative_coord[r_c][0]][1] + 2*buffer
        grid_h = grid_attrList[relative_coord[r_c][0]][2] - grid_attrList[relative_coord[r_c][0]][4] + 2*buffer
        
        per_w = grid_w/jpg_size
        per_h = grid_h/jpg_size
        #print(per_w)
        #print(per_h)
        
        relative_coord[r_c] = [relative_coord[r_c][0],grid_attrList[relative_coord[r_c][0]][1]-buffer+relative_coord[r_c][1]*per_w,grid_attrList[relative_coord[r_c][0]][2]+buffer-relative_coord[r_c][2]*per_h,relative_coord[r_c][3]]
    #print(relative_coord)
    return relative_coord
    
def get_polygons_absolute_h_w(jpg_size,select_path,grid_attrList,buffer):
    
    subfiles_and_subfolders = os.listdir(select_path)
    names_without_extension = [os.path.splitext(name)[0] for name in subfiles_and_subfolders]
    names_without_extension = sorted(list(map(int,names_without_extension)))
    #print(len(names_without_extension))
    i = 0
    h_infos = []
    w_infos = []
    h_w_infos = []
    for n in names_without_extension:
        with open(select_path + str(n)+'.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        relative_h = re.findall(r'高为\s*(\d+\.\d+|\d+)', content)
        relative_w = re.findall(r'宽为\s*(\d+\.\d+|\d+)', content)
        
        h_infos = h_infos + relative_h
        w_infos = w_infos + relative_w
        
        
    h_list = list(map(float,h_infos))
    w_list = list(map(float,w_infos))
    #print(point_info)
    
    grid_w = grid_attrList[0][3] - grid_attrList[0][1] + 2*buffer
    grid_h = grid_attrList[0][2] - grid_attrList[0][4] + 2*buffer
    per_w = grid_w/jpg_size
    per_h = grid_h/jpg_size
    for i in range(len(h_list)):
        h_list[i] = h_list[i] * per_h
        w_list[i] = w_list[i] * per_w
    #print(len([h_list,w_list]))
    return [h_list,w_list]


 

def add_polygons(layer_name,point_id,source,coord_x,coord_y,class_index,h,w):
    
    project = QgsProject.instance()
    layer_name = layer_name
    layer = project.mapLayersByName(layer_name)[0]

    layer.startEditing()

    center_x = coord_x  # 矩形中心的X坐标
    center_y = coord_y  # 矩形中心的Y坐标
    width = w      # 矩形的宽度
    height = h      # 矩形的高度

    x_min = center_x - width / 2
    y_min = center_y - height / 2
    x_max = center_x + width / 2
    y_max = center_y + height / 2

    rect_geometry = QgsGeometry.fromRect(QgsRectangle(x_min, y_min, x_max, y_max))

    feature = QgsFeature()
    feature.setGeometry(rect_geometry)
    
    feature.setAttributes([point_id,source,class_index])

    layer.addFeature(feature)

    layer.commitChanges()




for i in range(6):
    ia = i + 1
    jpg_size = 2908
    buffer  = 500
    grid_attrList = grid_layer_attrList("changjiang_clip"+str(ia)+"_454grid")
    select_path = 'G:/pier/500/all_model/train_1280size/yolov5lite/buffer_500/'+str(ia)+'/detect_result_h_w/'
    relative_coord = get_point_relative_coord(select_path)
    absolute_h_w = get_polygons_absolute_h_w(jpg_size,select_path,grid_attrList,buffer)
    absolute_coord = get_point_absolute_coord(jpg_size,relative_coord,grid_attrList,buffer,absolute_h_w)
    id = 0
    n = 0
    for a_c in absolute_coord:
        
        h = absolute_h_w[0][n]
        w = absolute_h_w[1][n]
        add_polygons('size1280_yolov5lite_500buffer500_pier_polygons',id,str(ia)+"_"+str(a_c[0]),a_c[1],a_c[2],a_c[3],h,w)
        #add_point('700notbuffer_pier_points',id,a_c[1],a_c[2],a_c[3])
        id = id + 1
        n = n + 1
        
        #if id >= 100:
        #    break;
    print(id)
print('添加完成')