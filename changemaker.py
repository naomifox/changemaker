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
        '''
        self.coin_denoms = coin_denoms

    def fill_table(self, amount):
        '''
        Memoization table for dynamic programming solution.
        table has 1 row, and N columns
        table[i]: contains a list of coin denominations that could be added
                  to previously computed values in table in order to
                  make up the amount, or None if its not possible
                  with the provided denominations.

        Running time: O(C * N)
        Contains a nested for loop
        that checks C coin denominations for every
        intermediate amount in [1, N]

        Space: O(C * N)
        This method fills in a 1 x N table, but every
        cell can contain a list of O(C) coin denominations.
        '''
        # initialize table with None for all values
        table = [None for i in range(1, amount + 1)]
        for i in range(1, amount + 1):
            for coin_val in self.coin_denoms:
                if coin_val > i:
                    continue
                if coin_val == i or table[i - coin_val - 1] is not None:
                    # add the coin
                    if table[i - 1] is None:
                        table[i - 1] = []
                    table[i - 1].append(coin_val)
        return table

    def get_combinations(self, table, amount):
        '''
        Recursive method to retrieve all coin combinations
        for making change.

        Just performs DFS to traverse all possible paths.

        Assumption: table was created by fill_table
        and it has a solution

        Each combination will be in order, from largest to smallest
        coin denomination

        Running time: O(C * N^2)
        This implements a DFS-like graph traversal.  There are at most
        N 'nodes' / table cells, but nodes may be visited multiple times.
        Each node stores at most O(C) values, so therefore,
        at most C children must be visited from each node.
        Since we are doing list concatenation at each step,
        that requires time linear in the size of the list, where
        the list size is O(N).

        Space: O(N^2)
        Stores all possible change combinations as a separate list of
        values, with no compression.
        The number of combinations is O(N), and each might contain as
        many as N separate values.

        Notes:
        To save time:
        - could memoize intermediate combinations
        - use chaining, or some other data structure, rather than list concatenation
        To save space:
        - could store frequency counts, as opposed to each
        value separately, possibly using collections.Counter class.
        - could change method to a generator, as opposed to just
        returning a list of lists
        '''
        combos = None
        if amount > 0:
            combos = []
            for coin_val in table[amount - 1]:
                combos2 = self.get_combinations(table, amount - coin_val)
                if not combos2:
                    combos += [[coin_val]]
                else:
                    combos += [c + [coin_val] for c in combos2 if c[-1] >= coin_val]
        return combos

    def change(self, amount):
        '''
        Get all possible sets of change that could be
        used.

        Calls the fill_table() and get_combination() methods

        Running time: O(C * N^2)
        Space: O(N^2)
        '''
        table = self.fill_table(amount)
        if table[-1] is None:  # no solution
            return None
        combinations = self.get_combinations(table, amount)
        return combinations

    def count_change(self, amount):
        '''
        Get the number of all combinations
        of coins for making change

        Calls the change() method

        Running time: O(C * N^2)
        Space: O(N^2)

        Note: could save space by not
        actually storing all the combinations
        '''
        combinations = self.change(amount)
        if not combinations:
            return 0
        else:
            return len(combinations)


class TestChangeMaker(unittest.TestCase):
    '''
    Class to test ChangeMaker class
    '''
    def test_fill_table_1(self):
        '''
        Simple test for fill_table()
        Checks case where only a penny change is needed
        '''
        cm = ChangeMaker([25, 10, 5, 1])
        table = cm.fill_table(1)
        self.assertEqual(len(table), 1)
        self.assertEqual(table[0], [1])

    def test_fill_table_2(self):
        '''
        Another simple test for fill_table()
        Checks case where 10 cents change is needed
        '''
        cm = ChangeMaker([25, 10, 5, 1])
        table = cm.fill_table(10)
        self.assertEqual(len(table), 10)
        self.assertEqual(len(table[0]), 1)
        self.assertEqual(len(table[9]), 3)

    def test_get_combinations(self):
        '''
        Test get_combinations()
        '''
        cm = ChangeMaker([])
        table = [[1], [1], [1], [1], [5, 1], [5, 1], [5, 1], [5, 1], [5, 1], [10, 5, 1]]
        combinations = cm.get_combinations(table, 10)
        self.assertEquals(len(combinations), 4)

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
        None
        '''
        cm = ChangeMaker([5])
        combinations = cm.change(5)
        self.assertEqual(len(combinations), 1)
        combinations = cm.change(1)
        self.assertEqual(combinations, None)

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
        answer = [[4, 3, 3], [7, 3], [5, 5]]
        for combo in answer:
            self.assertTrue(combo in combinations)

        combinations = cm.change(7)
        self.assertEqual(len(combinations), 2)
        answer = [[4, 3], [7]]
        for combo in answer:
            self.assertTrue(combo in combinations)

        cm = ChangeMaker([7, 5, 3, 4])
        combinations = cm.change(7)
        self.assertEqual(len(combinations), 2)
        answer = [[4, 3], [7]]
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
        self.assertEquals(num_coins, 0)

    def test_change_scale(self):
        '''
        Test how change() scales.
        Run on worst possible case where there
        is a denomination for every integer value.
        '''
        import time
        startTime = time.time()
        denoms = xrange(1, 20)
        cm = ChangeMaker(denoms)
        combinations = cm.change(20)
        endTime = time.time()
        print startTime
        print endTime
        self.assertTrue(endTime - startTime < 20 * 20 * 20)
        print len(combinations)


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

    Change count:
    1: 3 x 1, 1 x 5
    2: 8 x 1

    '''
    coin_denoms = [int(w) for w in raw_input().split()]
    amount = int(raw_input())
    return (coin_denoms, amount)


def combination_to_str(combination):
    '''
    Convert a combination, as a list of integers, to
    a string representation.

    For example: [3, 1, 1, 1, 1, 1]
    becomes: "3 x 1, 1 x 5"
    '''
    counter = collections.Counter(combination)
    outstr = ""
    for k in counter:
        outstr += "%d x %d, " % (counter[k], k)
    return outstr[:-2]  # cut off the trailing comma


def print_output(combinations):
    '''
    Print all combinations with combination_to_str()
    '''
    print "Change count:"
    if combinations is None:
        print "No solution"
        return
    for (i, combination) in enumerate(combinations):
        print str(i + 1) + ": " + combination_to_str(combination)

if __name__ == '__main__':
    '''
    Main method
    See README file for instructions
    '''
    (coin_denoms, amount) = parse_input()
    cm = ChangeMaker(coin_denoms)
    combinations = cm.change(amount)
    print_output(combinations)
