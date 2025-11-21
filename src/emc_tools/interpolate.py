def interpolation_search(data: list, lower: int, upper: int, value) -> int:
    pos: int = int(lower + ((upper - lower) / (data[upper] - data[lower]) * (value - data[lower])))

    if pos <= lower:
        return lower
    
    if pos >= upper:
        return upper
    
    """print(data[lower:upper+1])
    print(' ' * (len(str(data[0:pos])) + 1) + '^')"""

    if value < data[pos]:
        return interpolation_search(data, lower, pos, value)
    
    elif value > data[pos]:
        return interpolation_search(data, pos, upper, value)
    
    else:
        return pos

def search(data, value):
    return interpolation_search(data, 0, len(data) - 1, value)

# interpolate between data points so it can find a continuous line between each point
def interpolate(data: list, t, time: list = []):
    time_idx = int(t)
    if len(time) > 0:
        time_idx = search(time, t)

    if time_idx < 0:
        return data[0]
    
    if time_idx >= len(time) - 1:
        return data[-1]

    time_val = time[time_idx]
    time_next = time[time_idx + 1]

    ratio = (t - time_val) / (time_next - time_val)

    if ratio < 0:
        ratio = 0

    if ratio > 1:
        ratio = 1

    return data[time_idx] * (1 - ratio) + data[time_idx + 1] * ratio
