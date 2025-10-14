import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create a figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)

# Number of lines to animate
num_lines = 3

# Initialize lines
lines = [ax.plot([], [], lw=2)[0] for _ in range(num_lines)]

# Data for animation
x = np.linspace(0, 2 * np.pi, 100)
y_data = [np.sin(x + phase) for phase in np.linspace(0, 2 * np.pi, num_lines + 1)]

# Initialization function
def init():
    for line in lines:
        line.set_data([], [])
    return lines

# Animation function
def update(frame):
    for line, y in zip(lines, y_data):
        line.set_data(x[:frame], y[:frame])
    return lines

# Create the animation
ani = FuncAnimation(fig, update, frames=len(x), init_func=init, blit=True)

plt.show()