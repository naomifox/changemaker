'''

Benchmark ChangeMaker performance

Author: Naomi Fox <naomi.fox@gmail.com>
Date: August 12, 2014

'''

import random
import time
from changemaker import ChangeMaker
import matplotlib.pyplot as plt

def benchmark_count_change(denoms, max_N, num_samples):
    '''
    Collect number of combinatiosn and sames

    returns a tuple of three lists:
    1. amounts - input amount
    2. counts - number of change combinations
    3. times - actual run time, in seconds
    '''
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
    '''
    Creates a scatter plot showing:
    - amount vs. # combinations
    - amount vs. running time

    params amounts, counts, and times
    should all be of the same length
    '''  
    fig, ax1 = plt.subplots()
    ax1.plot(amounts, counts, 'b.')
    ax1.set_xlabel('amount')
    ax1.set_ylabel('combinations', color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    ax2 = ax1.twinx()
    ax2.plot(amounts, times, 'r.')
    ax2.set_ylabel('time (s)', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.show()


if __name__ == '__main__':
    '''
    Main 
    Collect samples from running ChangeMaker
    with US denominations on 100 amounts
    uniformly sampled from [1, 200]
    '''
    us_denoms = [25, 10, 5, 1]
    (amounts, counts, times) = benchmark_count_change(us_denoms, 500, 100)
    plot(amounts, counts, times)     
        
        

