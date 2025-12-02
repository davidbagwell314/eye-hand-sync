import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.style as style

from emc_tools import data, interpolate

def init():
    x = [point.x for point in points]
    y = [point.y for point in points]

    p_scatter.set_offsets(np.c_[x, y])
    for i in range(len(points)):
        plt.annotate(f'{i + 1}', (x[i], y[i]), xytext=(x[i], y[i]), ha='center', va='center', color='white')

    h_line.set_data([hand[0].x], [hand[0].y])
    e_line.set_data([eye[0].x], [eye[0].y])
    
    axis.set_xlim(-1.0, 1.0)
    axis.set_ylim(-1.0, 1.0)

    return p_scatter, h_line, e_line

# display the graphs
def display_graph(t):
    i = np.linspace(0, t, t, endpoint=False).astype(int)
    i = [time_index[j] for j in i]

    x = [hand[j].x for j in i]
    y = [hand[j].y for j in i]
    h_line.set_data(x, y)
    
    x = [eye[j].x for j in i]
    y = [eye[j].y for j in i]
    e_line.set_data(x, y)

    L.get_texts()[0].set_text("Points")
    L.get_texts()[1].set_text("Hand")
    L.get_texts()[2].set_text("Eye")

    return h_line, e_line

if __name__ == "__main__":
    name = "A1_prt_1"

    points: list[data.Pos] = data.lookup(f"data/Trail_Making_Time/points_TMT_{name}.csv", reject=False)
    d: list[data.TMT] = data.lookup(f"data/Trail_Making_Time/TMT_{name}.csv", reject=False)

    time_index: list[int] = []
    time: list[float] = []
    hand: list[data.Pos] = []
    eye: list[data.Pos] = []

    timer = 0.0

    fps = 10
    time_start = 0
    time_end = 30

    # read the data into the lists and convert ranges to -1 to 1 for easier processing
    for i, val in enumerate(d):
        time.append(val.time)
        hand.append(val.hand * 2 - (1, 1))
        eye.append(val.eye * 2 - (1, 1))

    points = [point * 2 - (1, 1) for point in points]

    times = np.linspace(time_start, time_end, (time_end - time_start) * fps, endpoint=False)
    time_index = [interpolate.search(time, t) for t in times]

    style.use('fast')

    fig, axis = plt.subplots()

    p_scatter = axis.scatter([], [], s = 200, color='tab:red')
    h_line, = axis.plot([], [], lw = 2, color='tab:green')
    e_line, = axis.plot([], [], lw = 2, color='tab:blue')

    L=axis.legend(handles=[p_scatter, h_line, e_line], loc=1)

    # calling the animation function     
    anim = FuncAnimation(fig, display_graph, init_func = init, frames = len(time_index), interval=1000//fps, blit=True)
        
    # save the animation as a gif
    anim.save(f'graphs/task2-paths-{name}.gif', writer=PillowWriter(fps=fps))