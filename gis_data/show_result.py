import cv2
import csv
csv_path = r"D:\liu601\project\data_processing\data\disaster\result\pos_sample_shp.csv"
im_path = r"D:\liu601\project\data_processing\data\disaster\show\showpx.png"
img = cv2.imread(im_path)
with open(csv_path, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        x = int(float(row['X']))
        y = int(float(row['Y']))
        cv2.circle(img, (x,y), 5, (0,255,0), -1)
cv2.imwrite('result.png', img)