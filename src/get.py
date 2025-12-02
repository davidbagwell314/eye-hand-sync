from emc_tools import data

if __name__ == "__main__":
    results = data.lookup("results-all.csv", raw=True)[1:]
    for x in [(0, 1), (0, 10), (10, 20), (20, 30)]:
        print(f"{x[0]}-{x[1]}s:")
        for result in results:
            if result[2] == x[0] and result[3] == x[1] and result[1] == 1 and result[0] in [1, 2, 6]:
                print(f"\tparticipant {result[0]}, repetition {result[1]}:", (result[5]))