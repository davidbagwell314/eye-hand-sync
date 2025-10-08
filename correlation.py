#correlation



#code for correlation function
 
import matplotlib.pyplot as plt
import numpy
 
def f(x):
    return numpy.exp(-4.0 * x * x) # change to suit the data
 
def g(x):
    return numpy.exp(-16.0 * x * x) * 0.5 # change to suit the data
 
def correlation(x, f, g):
    sum = 0
    for i in range(-100, 100, 1): # change the range to suit the data (this is currently just between -1 and 1, with dt=0.01)
        t = i / 100
        sum += f(t) * g(t - x) * 0.01
 
    return sum
 
def display_graph(t):
    x_vals = []
    y_vals = [[], [], [], []]
    for i in range(-100, 100, 1):
        x = i / 100
        x_vals.append(x)
        y_vals[0].append(f(x))
        y_vals[1].append(g(x - t))
        y_vals[2].append(f(x) * g(x - t))
        y_vals[3].append(correlation(x, f, g))
 
    plt.plot(x_vals, y_vals[0], color='red')
    plt.plot(x_vals, y_vals[1], color='blue')
    plt.plot(x_vals, y_vals[2], color='purple')
    plt.plot(x_vals, y_vals[3], color='green')
 
    plt.show()
 
if __name__ == "__main__":
    display_graph(0.5) 
    
