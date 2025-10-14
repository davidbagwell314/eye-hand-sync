import matplotlib.animation as animation 
import matplotlib.pyplot as plt 
import numpy as np 

def f(x):
    return np.exp(-4.0 * x * x) # change to suit the data

def g(x):
    return np.exp(-16.0 * x * x) * 0.5 # change to suit the data

def correlation(x, f, g):
    sum = 0
    for i in range(-100, 100, 1): # change the range to suit the data (this is currently just between -1 and 1, with dt=0.01)
        t = i / 100
        sum += f(t) * g(t - x) * 0.01

    return sum
 
# creating a blank window
# for the animation 
fig = plt.figure() 
axis = plt.axes(xlim =(-1, 1),
                ylim =(-0.5, 1.5)) 


num_lines = 3

# Initialize lines
lines = [axis.plot([], [], lw=2)[0] for _ in range(num_lines)]
 
# what will our line dataset
# contain?
def init(): 
    for line in lines:
        line.set_data([], [])
    return lines
 
# initializing empty values
# for x and y co-ordinates
 
# animation function 
def animate(t): 
    # t is a parameter which varies
    # with the frame number
    
    t = (t - 100) * 0.01

    j = 0
    for line in lines:
        xdata, ydata = [], []
        for i in range(-100, 100):
            x = i * 0.01
            y = f(x - t) + j
            xdata.append(x) 
            ydata.append(y) 
        
        line.set_data(xdata, ydata) 
        j += 1
    
    return lines
 
# calling the animation function     
anim = animation.FuncAnimation(fig, animate, init_func = init, 
                               frames = 200, interval = 20, blit = True) 
 
# saves the animation in our desktop
anim.save('growingCoil.gif', writer = 'Pillow', fps = 30)