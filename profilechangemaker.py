'''

Profile Change Maker

'''

import random
import time
from changemaker import ChangeMaker

def benchmark_count_change(denoms, max_N, num_samples):
    cm = ChangeMaker(denoms)
    amounts = []
    counts = []
    times = []
    for i in range(1,num_samples):
        amount = random.randint(1, max_N)
        amounts.append(amount)
        start_time = time.time()
        num_combos = cm.count_change(amount)
        end_time = time.time()
        counts.append(num_combos)
        times.append(end_time - start_time)
    return (amounts, counts, times)

def plot(amounts, counts, times):
    import matplotlib.pyplot as plt
    fig, ax1 = plt.subplots()
    ax1.plot(amounts, counts, 'b.')
    ax1.set_xlabel('amount')
    # Make the y-axis label and tick labels match the line color.
    ax1.set_ylabel('counts', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    ax2 = ax1.twinx()
    ax2.plot(amounts, times, 'r.')
    ax2.set_ylabel('times', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.show()


us_denoms = [25, 10, 5, 1]

(amounts, counts, times) = benchmark_count_change(us_denoms, 1000, 100)
plot(amounts, counts, times)     
        
        

