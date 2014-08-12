'''
Change Maker.

Makin' change

Author: Naomi Fox <naomi.fox@gmail.com>
Date: August 1, 2014

'''

import unittest
import collections


class ChangeMaker:
    '''
    Class to compute all the ways to make change
    from some set of coin denominations.

    The time and space requirements for each method
    are included in the documentation.

    Constants:
    N: amount for which to "make change"
    C: number of coin denominations
    '''
    def __init__(self, coin_denoms):
        '''
        Initialize coin_denoms

        Running time: O(C)
        Space: O(C)
        '''
        self.coin_denoms = coin_denoms

    def fill_table(self, amount):
        '''
        Returns memoization table for dynamic programming solution.
        table has 1 row, and N columns
        table[i]: contains all combinations of coin_vals that can add up to i + 1
                
        Running time: O(C * N ^ (C + 2)))
        Contains a nested for loop
        that checks C coin denominations for every
        amount in [1, N].
        For each coin denom that is found
        to be viable, O(C^N) lists are copied into
        the current cell.
        C^N: combination of N items drawn from 
        C possible values, with replacement).  
        Each list may have length O(N).
        
        Space: O(N ^ (C + 2))
        This method fills in a 1 x N table.
        Every cell can hold O(C^N) lists of possible combinations
        (combination with replacement).
        The length of each list is O(N) (worst case is all pennies).

        Notes: Could save time and space by saving combinations in a
        more compact representation.
        '''
        # initialize table with empty list for all values in [1, amount]
        table = [[] for i in range(1, amount + 1)]
        for i in range(1, amount + 1):
            for coin_val in self.coin_denoms:
                if coin_val == i:
                    table[i - 1].append([coin_val])
                elif coin_val < i and table[i - coin_val - 1]:
                    table[i - 1].extend([c + [coin_val] for c in table[i - 1 - coin_val] if c[-1] <= coin_val])
        return table

    def change(self, amount):
        '''
        Get all possible sets of change that could be
        used.

        Calls the fill_table() method

        Running time: see fill_table()
        Space: see fill_table()
        '''
        table = self.fill_table(amount)
        return table[-1]

    def count_change(self, amount):
        '''
        Get the number of all combinations
        of coins for making change.
        Will return 0 if there is no solution.

        Calls the fill_table() method

        Running time: see fill_table()
        Space: see fill_table()

        '''
        table = self.fill_table(amount)
        return len(table[-1])


class TestChangeMaker(unittest.TestCase):
    '''
    Class to test ChangeMaker class
    '''
    def test_fill_table(self):
        '''
        Simple test for fill_table()
        Checks case where only a penny change is needed
        '''
        cm = ChangeMaker([25, 10, 5, 1])
        table = cm.fill_table(1)
        self.assertEqual(len(table), 1)
        table = cm.fill_table(10)
        self.assertEqual(len(table), 10)
        self.assertEqual(len(table[9]), 4)  # 4 combinations possible to make 10
        self.assertEqual(len(table[8]), 2)  # 2 combinations possible to make 9

    def test_change_1(self):
        '''
        Test change(), using US coins
        >>> cm = ChangeMaker([25, 10, 5, 1])
        >>> cm.change(8)
        [[5, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
        '''
        cm = ChangeMaker([25, 10, 5, 1])
        combinations = cm.change(8)
        self.assertEqual(len(combinations), 2)
        self.assertEqual(len(combinations[0]), 4)
        self.assertEqual(len(combinations[1]), 8)

    def test_change_2(self):
        '''
        Test change() for simplest case where only one denomination
        is available.
        >>> cm = ChangeMaker([5])
        >>> cm.change(5)
        [[5]]
        >>> cm.change(1)
        []
        '''
        cm = ChangeMaker([5])
        combinations = cm.change(5)
        self.assertEqual(len(combinations), 1)
        combinations = cm.change(1)
        self.assertFalse(combinations)  # no solution

    def test_change_3(self):
        '''
        Test change() on non-trivial example
        where greedy algorithm does not suffice
        >>> cm = ChangeMaker([3, 4, 5, 7])
        >>> cm.change(10)
        [[4, 3, 3], [7, 3], [5, 5]]
        >>> cm.change(1)
        None
        '''
        cm = ChangeMaker([3, 4, 5, 7])
        combinations = cm.change(10)
        self.assertEqual(len(combinations), 3)
        answer = [[3, 3, 4], [5, 5], [3, 7]]
        for combo in answer:
            self.assertTrue(combo in combinations)

        combinations = cm.change(7)
        self.assertEqual(len(combinations), 2)
        answer = [[3, 4], [7]]
        for combo in answer:
            self.assertTrue(combo in combinations)

        cm = ChangeMaker([7, 5, 3, 4])
        combinations = cm.change(7)
        self.assertEqual(len(combinations), 2)
        answer = [[3, 4], [7]]
        for combo in answer:
            self.assertTrue(combo in combinations)

    def test_count_change(self):
        '''
        Test count_change()
        '''
        cm = ChangeMaker([2, 1])
        num_coins = cm.count_change(3)
        self.assertEquals(num_coins, 2)

        cm = ChangeMaker([2])
        num_coins = cm.count_change(2)
        self.assertEquals(num_coins, 1)
        num_coins = cm.count_change(1)  
        self.assertFalse(num_coins)

        cm = ChangeMaker([25, 10, 5, 1])
        combinations = cm.change(7)
        numcombinations = cm.count_change(7)
        self.assertEquals(len(combinations), numcombinations)
        combinations = cm.change(52)
        numcombinations = cm.count_change(52)
        self.assertEquals(len(combinations), numcombinations)

    def test_change_scale_1(self):
        '''
        Test how change() scales.
        Run on worst possible case where there
        is a denomination for every integer value.
        '''
        import time
        start_time = time.time()
        denoms = xrange(1, 20)
        cm = ChangeMaker(denoms)
        combinations = cm.change(20)
        end_time = time.time()
        self.assertTrue(end_time - start_time < .01)

    def test_change_scale_2(self):
        '''
        Test how change() for US denoms,
        for large N.
        '''
        import time
        start_time = time.time()
        cm = ChangeMaker([1, 5, 10, 25])
        combinations = cm.change(200)
        end_time = time.time()
        self.assertTrue(end_time - start_time, .01)

        
def parse_input():
    '''
    Input Format:
    Line 1: space-delimited coin denominations
    Line 2: 0 or positive integer amount to be changed into coins

    Output Format:
    All combinations

    Sample Input 1:
    25 10 5
    8

    Sample Output 1:
    No solution

    Sample Input 2:
    25 10 5 1
    8
    '''
    coin_denoms = [int(w) for w in raw_input().split()]
    amount = int(raw_input())
    return (coin_denoms, amount)


def combination_to_str(combination):
    '''
    Convert a combination, as a list of integers, to
    a string representation.

    For example: [3, 1, 1, 1, 1, 1]
    becomes: "(3 x 1) + (1 x 5)"
    '''
    counter = collections.Counter(combination)
    outstr = ""
    keys = sorted(counter.keys())
    for k in keys:
        outstr += "(%d x %d) + " % (counter[k], k)
    return outstr[:-3]  # strip off the trailing ' + '


def print_output(combinations):
    '''
    Print all combinations with combination_to_str()
    '''
    print "Change count:"
    if not combinations:
        print "No solution"
        return
    for (i, combination) in enumerate(combinations):
        print str(i + 1) + ": " + combination_to_str(combination)

if __name__ == '__main__':
    '''
    Main
    See README file for instructions
    '''
    (coin_denoms, amount) = parse_input()
    cm = ChangeMaker(coin_denoms)
    combinations = cm.change(amount)
    print_output(combinations)
