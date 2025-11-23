import os
import matplotlib.pyplot as plt

from emc_tools import data
from emc_tools import correlation

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

        updated_results = []
        for result in results:
            if result[0] == 5 and not(result[2] == 0 and result[3] == 30) and result[5] < 2000 and result[5] > -2000  and result[7] < 2000 and result[7] > -2000  and result[9] < 2000 and result[9] > -2000:
                print(result)
                updated_results.append(result)

        results = updated_results

        x = []
        y = []

        for result in results:
            x.append(result[4])
            y.append(result[5])

        plt.scatter(x, y)
        
        x = []
        y = []

        for result in results:
            x.append(result[6])
            y.append(result[7])

        plt.scatter(x, y)
        
        x = []
        y = []

        for result in results:
            x.append(result[8])
            y.append(result[9])

        plt.scatter(x, y)
        plt.grid()
        plt.xlim(30, 80)
        plt.ylim(-500, 500)
        plt.savefig("graphs/all-data.png")