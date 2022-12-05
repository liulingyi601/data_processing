from dbfread import DBF
import pdb
import csv
path = "D:\liu601\project\data_processing\data\地灾\数据\正样本\正样本.dbf"
csv_path = ''
table=DBF(path, encoding='utf-8')
data_list = []
F=3732630.7011880688
C=18519948.7572919540
A=90.0360566378
E=-90.0360566378
for data in table:
    near_y = data['NEAR_Y']
    near_x = data['NEAR_X']
    y = (near_y-F)/E
    x = (near_x - C) / A
    data['X']=x
    data['Y']=y
    data_list.append(dict(data))
header_list = list(data_list[0].keys())
with open('pos_sample.csv', mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, header_list)
    writer.writeheader()
    writer.writerows(data_list)
# 90.0360566378
# 0.0000000000
# 0.0000000000
# -90.0360566378
# 18519948.7572919540
# 3732630.7011880688