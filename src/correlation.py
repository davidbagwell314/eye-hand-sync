import matplotlib.animation as animation 
import matplotlib.pyplot as plt 
import numpy as np

import random

from emc_tools import data, interpolate

def correlation(x: float, t: list[float], f: list[data.Pos], g: list[data.Pos]) -> float:
    if not (len(t) == len(f ) and len(t) == len(g)):
        raise Exception("Cannot cross-correlate with arrays of different lengths")
    
    sum: float = 0.0

    for i in range(len(t) - 1):
        if i - int(x) >= 0 and i - int(x) < len(g):
            dt = t[i + 1] - t[i]
            f_val = interpolate.interpolate(f, 30 * i / len(t), t)
            g_val = interpolate.interpolate(g, (30 * i / len(t)) - x, t)
            prod = data.similarity(f_val, g_val) # between 0 and 1, higher values mean points are closer together
            sum += prod * dt
            
    return sum


def get_similarity(t:list[float], f: list[data.Pos], g: list[data.Pos], autocorrelation: float = 1.0):
    max_correlation = 0
    max_i = 0

    for z in range(100):
        x = z - 50
        result = correlation(x / 50, t, f, g)

        if result > max_correlation:
            max_correlation = result
            max_i = x

    return (correlation(0.0, t, f, g) / autocorrelation, max_correlation, max_i * (30 / 3600))


if __name__ == "__main__":
    d: list[data.Data] = data.lookup("data/tracking/tracking_r1_prt_1.csv")

    time: list[float] = []
    target: list[data.Pos] = []
    hand: list[data.Pos] = []
    eye: list[data.Pos] = []

    # read the data into the lists and convert ranges to -1 to 1 for easier processing
    for val in d:
        time.append(val.time)
        target.append(val.target * 2 - (1, 1))
        hand.append(val.hand * 2 - (1, 1))
        # target.append(val.target * (2 / data.res_x, 2 / data.res_y) - (1, 1))
        # hand.append(val.hand * (2 / data.res_x, 2 / data.res_y) - (1, 1))
        eye.append(val.eye * 2 - (1, 1))

    for i in range(len(time)):
        print(time[i], target[i], hand[i], eye[i])

    autocorrelation = get_similarity(time, target, target)[0] # cross-correlation results are pretty meaningless - this normalises results to the range 0-1

    print(get_similarity(time, target, hand, autocorrelation))
    print(get_similarity(time, target, eye, autocorrelation))