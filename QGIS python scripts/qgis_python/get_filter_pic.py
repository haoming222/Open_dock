import os
from qgis.core import QgsProject, QgsRectangle, QgsMapSettings, QgsMapRendererCustomPainterJob
from qgis.PyQt.QtGui import QImage, QPainter


# 确保QGIS项目已经打开
project = QgsProject.instance()

# 获取当前的地图画布
canvas = iface.mapCanvas()

# 创建一个函数，用于根据给定的坐标范围捕获地图图像
def capture_map_image(left, top, right, bottom, output_file):
    # 设置地图范围
    rect = QgsRectangle(left, bottom, right, top)
    canvas.setExtent(rect)
    canvas.refresh()

    # 创建QgsMapSettings对象并配置
    map_settings = QgsMapSettings()
    map_settings.setExtent(rect)
    map_settings.setLayers(canvas.layers())
    #map_settings.setOutputSize(QSize(1680, 1680))
    map_settings.setOutputSize(canvas.size())
    map_settings.setDestinationCrs(canvas.mapSettings().destinationCrs())

    # 创建QImage对象用于存储捕获的图像
    image = QImage(canvas.size(), QImage.Format_ARGB32_Premultiplied)
    image.fill(0)

    # 创建QPainter对象用于绘制图像
    painter = QPainter(image)

    # 创建QgsMapRendererCustomPainterJob对象并执行
    render = QgsMapRendererCustomPainterJob(map_settings, painter)
    render.start()
    render.waitForFinished()

    # 保存图像到文件
    image.save(output_file, "jpg")
    painter.end()

import os

grid_items = []
grid_ids = []
output_file = "G:/data/500/all_model/train_1280size/yolov11/not_buffer/get_filter_by_only_fd_lz_labels/pic_0.5relation/"
for n in range(6):
    labelpath = "G:/data/500/all_model/train_1280size/yolov11/not_buffer/"+str(n+1)+"/test_dataset/img_source/"
    l_n = [os.path.splitext(name)[0] for name in os.listdir(labelpath)]
    #print(l_n)
    grid_item = []
    for l in l_n:
        if "_" in l:
            #print(l)
            n = l.split('_')[1]
            grid_id = l.split('_')[0]
            grid_item.append(int(n))
    grid_ids.append(grid_id)
    grid_items.append(grid_item)
#print(len(grid_ids))
#print(grid_items)
#print(type(grid_items[1][1]))
    


# 获取当前项目和图层
for n in range(len(grid_ids)):
    project = QgsProject.instance()
    grid_layer = project.mapLayersByName('changjiang_clip'+grid_ids[n]+'_454grid')[0]
    for feature in grid_layer.getFeatures():
        
        grid_id = feature.id()
        if grid_id in grid_items[n]:
            print(grid_ids[n])
            print(grid_id)
            id = str(grid_id)
            #print(type(grid_id))
            capture_map_image(feature.attributes()[1], feature.attributes()[2], feature.attributes()[3], feature.attributes()[4], output_file+grid_ids[n]+'_'+id+'.jpg')

        #if grid_id>100:
        #    break


#capture_map_image(left, top, right, bottom, output_file)

print("图像已保存")













