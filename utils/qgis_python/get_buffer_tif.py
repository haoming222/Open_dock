from qgis.core import QgsPoint, QgsGeometry, QgsProject, QgsCoordinateReferenceSystem,QgsPointXY, QgsFeature, QgsRasterLayer
import qgis.processing
from qgis.utils import iface
def get_tif(left,top,right,bottom,id,buffer,output_path):
    canvas = iface.mapCanvas()
    extent = QgsRectangle(left-buffer,top+buffer,right+buffer,bottom-buffer)
    #raster_layer = QgsProject.instance().mapLayersByName("Google Satellite")[0]
    canvas.setExtent(extent)
    canvas.refresh()
    #raster_layer = QgsProject.instance().mapLayersByName('Google Satellite')[0]
    processing.run("native:rasterize", {'EXTENT':extent,'EXTENT_BUFFER':0,'MAP_UNITS_PER_PIXEL':0.4,'MAKE_BACKGROUND_TRANSPARENT':False,'MAP_THEME':None,'LAYERS':['type=xyz&zmin=0&zmax=20&url=https://mt1.google.com/vt/lyrs%3Ds%26x%3D{x}%26y%3D{y}%26z%3D{z}'],'OUTPUT':output_path })
    


buffer = 700
point_layer = QgsProject.instance().mapLayersByName("700notbuffer_pier_points")[0]

polygon_layer = QgsProject.instance().mapLayersByName("changjiang_clip1_700grid")[0]
polygon_crs = polygon_layer.crs()
point_crs = point_layer.crs()

#if point_crs != polygon_crs:
transformer = QgsCoordinateTransform(point_crs, polygon_crs, QgsProject.instance())

sum = 0
for i in range (6):
    num = i + 1
    polygon_layer = QgsProject.instance().mapLayersByName("changjiang_clip"+str(num)+"_700grid")[0]
    n = 0
    for point_feature in point_layer.getFeatures():
        point_geom = point_feature.geometry()
        point_geom = transformer.transform(point_geom.asPoint())
        
        #if n >= 100:
        #    break
        
        for polygon_feature in polygon_layer.getFeatures():
            polygon_geom = polygon_feature.geometry()
            polygon_left = polygon_feature["left"]
            polygon_top = polygon_feature["top"]
            polygon_right = polygon_feature["right"]
            polygon_bottom = polygon_feature["bottom"]
            if point_geom.x()>polygon_left and point_geom.y()<polygon_top and point_geom.x()<polygon_right and point_geom.y()>polygon_bottom:
                
                
                #print(f"转换后的坐标: {point_geom}")
                
                
                output_path = 'G:/data/700/detect/buffer_700/'+str(num)+'/notcut/'+str(polygon_feature.id())+'.tif'
                sum = sum + 1
                get_tif(polygon_left,polygon_top,polygon_right,polygon_bottom,polygon_feature.id(),buffer,output_path)
                #print(f"点 {point_feature.id()} 在多边形 {polygon_feature.id()} 内")
        n = n + 1        

print("总数：",sum)
print("ok")