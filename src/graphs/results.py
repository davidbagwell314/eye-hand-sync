import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from emc_tools import data
from emc_tools import correlation

def full_extent(ax, pad=0.0):
    """Get the full extent of an axes, including axes labels, tick labels, and
    titles."""
    # For text objects, we need to draw the figure first, otherwise the extents
    # are undefined.
    ax.figure.canvas.draw()
    items = ax.get_xticklabels() + ax.get_yticklabels() 
#    items += [ax, ax.title, ax.xaxis.label, ax.yaxis.label]
    items += [ax, ax.title]
    items += [ax.get_xaxis().get_label(), ax.get_yaxis().get_label()]
    bbox = Bbox.union([item.get_window_extent() for item in items])

    return bbox.expanded(1.0 + pad, 1.0 + pad)

if __name__ == "__main__":
    results = data.lookup("results-all.csv", reject=False, raw=True)[1:]

    participant = 3
    repetition = 1

    means = []
    for i in range(30):
        mean = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        total = 0
        for result in results:
            if result[1] == repetition and result[2] == i and result[3] == i + 1:
                mean = tuple(map(lambda x, y: x + y, mean, result))
                total += 1

        means.append(tuple(map(lambda x: x / total, mean)))

    updated_results = []
    for result in results:
        if result[0] == participant and result[1] == repetition and not(result[2] == 0 and result[3] == 30):
            updated_results.append(result)

    results = updated_results

    times = []
    m_times = []

    hand_coordination = []
    eye_coordination = []
    both_coordination = []

    hand_delay = []
    eye_delay = []
    both_delay = []

    m_hand_coordination = []
    m_eye_coordination = []
    m_both_coordination = []

    m_hand_delay = []
    m_eye_delay = []
    m_both_delay = []

    for result in results:
        times.append(result[2])

        hand_coordination.append(result[4])
        hand_delay.append(result[5])

        eye_coordination.append(result[6])
        eye_delay.append(result[7])
        
        both_coordination.append(result[8])
        both_delay.append(result[9])

    
    for result in means:
        m_times.append(result[2])

        m_hand_coordination.append(result[4])
        m_hand_delay.append(result[5])

        m_eye_coordination.append(result[6])
        m_eye_delay.append(result[7])
        
        m_both_coordination.append(result[8])
        m_both_delay.append(result[9])

    fig, axes = plt.subplots(3, dpi=1000, figsize=(6, 10))

    # coordination
    axes[0].plot(m_times, m_hand_coordination, color="green", alpha=0.25)
    axes[0].plot(m_times, m_eye_coordination, color="blue", alpha=0.25)
    axes[0].plot(m_times, m_both_coordination, color="orange", alpha=0.25)

    axes[0].plot(times, hand_coordination, color="green", label="Hand")
    axes[0].plot(times, eye_coordination, color="blue", label="Eye")
    axes[0].plot(times, both_coordination, color="orange", label="Hand vs eye")
    
    axes[0].set_xlim(0, 30)
    axes[0].set_ylim(0, 100)

    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Coordination (%)")

    axes[0].set_title("Coordination")

    axes[0].legend()

    # time delay
    axes[1].plot(m_times, m_hand_delay, color="green", alpha=0.25)
    axes[1].plot(m_times, m_eye_delay, color="blue", alpha=0.25)
    axes[1].plot(m_times, m_both_delay, color="orange", alpha=0.25)

    axes[1].plot(times, hand_delay, color="green", label="Hand vs target")
    axes[1].plot(times, eye_delay, color="blue", label="Eye vs target")
    axes[1].plot(times, both_delay, color="orange", label="Hand vs eye")

    axes[1].set_xlim(0, 30)
    axes[1].set_ylim(0, 300)

    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Time delay (ms)")

    axes[1].set_title("Time delay")

    axes[1].legend()

    # save figures

    fig.tight_layout()

    extent = full_extent(axes[0], 0.1).transformed(fig.dpi_scale_trans.inverted())
    fig.savefig('graphs/coordination.png', bbox_inches=extent)
    
    extent = full_extent(axes[1], 0.1).transformed(fig.dpi_scale_trans.inverted())
    fig.savefig('graphs/time-delay.png', bbox_inches=extent)