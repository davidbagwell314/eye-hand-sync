def interpolation_search(data: list, lower: int, upper: int, value) -> int:
    if value < data[lower]:
        return lower
    
    elif value > data[upper]:
        return upper
    
    elif data[lower + 1] > value and data[lower] <= value:
        return lower
    
    else:
        pos = int(lower + ((upper - lower) // (data[upper] - data[lower]) * (value - data[lower])))

        if data[pos] == value:
            return pos

        # If x is larger, x is in right subarray
        if data[pos] < value:
            return interpolation_search(data, pos + 1,
                                       upper, value)

        # If x is smaller, x is in left subarray
        if data[pos] > value:
            return interpolation_search(data, lower,
                                       pos - 1, value)
        
        return -1

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

    return data[time_idx] * (1 - ratio) + data[time_idx + 1] * ratio


if __name__ == "__main__":
    from emc_tools import data

    d: list[data.Data] = data.lookup("data/tracking/tracking_r1_prt_1.csv", reject=False)

    time: list[float] = []
    target: list[data.Pos] = []
    hand: list[data.Pos] = []
    eye: list[data.Pos] = []

    # read the data into the lists and convert ranges to -1 to 1 for easier processing
    for val in d:
        time.append(val.time)
        target.append(val.target)# * 2 - (1, 1))
        hand.append(val.hand)# * 2 - (1, 1))
        eye.append(val.eye)# * 2 - (1, 1))

    print(interpolate(target, 1.3, time))