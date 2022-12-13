import pandas as pd
import csv
def load_pd_csv(path, key_list=None):
    try:
        data=pd.read_csv(path,encoding='gbk', usecols=key_list)
    except:
        data=pd.read_csv(path, usecols=key_list)
    if key_list is None:
        key_list = list(data)
    return data, key_list


def load_csv(path, key_list=None):
    try:
        with open(path, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]
    except:
        with open(path) as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]

    if key_list is None:
        key_list = list(rows[0].keys())
    datas = []
    for row in rows:
        data = []
        for key in key_list:
            if key not in row:
                data.append(0)
            else:
                data.append(row[key])
        datas.append(data)
    return datas, key_list