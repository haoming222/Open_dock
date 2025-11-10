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

# 示例：捕获一个特定矩形区域的Google卫星图像
#left = 13155966.607518592849374
#top = 3672181.647986448369920
#right = 13156218.607518592849374
#bottom = 3671929.647986448369920
output_file = "G:/数据集/changjiang/changjiangtrunkpart2/not_cut/"

# 获取当前项目和图层
project = QgsProject.instance()
grid_layer = project.mapLayersByName('changjiang_clip2_grid')[0]
for feature in grid_layer.getFeatures():
    grid_id = feature.id()
    print(grid_id)
    capture_map_image(feature.attributes()[1], feature.attributes()[2], feature.attributes()[3], feature.attributes()[4], output_file+str(grid_id)+'.jpg')

    if grid_id==100:
        break





#capture_map_image(left, top, right, bottom, output_file)

print("图像已保存")













