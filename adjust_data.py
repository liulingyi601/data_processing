
from osgeo import gdal
import pdb
from gis_data.utils_gis import gen_mask
import cv2
from gis_data.gdal_data import read_image, write_image
from glob import glob
import numpy as np
import copy

if __name__=='__main__':
    img_dir=r'D:\liu601\project\data_processing\data\disaster\data'
    file_list = glob(img_dir + '/*.tif')
    mask = None
    pdb.set_trace()
    for file_path in file_list:
        width,height,image_proj,image_geotrans,image_band,image_data=read_image(file_path)
        data_mask = gen_mask(image_data)
        if mask is None:
            mask = copy.deepcopy(data_mask)
            diff_mask = copy.deepcopy(data_mask)
        diff_mask[mask!=data_mask]=-1
        mask[mask!=data_mask] = 0
    diff_masks_uint8 = diff_mask.astype(np.uint8)
    diff_masks_uint8[diff_mask==1]=255
    diff_masks_uint8[diff_mask==-1]=0
    diff_masks_uint8[diff_mask==0]=128
    pdb.set_trace()
    cv2.imwrite('mask.png', diff_masks_uint8.copy())


        
    

    
    