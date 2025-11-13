import matplotlib.animation as animation 
import matplotlib.pyplot as plt 
import numpy as np

import random

from interpolate import interpolate
import data

def correlation(x: float, t: list[float], f: list[data.Pos], g: list[data.Pos]) -> float:
    if not (len(t) == len(f ) and len(t) == len(g)):
        raise Exception("Cannot cross-correlate with arrays of different lengths")
    
    sum: float = 0.0

    for i in range(len(t) - 1):
        if i - int(x) >= 0 and i - int(x) < len(g):
            dt = t[i + 1] - t[i]
            prod = data.dot(f[i], g[i-int(x)]) # between 0 and 1, higher values mean points are closer together
            sum += prod * dt
            # print(prod)

    print(sum)
    return sum


def get_similarity(f: list[data.Pos], g: list[data.Pos]) -> list[float]:
    result: list[float] = []

    for i in range(len(f)):
        similarity = 1.0 / (1.0 + data.dot(f[i] - g[i], f[i] - g[i])) # between 0 and 1, higher values mean points are closer together
        result.append(similarity)

    return result


if __name__ == "__main__":
    # resolution of monitor
    res_x = 3840 # maybe 4096?
    res_y = 2160


    d: list[data.Data] = data.lookup("data/r1/tracking_r1_prt_1.csv")

    time: list[float] = []
    target: list[data.Pos] = []
    hand: list[data.Pos] = []
    eye: list[data.Pos] = []

    # read the data into the lists and convert ranges to -1 to 1 for easier processing
    for val in d:
        time.append(val.time)
        target.append(val.target * (2 / res_x, 2 / res_y) - (1, 1))
        hand.append(val.hand * (2 / res_x, 2 / res_y) - (1, 1))
        eye.append(val.eye * 2 - (1, 1))

    sum = 0
    for x in range(3600):
        sum += correlation(x, time, target, hand)

    sum *= 0.00833564879133093

    print(sum)