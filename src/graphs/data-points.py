import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.style as style

from emc_tools import data, interpolate

def init(): 
    t_line.set_data([target[0].x], [target[0].y])
    h_line.set_data([hand[0].x], [hand[0].y])
    e_line.set_data([eye[0].x], [eye[0].y])
    
    axis.set_xlim(-1.0, 1.0)
    axis.set_ylim(-1.0, 1.0)

    return t_line, h_line, e_line

# display the graphs
def display_graph(t):
    i = np.linspace(0, t, t, endpoint=False).astype(int)
    i = [time_index[j] for j in i]
 
    x = [target[j].x for j in i]
    y = [target[j].y for j in i]
    t_line.set_data(x, y)

    x = [hand[j].x for j in i]
    y = [hand[j].y for j in i]
    h_line.set_data(x, y)
    
    x = [eye[j].x for j in i]
    y = [eye[j].y for j in i]
    e_line.set_data(x, y)

    L.get_texts()[0].set_text("Target")
    L.get_texts()[1].set_text("Hand")
    L.get_texts()[2].set_text("Eye")

    return t_line, h_line, e_line

if __name__ == "__main__":
    d: list[data.Data] = data.lookup("data/tracking_circle/tracking_circle_r2_prt_1.csv", reject=False)

    time_index: list[int] = []
    time: list[float] = []
    target: list[data.Pos] = []
    hand: list[data.Pos] = []
    eye: list[data.Pos] = []

    timer = 0.0

    fps = 60
    time_start = 0
    time_end = 30

    # read the data into the lists and convert ranges to -1 to 1 for easier processing
    for i, val in enumerate(d):
        time.append(val.time)
        target.append(val.target * 2 - (1, 1))
        hand.append(val.hand * 2 - (1, 1))
        eye.append(val.eye * 2 - (1, 1))

    times = np.linspace(time_start, time_end, (time_end - time_start) * fps, endpoint=False)
    time_index = [interpolate.search(time, t) for t in times]

    style.use('fast')

    fig, axis = plt.subplots()

    t_line, = axis.plot([], [], lw = 2, color='tab:red')
    h_line, = axis.plot([], [], lw = 2, color='tab:green')
    e_line, = axis.plot([], [], lw = 2, color='tab:blue')

    L=axis.legend(handles=[t_line, h_line, e_line], loc=1)

    if True:
        # calling the animation function     
        anim = FuncAnimation(fig, display_graph, init_func = init, frames = len(time_index), interval=1000//fps, blit=True)
        
        # save the animation as a gif
        anim.save('graphs/data-paths.gif', writer=PillowWriter(fps=fps))

    elif True:
        init()
        display_graph(len(time_index))
        plt.savefig('graphs/data-paths-1s')

    else:
        display_graph(len(time_index))
        plt.savefig('graphs/saccade.png')