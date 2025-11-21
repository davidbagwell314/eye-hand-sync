from emc_tools import data, interpolate

def correlation(x: float, t: list[float], f: list[data.Pos], g: list[data.Pos]) -> float:
    if not (len(t) == len(f ) and len(t) == len(g)):
        raise Exception("Cannot cross-correlate with arrays of different lengths")
    
    sum: float = 0.0

    for i in range(len(t) - 1):
            dt = t[i + 1] - t[i]

            f_val = interpolate.interpolate(f, t[i], t)
            g_val = interpolate.interpolate(g, t[i] - x, t)

            prod = data.similarity(f_val, g_val) # between 0 and infinity, smaller values mean points are closer together

            sum += prod * dt
            
    return sum

def get_similarity(start_time: float, end_time: float, t:list[float], f: list[data.Pos], g: list[data.Pos]):
    time_delay = -0.5

    time_range = 0.5 # time range to sample in seconds
    dt = 0.1
    
    results = []

    start_idx = interpolate.search(t, start_time)
    end_idx = interpolate.search(t, end_time) + 1

    for i in range(4):
        time_offsets: list[float] = [time_delay + dt * j for j in range(-int(time_range / dt), int(time_range / dt))]
        min_correlation = 10000

        for x in time_offsets:
            result = correlation(x, t[start_idx:end_idx], f[start_idx:end_idx], g[start_idx:end_idx])

            # find the time offset with the biggest correlation - this is the delay between signals
            if result < min_correlation:
                min_correlation = result
                time_delay = x

            results.append(result)

        time_range *= 0.1
        dt *= 0.1

    result = correlation(time_delay, t, f, g)
    result = 2.0 / (2.0 + (result / (end_time - start_time)) ** 0.5)
    return (result, time_delay)


if __name__ == "__main__":
    d: list[data.Data] = data.lookup("data/tracking/tracking_r1_prt_3.csv", reject=True)

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

    if False:
        time_range = 0.5 # time range to sample in seconds
        dt = 0.005

        t = [dt * i for i in range(-int(time_range / dt), int(time_range / dt))]
        r1 = get_similarity(time, target, target)[2]
        r2 = get_similarity(time, target, hand)[2]
        r3 = get_similarity(time, target, eye)[2]

        print("time,target,hand,eye")
        for i in range(len(t)):
            print(t[i],r1[i], r2[i], r3[i], sep=',')

    else:
        start_time = 0
        end_time = 1

        s_hand = get_similarity(start_time, end_time, time, target, hand)
        s_eye = get_similarity(start_time, end_time, time, target, eye)

        print(f"Cross-correlation results between {start_time}s and {end_time}s")
        print(f"Hand vs target:\n\tCorrelation: {int(s_hand[0] * 1000) / 10}%, Mean time delay: {int(-s_hand[1] * 1000)}ms")
        print(f"Eye vs target:\n\tCorrelation: {int(s_eye[0] * 1000) / 10}%, Mean time delay: {int(-s_eye[1] * 1000)}ms")