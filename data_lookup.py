import csv
import numpy as np
import matplotlib.pyplot as plt

class Pos:
    x: float
    y: float

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Data:
    time: float
    target: Pos
    hand: Pos
    eye: Pos

    def __init__(self, time=0.0, target=Pos(), hand=Pos(), eye=Pos()):
        self.time = 0.0
        self.target = target
        self.hand = hand
        self.eye = eye
    
    def __repr__(self):
        return '{' + f"{self.time}, {self.target}, {self.hand}, {self.eye}" + '}'

#data lookup function
def data_lookup(correlation):
    data = []
    with open(correlation, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = tuple(row)

            valid = True
            for element in row:
                if element == "NaN":
                    valid = False

            if valid:
                row_data: Data = Data()
                row_data.time = float(row[0])
                row_data.target = Pos(float(row[1]), float(row[2]))
                row_data.hand = Pos(float(row[3]), float(row[4]))
                row_data.eye = Pos(float(row[5]), float(row[6]))

                data.append(row_data)
    return data

if __name__ == "__main__":
    data = data_lookup("data/r3/tracking_r3_prt_4.csv")
    for row in data:
        print(row)