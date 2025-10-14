import random

# interpolate between data points so it can find a continuous line between each point
def interpolate(data, t):
    # restrict the range of t
    if (t < 0): t = 0
    if (t > len(data)): t = len(data)

    node = int(t)
    t = t - float(node)

    if (node == len(data) - 1):
        return data[node]
    
    a = data[node]
    b = data[node + 1]
    return a * (1 - t) + b * t

data = [random.randint(-10, 10) for _ in range(3)]

for i in range(20):
    print(interpolate(data, i / 10))