import csv
import ast
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
        else:
            return Pos()
    
    def __add__(self, s):
        if isinstance(s, Pos):
            return Pos(self.x + s.x, self.y + s.y)
        if isinstance(s, tuple):
            return Pos(self.x + s[0], self.y + s[1])
        else:
            return Pos()
        
    def __sub__(self, s):
        if isinstance(s, Pos):
            return Pos(self.x - s.x, self.y - s.y)
        if isinstance(s, tuple):
            return Pos(self.x - s[0], self.y - s[1])
        else:
            return Pos()

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
class TMT:
    time: float
    hand: Pos
    eye: Pos

    def __init__(self, time=0.0, hand=Pos(), eye=Pos()):
        self.time = 0.0
        self.hand = hand
        self.eye = eye
    
    def __repr__(self):
        return '{' + f"{self.time}, {self.hand}, {self.eye}" + '}'

def dot(a: Pos | None, b: Pos | None) -> float:
    if isinstance(a, Pos) and isinstance(b, Pos):
        return a.x * b.x + a.y * b.y
    else:
        return 0.0
    
def similarity(a: Pos | None, b: Pos | None) -> float:
    if isinstance(a, Pos) and isinstance(b, Pos):
        if a.x == float('NaN') or a.y == float('NaN') or b.x == float('NaN') or b.y == float('NaN'):  
            return float('NaN')
        else:
            return dot(a - b, a - b)
    else:
        return float('NaN')
    
def cast_string(value: str):
    if not isinstance(value, str):
        raise TypeError("Input must be a string.")

    value = value.strip()

    # Handle common literals manually
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() == "none" or value.lower() == "null":
        return None

    # Try numeric conversions
    try:
        if "." in value or "e" in value.lower():
            return float(value)
        return int(value)
    except ValueError:
        pass

    # Try safe literal evaluation (list, dict, tuple, etc.)
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        pass

    # Fallback: return as string
    return value

#data lookup function
def lookup(data_filename: str, reject: bool = True, raw: bool = False) -> list:
    data = []
    file = open(data_filename, 'r')

    reader = csv.reader(file)

    for row in reader:
        if raw:
            row_list: list = list(row)
            for i, x in enumerate(row):
                row_list[i] = cast_string(x)
            data.append(tuple(row_list))
        else:
            row = tuple(row)

            valid = True

            if reject:
                for element in row:
                    if element == "NaN":
                        valid = False

            if valid:
                if len(row) == 7:
                    row_data: Data = Data()
                    row_data.time = float(row[0])
                    row_data.target = Pos(float(row[1]), float(row[2]))
                    row_data.hand = Pos(float(row[3]), float(row[4]))
                    row_data.eye = Pos(float(row[5]), float(row[6]))

                    data.append(row_data)
                elif len(row) == 5:
                    row_tmt: TMT = TMT()
                    row_tmt.time = float(row[0])
                    row_tmt.hand = Pos(float(row[1]), float(row[2]))
                    row_tmt.eye = Pos(float(row[3]), float(row[4]))

                    data.append(row_tmt)
                elif len(row) == 2:
                    row_pos: Pos = Pos()
                    row_pos = Pos(float(row[0]), float(row[1]))

                    data.append(row_pos)

    file.close()
    return data

res_x = 2560
res_y = 1440