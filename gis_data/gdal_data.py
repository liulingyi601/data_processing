
from osgeo import gdal

import pdb
path="D:\liu601\project\data_processing\data\disaster\data\DCJL.tif"

ds = gdal.Open(path)
geotransform = ds.GetGeoTransform()
cols = ds.RasterXSize
rows = ds.RasterYSize
bands = ds.RasterCount
band = ds.GetRasterBand(1)
band_data = band.ReadAsArray(0, 0, 1, 1)
data= ds.ReadAsArray()

pdb.set_trace()



