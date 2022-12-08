import cv2
import csv
from osgeo import gdal
import numpy as np
from utils_gis import convert_uint8
from glob import glob
import pdb
import os
def show_result(img_path, pos_points_path, neg_points_path, result_path):
    print(img_path)
    ds = gdal.Open(img_path)
    data= ds.ReadAsArray()
    if len(data.shape)==2:
        data = data[None]
    data = data.transpose(1,2,0)

    if data.shape[2] ==1:
        data = np.tile(data,3)
    # if data.dtype!='uint8':
    data = convert_uint8(data)
    with open(pos_points_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = int(float(row['PX']))
            y = int(float(row['PY']))
            cv2.circle(data, (x,y), 5, (0,255,0), -1)
    with open(neg_points_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = int(float(row['PX']))
            y = int(float(row['PY']))
            cv2.circle(data, (x,y), 5, (255,0,0), -1)
    cv2.imwrite(result_path, data)

if __name__=='__main__':
    im_dir = r'D:\liu601\project\data_processing\data\disaster\data'
    pos_points_path = r'D:\liu601\project\data_processing\data\disaster\result\pos_samples.csv'
    neg_points_path = r'D:\liu601\project\data_processing\data\disaster\result\neg_samples.csv'
    result_dir = r'D:\liu601\project\data_processing\data\disaster\image'
    # file_path=r'D:\liu601\project\data_processing\data\disaster\data\LWJL.tif'
    # name = os.path.basename(file_path)
    # result_path = result_dir + '/' + name.replace('tif', 'png')
    # show_result(file_path, pos_points_path, neg_points_path, result_path)

    file_list = glob(im_dir + '/*.tif')
    for file_path in file_list:
        name = os.path.basename(file_path)
        result_path = result_dir + '/' + name.replace('tif', 'png')
        show_result(file_path, pos_points_path, neg_points_path, result_path)
    
    # ds = gdal.Open(im_path)
    # # pdb.set_trace()
    # data= ds.ReadAsArray()
    # if len(data.shape)==2:
    #     data = data[None]
    # data = data.transpose(1,2,0)

    # if data.shape[2] ==1:
    #     data = np.tile(data,3)

    # if data.dtype!='uint8':
    #     img = convert_uint8(data)
    # with open(pos_csv_path, encoding="utf-8-sig") as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         x = int(float(row['PX']))
    #         y = int(float(row['PY']))
    #         cv2.circle(img, (x,y), 5, (0,255,0), -1)
    # with open(neg_csv_path, encoding="utf-8-sig") as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         x = int(float(row['PX']))
    #         y = int(float(row['PY']))
    #         cv2.circle(img, (x,y), 5, (255,0,0), -1)
    # cv2.imwrite(result_path, img)


# csv_path = r"D:\liu601\project\data_processing\data\disaster\result\pos_sample_shp.csv"
# im_path = r"D:\liu601\project\data_processing\data\disaster\show\showpx.png"
# img = cv2.imread(im_path)
# with open(csv_path, encoding="utf-8-sig") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         x = int(float(row['X']))
#         y = int(float(row['Y']))
#         cv2.circle(img, (x,y), 5, (0,255,0), -1)
# cv2.imwrite('result.png', img)

# def show_png()