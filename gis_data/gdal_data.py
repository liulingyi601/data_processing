
from osgeo import gdal
import pdb
import numpy as np
import cv2
from .utils_gis import GeoTransform

def read_image(filename):
    dataset = gdal.Open(filename)##调用Open函数打开遥感影像，并创建一个数据集：dataset
    width = dataset.RasterXSize##图像的列数
    height = dataset.RasterYSize##图像的行数
    image_proj = dataset.GetProjection()##获取投影信息
    image_geotrans = dataset.GetGeoTransform()##获取地理转换参数
    image_band = dataset.RasterCount##获取波段数
    image_data = dataset.ReadAsArray(0,0,width,height)##将栅格数据读作能够用numpy操作的array
    del dataset##在获取完数据之后记得删除数据集，释放内存

    return width,height,image_proj,image_geotrans,image_band,image_data

def convert_img(ori_iamge_data,ori_image_geotrans,det_image_geotrans,det_width,det_height):
    det_geotransform = GeoTransform(det_image_geotrans)
    ori_geotransform = GeoTransform(ori_image_geotrans)
    x1, y1 = ori_geotransform.geo2pixel(*det_geotransform.pixel2geo(0,0))
    x2, y2 = ori_geotransform.geo2pixel(*det_geotransform.pixel2geo(det_width,det_height))
    det_img= cv2.resize(ori_iamge_data[int(y1):int(y2), int(x1):int(x2)], (det_width, det_height))
    return det_img

def write_image(filename,proj,trans,image_data):
    if 'int8' in image_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in image_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(image_data.shape) == 2:
        image_data = np.array([image_data])
    im_bands,im_width,im_height = image_data.shape#获取数据的波段数、宽、高
    driver = gdal.GetDriverByName('GTiff')#注册一个类型为“tif"的驱动
    dataset = driver.Create(filename,im_height,im_width,im_bands,datatype)#借助驱动来创建一个"tif"的数据集
    dataset.SetGeoTransform(trans)#将转换参数写到数据集里
    dataset.SetProjection(proj)#将投影信息写到数据集里
    for band in range(im_bands):#range函数从0开始，例如3的话，遍历就是0，1，2
        dataset.GetRasterBand(band+1).WriteArray(image_data[band])#遍历将三个波段的数据写入数据集
    del dataset

if __name__=='__main__':
    ori_path=r"D:\liu601\project\data_processing\data\disaster\data\NDVI.tif"
    det_path=r"D:\liu601\project\data_processing\data\disaster\data\LWJL.tif"
    output_path = r"D:\liu601\project\data_processing\data\disaster\data\NDVI_det.tif"
    ori_width,ori_height,ori_image_proj,ori_image_geotrans,ori_image_band,ori_iamge_data=read_image(ori_path)
    det_width,det_height,det_image_proj,det_image_geotrans,det_image_band,det_iamge_data=read_image(det_path)
    det_img = convert_img(ori_iamge_data,ori_image_geotrans,det_image_geotrans,det_width,det_height)
    write_image(output_path,det_image_proj,det_image_geotrans,det_img)



