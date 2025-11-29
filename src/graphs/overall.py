import numpy as np
import matplotlib.pyplot as plt
from scipy import stats 

from emc_tools import data
from emc_tools import correlation

def plot_stats(x, y, points=True, mean=False, linregress=False, color='', label=''):
    if points:
        plt.scatter(x, y, color=color, label=label)

    if mean:
        mx = np.mean(x)
        my = np.mean(y)
        plt.plot(mx, my, color=color, marker='o', ms=10, mew=3, mfc='white')
        mx = np.round(mx, decimals=1)
        my = np.round(my)
        print(f"{label} mean:\n\tCoordination: {mx}%\n\tTime delay: {my}ms")

    if linregress:
        gradient, intercept,r,p,st_err = stats.linregress(x, y)

        line = [gradient * px + intercept for px in x]

        plt.plot(x, line, color=color, alpha=0.5)

    m = 0.0
    m_i = 0
    for i, p in enumerate(x):
        if p > m:
            m = p
            m_i = i

    print(x[m_i], y[m_i])
    

if __name__ == "__main__":
    if False:
        print("participant,repetition,start time,end time,hand coordination,hand delay,eye coordination,eye delay,overall coordination,overall delay")
        for participant in range(1, 12):
            for repetition in range(1, 6):
                d: list[data.Data] = data.lookup(f"data/tracking/tracking_r{repetition}_prt_{participant}.csv", reject=True)

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

                start_time = [i for i in range(30)]
                end_time = [i + 1 for i in range(30)]

                start_time += [10 * i for i in range(3)]
                end_time += [10 * i + 10 for i in range(3)]

                start_time.append(0)
                end_time.append(30)

                for i in range(len(start_time)):
                    start = start_time[i]
                    end = end_time[i]

                    s_hand = correlation.get_similarity(start, end, time, target, hand, include_positives=True)
                    s_eye = correlation.get_similarity(start, end, time, target, eye, include_positives=True)
                    s_both = correlation.get_similarity(start, end, time, hand, eye, include_positives=True)

                    print(f"{participant},{repetition},{start},{end},{s_hand[0] * 100},{-s_hand[1] * 1000},{s_eye[0] * 100},{-s_eye[1] * 1000},{s_both[0] * 100},{s_both[1] * 1000}")

    else:
        results = data.lookup("results-all.csv", raw=True)[1:]

        hand = True
        eye = True
        both = True

        mean = True
        linregress = True

        start_time = 0
        end_time = 30
        intervals = [1, 10, 30]

        remove_results = []

        updated_results = []
        for result in results:
            if result[5] < 2000 and result[5] > -2000  and result[7] < 2000 and result[7] > -2000  and result[9] < 2000 and result[9] > -2000: # remove outliers
                if intervals == [] or (result[3] - result[2] in intervals and result[2] >= start_time and result[3] <= end_time):
                    updated_results.append(result)
            elif not (result[0], result[1]) in remove_results:
                remove_results.append((result[0], result[1]))

        results = updated_results
        updated_results = []
        for result in results:
            if not (result[0], result[1]) in remove_results:
                updated_results.append(result)

        results = updated_results

        if hand:
            x = []
            y = []

            for result in results:
                x.append(result[4])
                y.append(result[5])

            plot_stats(x, y, color="tab:green", label="Hand", mean=mean, linregress=linregress)
        
        if eye:
            x = []
            y = []

            for result in results:
                x.append(result[6])
                y.append(result[7])

            plot_stats(x, y, color="tab:blue", label="Eye", mean=mean, linregress=linregress)
        
        if both:
            x = []
            y = []

            for result in results:
                x.append(result[8])
                y.append(result[9])

            plot_stats(x, y, color="tab:orange", label="Hand vs eye", mean=mean, linregress=linregress)

        plt.grid()
        plt.legend()

        name = ""

        if hand and eye and both:
            name = "all"
        elif hand and eye:
            name = "hand-and-eye"
        elif hand and both:
            name = "hand-and-hand-vs-eye"
        elif eye and both:
            name = "eye-and-hand-vs-eye"
        elif hand:
            name = "hand"
        elif eye:
            name = "eye"
        else:
            name = "hand-vs-eye"

        plt.savefig(f"graphs/{name}-data-{start_time}-{end_time}s-group{intervals}.png")