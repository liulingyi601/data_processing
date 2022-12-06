# pip install pyshape
import shapefile
import pdb
import csv
from osgeo import gdal
from utils_gis import GeoTransform
def load_shapefile(path):
    sf = shapefile.Reader(path)
    shapes = sf.shapes()
    shape_records = sf.shapeRecords()
    fields = list(sf.fields)
    data_list = []
    pdb.set_trace()
    for i in range(len(shapes)):
        data_dict = {}
        shape = shapes[i]
        record = shape_records[i].record
        for j in range(len(fields)-1):
            data_dict[fields[j+1][0]] = record[j]
        data_dict["GX"] = shape.points[0][0]
        data_dict["GY"] = shape.points[0][1]
        data_list.append(data_dict)
    return data_list

if __name__=='__main__':
    pos_path = r'D:\liu601\project\data_processing\data\disaster\data\正样本\正样本.shp'
    neg_path = r'D:\liu601\project\data_processing\data\disaster\data\负样本\负样本.shp'
    tif_path = r'D:\liu601\project\data_processing\data\disaster\data\PJJY.tif'
    result_dir = r'D:\liu601\project\data_processing\data\disaster\result'
    output_neg_path = result_dir + '/neg_samples.csv'
    output_pos_path = result_dir + '/pos_samples.csv'
    neg_data = load_shapefile(neg_path)
    pos_data = load_shapefile(pos_path)
    ds = gdal.Open(tif_path)
    geotransorm = GeoTransform(ds.GetGeoTransform())
    for i in range(len(neg_data)):
        neg_data[i]['PX'], neg_data[i]['PY'] = geotransorm.geo2pixel(neg_data[i]['GX'], neg_data[i]['GY'])
    for i in range(len(pos_data)):
        pos_data[i]['PX'], pos_data[i]['PY'] = geotransorm.geo2pixel(pos_data[i]['GX'], pos_data[i]['GY'])
    pos_header_list = list(pos_data[0].keys())
    with open(output_pos_path, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, pos_header_list)
        writer.writeheader()
        writer.writerows(pos_data)  
    neg_header_list = list(neg_data[0].keys())
    with open(output_neg_path, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, neg_header_list)
        writer.writeheader()
        writer.writerows(neg_data) 

    
    
# path=r"D:\liu601\project\data_processing\data\disaster\data\NEG_sample.shp"
# output_path = r"D:\liu601\project\data_processing\data\disaster\result\pos_sample_shp.csv"
# sf = shapefile.Reader(path)
# shapes = sf.shapes()
# shape_records = sf.shapeRecords()
# fields = list(sf.fields)
# data_list = []
# F=3732675.7192163877

# C=18519903.73926363
# A=90.0360566378
# E=-90.0360566378
# # (18519903.739263635, 90.03605663778877, 0.0, 3732675.7192163877, 0.0, -90.03605663778866)
# # 90.0360566378
# # 0.0000000000
# # 0.0000000000
# # -90.0360566378
# # 18519948.7572919540
# # 3732630.7011880688
# # pdb.set_trace()
# for i in range(len(shapes)):
#     data_dict = {}
#     shape = shapes[i]
#     record = shape_records[i].record
#     for j in range(len(fields)-1):
#         data_dict[fields[j+1][0]] = record[j]
#     # pdb.set_trace()
#     y = (shape.points[0][1]-F)/E
#     x = (shape.points[0][0] - C) / A
#     data_dict["X"] = x
#     data_dict["Y"] = y
#     data_list.append(data_dict)
# header_list = list(data_list[0].keys())
# with open(output_path, mode='w', encoding='utf-8-sig', newline='') as f:
#     writer = csv.DictWriter(f, header_list)
#     writer.writeheader()
#     writer.writerows(data_list)  
    