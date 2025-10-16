import matplotlib.animation as animation 
import matplotlib.pyplot as plt 
import numpy as np

import random

from interpolate import interpolate
import data

def correlation(t: list[float], f: list, g: list):
    if not (len(t) == len(f) and len(t) == len(g)):
        raise Exception("Cannot cross-correlate with arrays of different lengths")

    

if __name__ == "__main__":
    d: list[data.Data] = data.lookup("data/r1/tracking_r1_prt_1.csv")

    time: list[float] = []
    target: list[data.Pos] = []
    hand: list[data.Pos] = []
    eye: list[data.Pos] = []

    for val in d:
        time.append(val.time)
        target.append(val.target)
        hand.append(val.hand)
        eye.append(val.eye)

    print(target)
