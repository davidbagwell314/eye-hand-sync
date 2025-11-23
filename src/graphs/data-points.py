import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.style as style

from emc_tools import data

# display the graphs
def display_graph(t):
    i = time_index[t]

    x_vals[0].append(target[i].x)
    y_vals[0].append(target[i].y)
        
    x_vals[1].append(hand[i].x)
    y_vals[1].append(hand[i].y)
        
    x_vals[2].append(eye[i].x)
    y_vals[2].append(eye[i].y)

    if (t > 1):
        plt.plot(x_vals[0][(t-2):t], y_vals[0][(t-2):t], color="red", label='target')
        # plt.plot(x_vals[1][(t-2):t], y_vals[1][(t-2):t], color="green", label='hand')
        # plt.plot(x_vals[2][(t-2):t], y_vals[2][(t-2):t], color="blue", label='eye')

    print("Currently processing:", t)

    return line,

if __name__ == "__main__":
    d: list[data.Data] = data.lookup("data/tracking/tracking_r1_prt_3.csv", reject=False)

    time_index: list[int] = []
    time: list[float] = []
    target: list[data.Pos] = []
    hand: list[data.Pos] = []
    eye: list[data.Pos] = []

    timer = 0.0

    # read the data into the lists and convert ranges to -1 to 1 for easier processing
    for i, val in enumerate(d):
        time.append(val.time)
        target.append(val.target * 2 - (1, 1))
        hand.append(val.hand * 2 - (1, 1))
        eye.append(val.eye * 2 - (1, 1))

        if True:
        #if val.time >= 23 and val.time <= 26:
            # don't plot the graph for each data point; plot it for each frame
            if ((val.time - timer) > (1.0 / 10.0) and len(time_index) < 30 * 10):
                timer = val.time
                for j in range(int((val.time - timer) / (1.0 / 10.0)) + 1):
                    time_index.append(i)

    style.use('fast')

    x_vals: list[list[float]] = [[], [], []]
    y_vals: list[list[float]] = [[], [], []]

    fig = plt.figure() 
    axis = plt.axes(xlim =(-1, 1),
                    ylim =(-1, 1)) 

    num_lines = 3 # the gif displays 3 different graphs

    # Initialize lines
    line, = axis.plot([], [])

    # calling the animation function     
    anim = animation.FuncAnimation(fig, display_graph, frames = len(time_index), interval=0, blit=True)
    
    # save the animation as a gif
    anim.save('graphs/target-points.gif', writer = 'Pillow', fps = 10)