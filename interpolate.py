def search(data, value):
    first = data[0]
    last = data[-1]
    
    idx = int((value - first) / (last - first) * len(data))

    if idx < 0:
        return 0
    if idx > len(data) - 1:
        return len(data) - 1

    if data[idx] == value:
        return idx
    elif data[idx] > value:
        while data[idx] > value:
            idx -= 1

        return idx
    else:
        while data[idx] < value:
            idx += 1

        return idx - 1

# interpolate between data points so it can find a continuous line between each point
def interpolate(data, time, t):
    time_idx = search(time, t)

    if time_idx < 0:
        return data[0]
    
    if time_idx > len(time) - 1:
        return data[-1]

    time_val = time[time_idx]
    time_next = time[time_idx + 1]

    ratio = (t - time_val) / (time_next - time_val)

    return data[time_idx] * (1 - ratio) + data[time_idx + 1] * ratio


if __name__ == "__main__":
    import data

    d: list[data.Data] = data.lookup("csv_data/tracking/tracking_r1_prt_1.csv", reject=False)

    time: list[float] = []
    target: list[data.Pos] = []
    hand: list[data.Pos] = []
    eye: list[data.Pos] = []

    # read the data into the lists and convert ranges to -1 to 1 for easier processing
    for val in d:
        time.append(val.time)
        target.append(val.target * 2 - (1, 1))
        hand.append(val.hand * 2 - (1, 1))
        eye.append(val.eye * 2 - (1, 1))

    print(interpolate(target, time, 1.3))