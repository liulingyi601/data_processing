import shapefile
import pdb
import csv
path="D:\liu601\project\data_processing\data\disaster\data\正样本\正样本.shp"
output_path = r"D:\liu601\project\data_processing\data\disaster\result\pos_sample_shp.csv"
sf = shapefile.Reader(path)
shapes = sf.shapes()
shape_records = sf.shapeRecords()
fields = list(sf.fields)
data_list = []
F=3732630.7011880688

C=18519948.7572919540
A=90.0360566378
E=-90.0360566378

# 90.0360566378
# 0.0000000000
# 0.0000000000
# -90.0360566378
# 18519948.7572919540
# 3732630.7011880688
for i in range(len(shapes)):
    data_dict = {}
    shape = shapes[i]
    record = shape_records[i].record
    for j in range(len(fields)-1):
        data_dict[fields[j+1][0]] = record[j]
    # pdb.set_trace()
    y = (shape.points[0][1]-F)/E
    x = (shape.points[0][0] - C) / A
    data_dict["X"] = x
    data_dict["Y"] = y
    data_list.append(data_dict)
header_list = list(data_list[0].keys())
with open(output_path, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, header_list)
    writer.writeheader()
    writer.writerows(data_list)  
    