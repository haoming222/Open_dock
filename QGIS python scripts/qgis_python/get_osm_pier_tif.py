from qgis.core import QgsPointXY, QgsProject, QgsCoordinateTransform, QgsCoordinateReferenceSystem
from qgis.utils import iface
import shapely, geopandas
import os
from qgis.core import (
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransformContext,
    QgsCoordinateTransform,
    QgsProject,
    QgsPointXY,
    QgsRectangle,
    QgsProcessingFeedback,
    QgsProcessingContext,
    QgsProcessingParameters,
    QgsProcessingAlgorithm,
    QgsProcessingFeedback
)
from qgis import processing

def imagedownload(id,center_lon,center_lat):
    wgs84_center = QgsPointXY(center_lon, center_lat)

    # 获取当前项目的CRS
    project_crs = QgsProject.instance().crs()

    # 创建WGS84 CRS对象
    wgs84_crs = QgsCoordinateReferenceSystem('EPSG:4326')

    # 创建坐标转换对象
    transform = QgsCoordinateTransform(wgs84_crs, project_crs, QgsProject.instance())

    # 将WGS84坐标转换为项目的CRS
    new_center = transform.transform(wgs84_center)

    # 获取当前的地图画布
    canvas = iface.mapCanvas()

    # 设置新的中心点
    #canvas.setCenter(new_center)
    half_width = 350
    half_height = 350
    extent = QgsRectangle(new_center.x() - half_width, new_center.y() - half_height,
                        new_center.x() + half_width, new_center.y() + half_height)
       
    canvas.setExtent(extent)
    # 刷新画布以应用更改
    canvas.refresh()


    # save_map_as_image(extent, 200, 200, "D:/study/码头图片爬取/码头image/output_image.png")
    raster_layer = QgsProject.instance().mapLayersByName('Google Satellite')[0]
    #output_path = 'D:/study/码头图片爬取/add_not_port_image/'+str(id)+'.tif'
    output_path = 'E:/700/notcut/'+str(id)+'.tif'
    #print(raster_layer.isValid())
    processing.run("native:rasterize", {'EXTENT':extent,'EXTENT_BUFFER':0,'MAP_UNITS_PER_PIXEL':0.15,'MAKE_BACKGROUND_TRANSPARENT':False,'MAP_THEME':None,'LAYERS':['type=xyz&zmin=0&zmax=20&url=https://mt1.google.com/vt/lyrs%3Ds%26x%3D{x}%26y%3D{y}%26z%3D{z}'],'OUTPUT':output_path })

tpath = 'D:/浏览器下载/研究区码头/研究区码头.shp'
tpath = "D:/study/码头图片爬取/add_ports/add_ports.shp"
tpath = "D:/study/码头图片爬取/add_ports/add_not_ports.shp"
tpath = "D:/study/码头图片爬取/add_ports/add_ports2_isandnot.shp"
tpath = 'G:/长江水系/码头/qgis_pier/pier/changjiang_pier_Centroids.shp'
shp_df = geopandas.GeoDataFrame.from_file(tpath,encoding = 'gb18030')
#print(len(shp_df))
num = 1
for i in range(len(shp_df)):
    num = num + 1
    #if(i>2222 and i<2330):
    imagedownload(i,list(shp_df.geometry[i].coords[0])[0],list(shp_df.geometry[i].coords[0])[1])
    #if num >= 10:
    #    break
    
print('ok')