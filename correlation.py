import matplotlib.animation as animation 
import matplotlib.pyplot as plt 
import numpy as np

import random

# functions for correlation

cross_correlation_data_points = [random.randint(-10, 10) / 30 for _ in range(10)]

# interpolate between data points so it can find a continuous line between each point
def interpolate(data, t):
    # restrict the range of t
    if (t < 0):
        t = 0
    if (t > len(data) - 1):
        t = len(data) - 1

    node = int(t)
    t = t - float(node)

    if (node == len(data) - 1):
        return data[node]
    
    a = data[node]
    b = data[node + 1]
    return a * (1 - t) + b * t

def f(x):
    return np.exp(-4.0 * x * x) # change to suit the data

def g(x):
    sample = interpolate(cross_correlation_data_points, x * 5 + 5)
    return f(x) + sample
    return np.exp(-16.0 * x * x) * 0.5 # change to suit the data

def correlation(x, f, g):
    sum = 0
    for i in range(-100, 100, 1): # change the range to suit the data (this is currently just between -1 and 1, with dt=0.01)
        t = i / 100
        sum += f(t) * g(t - x) * 0.01

    return sum
 
# initialise the graphs
def init(): 
    line.set_data([], [])
    return line,

# display the graphs
def display_graph(j):
    t = (j - 100) * 0.01

    x_vals = []
    y_vals = [[], [], [], []]
    for i in range(-100, 100, 1):
        x = i / 100
        x_vals.append(x)
        y_vals[0].append(f(x))
        y_vals[1].append(g(x - t))
        y_vals[2].append(f(x) * g(x - t))
        y_vals[3].append(correlation(x, f, g))

    plt.cla()
    plt.fill_between(x_vals, y_vals[2], 0.0, color='lightblue', alpha=0.5)
    plt.plot(x_vals[:j], y_vals[3][:j], "green")
    plt.plot(x_vals, y_vals[2], "purple")
    plt.plot(x_vals, y_vals[1], "blue")
    plt.plot(x_vals, y_vals[0], "red")

    print("frame", j)
    return line,

if __name__ == "__main__":
    fig = plt.figure() 
    axis = plt.axes(xlim =(-1, 1),
                    ylim =(-0.5, 1.5)) 

    num_lines = 4 # the gif displays 4 different graphs

    # Initialize lines
    line, = axis.plot([], [])

    # calling the animation function     
    anim = animation.FuncAnimation(fig, display_graph, frames = 200, interval=0)
    
    # save the animation as a gif
    anim.save('cross_correlation.gif', writer = 'Pillow', fps = 30)