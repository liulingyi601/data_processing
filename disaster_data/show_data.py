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
from gis_data.utils_gis import convert_uint8

import random

if __name__=='__main__':
    train_img_path = r'D:\liu601\project\data_processing\data\disaster\result\train.png'
    test_img_path = r'D:\liu601\project\data_processing\data\disaster\result\test.png'
    show_dir = r'D:\liu601\project\data_processing\data\disaster\result_show'
    train_img = cv2.imread(train_img_path, -1)
    test_img = cv2.imread(test_img_path, -1)
    h5_path = r'D:\liu601\project\data_processing\data\disaster\result\data.h5'
    f = h5py.File(h5_path, 'r')
    
    for key in f.keys():
        im = f[key][:]
        pdb.set_trace()
        im = im[:,:,None].repeat(3,2)
        im_uint8 = convert_uint8(im)
        im_uint8[train_img==1]=np.array([255,0,0])
        im_uint8[train_img==2]=np.array([0,255,0])
        im_uint8[test_img==1]=np.array([255,0,255])
        im_uint8[test_img==2]=np.array([0,255,255])
        cv2.imwrite(show_dir + '/' + key + '.png', im_uint8)