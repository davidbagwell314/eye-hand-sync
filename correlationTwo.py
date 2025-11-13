#recoded correlation
import numpy as np
import csv
from interpolate import interpolate

def lookup(path: str) -> list: #data lookup cuz ur function was bugging out in data.PY :(
    f = open(path, "r")
    reader = csv.reader(f)
    data = []
    for row in reader:
        data.append(row)
        for column in row:
            data.append(float(column))
    
    return data

def correlation(x):
    d: list = lookup("data/r1/tracking_r1_prt_4.csv")
    f = []
    g = []
    for i in range(3600):
        sum = 0
        sum += list.dot(f[i], g[i - float(x)])
        return sum / len(list)
    
print(correlation(0.0833564879133093))

