import csv
import numpy as np
import matplotlib.pyplot as plt

file = open("tracking_r1_prt_1.csv", "r")
#data lookup function
def data_lookup(correlation, column_name):
    data = []
    with open(correlation, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(float(row[column_name]))
    return data

data_lookup("tracking_r1_prt_1.csv", "0")

#just random ahh code :( will do later in emc skills