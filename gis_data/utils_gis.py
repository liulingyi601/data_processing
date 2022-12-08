import numpy as np
import pdb
def convert_uint8(img, keep=None):
    if keep is None:
        keep = gen_mask(img)
    # pdb.set_trace()
    if len(img.shape)==2:
        img[keep] = ((img[keep]-img[keep].min())/(img[keep].max()-img[keep].min())*255)
        img[~keep]=128
    else:
        for i in range(img.shape[2]):
            img_b = img[:,:,i]
            img_b[keep] = ((img_b[keep]-img_b[keep].min())/(img_b[keep].max()-img_b[keep].min())*255)
            img_b[~keep]=128
            img[:,:,i] = img_b
    img = img.astype(np.uint8)
    return img
def gen_mask(img, loc=None):
    if loc is None:
        w, h = img.shape[:2]
        assert (img[0, 0] == img[w-1, h-1]).all()
        mask = img!=img[0,0]
    else:
        mask = img!=img[loc[0], loc[1]]
    if img.dtype == 'int8':
        mask[img==-128]=False
    if len(mask.shape)==3:
        mask = mask.any(-1)
    
    return mask
class GeoTransform(object):
    def __init__(self, transform_data):
        self.transform_data=transform_data
        (self.off_x, self.relosution_x, self.rotation_x, self.off_y, self.rotation_y, self.relosution_y) = transform_data
    def geo2pixel(self, gx, gy):
        # pdb.set_trace()
        px = ((gx-self.off_x) * self.relosution_y - (gy-self.off_y) * self.rotation_x) / \
        (self.relosution_x*self.relosution_y- self.rotation_x* self.rotation_y)
        py = ((gy-self.off_y) * self.relosution_x - (gx-self.off_x) * self.rotation_y) / \
        (self.relosution_y*self.relosution_x- self.rotation_y* self.rotation_x)
        return px, py
    def pixel2geo(self, px, py):
        gx = self.off_x + px*self.relosution_x + py * self.rotation_x
        gy = self.off_y + py*self.relosution_y + px * self.rotation_y
        return gx, gy