# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from txt_data.csv_data import load_pd_csv
from osgeo import gdal
import pdb
from gis_data.utils_gis import gen_mask
import cv2
from gis_data.gdal_data import read_image, write_image
from glob import glob
import numpy as np
import copy
import h5py

import random

if __name__=='__main__':
    img_dir=r'D:\liu601\project\data_processing\data\disaster\data'
    result_dir = r'D:\liu601\project\data_processing\data\disaster\result'
    neg_path = r'D:\liu601\project\data_processing\data\disaster\result\neg_samples.csv'
    pos_path = r'D:\liu601\project\data_processing\data\disaster\result\pos_samples.csv'
    key_list = ['PX','PY']
    neg_data, key_list = load_pd_csv(neg_path,key_list)
    pos_data, key_list = load_pd_csv(pos_path,key_list)
    file_list = glob(img_dir + '/*.tif')
    mask = None
    for file_path in file_list:
        width,height,image_proj,image_geotrans,image_band,image_data=read_image(file_path)
        data_mask = gen_mask(image_data)
        if mask is None:
            mask = copy.deepcopy(data_mask)
            diff_mask = copy.deepcopy(data_mask)
        diff_mask[mask!=data_mask]=-1
        mask[mask!=data_mask] = 0
    valid_neg_points = []
    for i in range(len(neg_data)):
        if mask[int(neg_data.loc[i][key_list[1]]),int(neg_data.loc[i][key_list[0]])]:
            valid_neg_points.append([neg_data.loc[i][key_list[0]], neg_data.loc[i][key_list[1]]])
    valid_pos_points = []
    for i in range(len(pos_data)):
        if mask[int(pos_data.loc[i][key_list[1]]),int(pos_data.loc[i][key_list[0]])]:
            valid_pos_points.append([pos_data.loc[i][key_list[0]], pos_data.loc[i][key_list[1]]])
    random.shuffle(valid_neg_points)
    random.shuffle(valid_pos_points)
    train_pos_points = valid_pos_points[:int(len(valid_pos_points)*0.7)]
    test_pos_points = valid_pos_points[int(len(valid_pos_points)*0.7):]
    train_neg_points = valid_neg_points[:int(len(valid_neg_points)*0.7)]
    test_neg_points = valid_neg_points[int(len(valid_neg_points)*0.7):]
    train_im = np.zeros_like(mask).astype(np.uint8)
    for train_pos_point in train_pos_points:
        x1 = int(train_pos_point[0])
        y1 = int(train_pos_point[1])
        train_im[y1:y1+2, x1:x1+2]=2
    for train_neg_point in train_neg_points:
        x1 = int(train_neg_point[0])
        y1 = int(train_neg_point[1])
        train_im[y1:y1+2, x1:x1+2]=1
    test_im = np.zeros_like(mask).astype(np.uint8)
    for test_pos_point in test_pos_points:
        x1 = int(test_pos_point[0])
        y1 = int(test_pos_point[1])
        test_im[y1:y1+2, x1:x1+2]=2
    for test_neg_point in test_neg_points:
        x1 = int(test_neg_point[0])
        y1 = int(test_neg_point[1])
        test_im[y1:y1+2, x1:x1+2]=1
    # train_im[train_im==1]=128
    # train_im[train_im==2]=255
    # cv2.imwrite('train.png', train_im)

    valid_x = np.where(mask.max(0)>0)[0]
    valid_y = np.where(mask.max(1)>0)[0]
    l = valid_x.min()
    r = valid_x.max()
    u = valid_y.min()
    b = valid_y.max()
    train_im_path = result_dir + '/train.png'
    test_im_path = result_dir + '/test.png'
    cv2.imwrite(train_im_path, train_im[u:b+1, l:r+1])
    cv2.imwrite(test_im_path, test_im[u:b+1, l:r+1])
    h5_path = result_dir + '/data.h5'
    f=h5py.File(h5_path,"w")

    for file_path in file_list:
        # pdb.set_trace()
        width,height,image_proj,image_geotrans,image_band,image_data=read_image(file_path) 
        im = image_data[u:b+1, l:r+1]
        d1=f.create_dataset(os.path.basename(file_path).split('.')[0],data=im)

    f.close()
