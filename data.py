import csv
import numpy as np
import matplotlib.pyplot as plt

class Pos:
    x: float
    y: float

    def __init__(self, x: float | None = 0.0, y: float | None = 0.0):
        if isinstance(x, float) and not isinstance(y, float):
            self.x = x
            self.y = x
        elif isinstance(x, float) and isinstance(y, float):
            self.x = x
            self.y = y
        else:
            self.x = 0.0
            self.y = 0.0

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def __mul__(self, s):
        if isinstance(s, float | int): # scalar multiplication
            return Pos(self.x * s, self.y * s)
        elif isinstance(s, Pos): # dot product
            return Pos(self.x * s.x, self.y * s.y)
        elif isinstance(s, tuple): # dot product
            return Pos(self.x * s[0], self.y * s[1])
    
    def __add__(self, s):
        if isinstance(s, Pos):
            return Pos(self.x + s.x, self.y + s.y)
        if isinstance(s, tuple):
            return Pos(self.x + s[0], self.y + s[1])
        
    def __sub__(self, s):
        if isinstance(s, Pos):
            return Pos(self.x - s.x, self.y - s.y)
        if isinstance(s, tuple):
            return Pos(self.x - s[0], self.y - s[1])

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

def dot(a: Pos | None, b: Pos | None) -> float:
    if isinstance(a, Pos) and isinstance(b, Pos):
        return a.x * b.x + a.y * b.y
    else:
        return 0.0

#data lookup function
def lookup(data_filename: str, reject: bool = True) -> list:
    data = []
    file = open(data_filename, 'r')

    reader = csv.reader(file)
    for row in reader:
        row = tuple(row)

        valid = True

        if reject:
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

    file.close()
    return data

res_x = 2560
res_y = 1440

if __name__ == "__main__":
    data = lookup("data/r3/tracking_r3_prt_4.csv")
    for row in data:
        print(row)