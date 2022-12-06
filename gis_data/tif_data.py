


import cv2
import pdb
import numpy as np
from glob import glob


def convert_png(img, keep):
    img[keep] = ((img[keep]-img[keep].min())/(img[keep].max()-img[keep].min())*255)
    img[~keep]=255
    img = img.astype(np.uint8)
    return img
def save_png(path, output_dir, keep_pre=None):
    img = cv2.imread(path, -1)
    keep = img!=img[0,0]
    if keep_pre is not None:
        if not (keep_pre==keep).all():
            pdb.set_trace()
            # keep= np.maximum(keep_pre,keep)
            # pdb.set_trace()
    img=convert_png(img, keep)
    output_path = output_dir + '/' + path.split('\\')[-1].split(r'.')[0] + '.png'
    cv2.imwrite(output_path, img)
    return keep

    

if __name__ == '__main__':
    img_dir=r'D:\liu601\project\disaster\data\data'
    path_list = glob(img_dir + '\*.tif')
    output_dir = r'D:\liu601\project\disaster\data\show'
    keep=None
    for path in path_list:
        keep=save_png(path, output_dir, keep)
# if __name__ == '__main__':
#     path1 = r'D:\liu601\project\disaster\data\data\tdlylx.tif'
#     img1 = cv2.imread(path1, -1)
        # path2 = r'D:\liu601\project\disaster\data\data\DEM.tif'

    
    
    # path1 = r'D:\liu601\project\disaster\data\data\pd.tif'
    # ((img1==img1[0,0]) and (img2==img2[0,0]) and (img3==img3[0,0])).sum()
    # img1 = cv2.imread(path1, -1)
    # path2 = r'D:\liu601\project\disaster\data\data\DEM.tif'
    # img2 = cv2.imread(path2, -1)
    # path3 = r'D:\liu601\project\disaster\data\data\ql.tif'
    # img3 = cv2.imread(path3, -1)
    # keep = img1!=img1[0,0]
    # img1[img1==img1[0,0]]=0
    # img1[keep] = ((img1[keep]-img1[keep].min())/(img1[keep].max()-img1[keep].min())*255).astype(np.uint8)
    # img1[~keep]=255
    # cv2.imwrite('test.png', img1)
    # img1 = cv2.convertScaleAbs(img1, 255./img1.max())
    # pdb.set_trace()
    