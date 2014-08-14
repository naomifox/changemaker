'''
Change Maker.

Makin' change

Author: Naomi Fox <naomi.fox@gmail.com>
Date: August 1, 2014, August 14, 2014

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
        Initialize coin_denoms, which is a
        list of coin denominations.
        For example:
        >>> cm = ChangeMaker([25, 10, 5, 1])

        Running time: O(C log C)
        Sorts coin_denoms
        
        Space: O(C)
        Stores list of coin denominations
        '''
        self.coin_denoms = coin_denoms
        self.coin_denoms.sort()

    def fill_table(self, amount):
        '''
        Returns memoization table for dynamic programming solution.
        table has 1 row, and N columns.
        
        table[i]: contains a list of coin denominations that could be added
                  to previously computed values in table in order to
                  make up the amount, or None if its not possible
                  with the provided denominations.

        Running time: O(C * N)
        Method contains a nested for loop
        that checks C coin denominations for every
        intermediate amount in [1, N]

        Space: O(C * N)
        This method fills in a 1 x N table, but every
        cell contains a list of O(C) coin denominations.
        '''
        table = [[] for i in range(1, amount + 1)]
        for i in range(1, amount + 1):
            for coin_val in self.coin_denoms:
                if coin_val == i:
                    table[i - 1].append(coin_val)
                elif coin_val < i and table[i - coin_val - 1] and table[i - coin_val - 1][0] <= coin_val:
                    table[i - 1].append(coin_val)
        return table

    class vertex:
        '''
        Vertex class used in get_combo_graph() method.
        Used in auxiliary graph for quickly retrieving all
        combinations. The graph uses an adjacency list
        representation.
        '''
        def __init__(self, coin_val, children):
            '''
            Initialize vertex with coin_val
            Running time: O(C)
            Space: O(C) 
            '''
            self.coin_val = coin_val
            self.children = children

        def __repr__(self):
            '''
            string representation for debugging
            '''
            out_str = 'coin_val: %d children: [' % self.coin_val
            for v2 in self.children:
                out_str += '%d, ' % v2.coin_val
            out_str += ']'
            return out_str

    def get_combo_graph(self, table):
        '''
        Returns a DAG that can be 
        traversed in order to generate
        all possible combinations from the table.

        This method is called by get_combinations().

        Returns a list of lists of vertices
        The last vertex list are the tree "roots".

        Running time: O(N * C^2)
        Iterates over table, from [1, N]
        and checks each coin_val in cell (O(C))
        For each coin_val it finds, collects all
        O(C) "children", which were vertices
        generated previous from table[i - 1 - coin_val].

        Space: O(N * C^2)
        There can be at most N * C vertices.
        Each vertex stores a list of O(C) children.
        '''
        amount = len(table)
        vertices = []
        for i in range(1, amount + 1):
            vertices.append([])
            for coin_val in table[i - 1]:
                if i == coin_val:
                    children = []
                else:
                    children = [v2 for v2 in vertices[i - 1 - coin_val] if v2.coin_val <= coin_val]
                vertices[i - 1].append(self.vertex(coin_val, children))
        return vertices

    def search_combo_graph(self, v):
        '''
        Peforms a DFS-type traversal on the auxiliary graph
        to collect all combinations.

        Running time: O(N^2 * C)
        This implements a DFS-like graph traversal.  
        There are at most N vertices, but vertices may be visited 
        multiple times.  Each vertex has at most O(C) children, 
        so therefore, at most C children must be visited from each node,
        Each time a vertex is visited, a list
        of length O(N) must be copied for each child.

        Space: O(C ^ N)
        Saves all possible combinations (as lists) into a list.

        Note:
        Looked into caching combos in the vertex to prevent
        multiple visits to the same vertex, but found this didn't 
        improve performance sufficiently using profile_changemaker.py
        '''
        combos = []
        if not v.children:
            combos = [[v.coin_val]]
        else:
            for v2 in v.children:
                short_combos = self.search_combo_graph(v2)
                combos.extend([[v.coin_val] + short_combo for short_combo in short_combos])
        return combos

    def get_combinations(self, table):
        '''
        Returns a list of combinations, each combination 
        is stored in  a list.

        The input is a table output by fill_table().
        
        Calls get_combo_graph() to create
        an auxiliary graph based on the table.
        Then calls search_combo_graph() to perform DFS-type
        searches of the graph.
        
        Running time: See fill_table() and get_combo_graph()
        Space: See fill_table() and get_combo_graph()
        '''
        vertex_lists = self.get_combo_graph(table)
        combinations = []
        for v in vertex_lists[-1]:
            combinations.extend([c for c in self.search_combo_graph(v)])
        return combinations

    def get_num_combinations(self, table, amount, last_coin_val=None):
        '''
        Recursive method to count the number of combinations for making change
        for some amount.

        Parameter table was produced from output of fill_table()
        Parameter last_coin_val is used so we don't get duplicate combinations
        that are just permutations

        Returns None if no solution is found, otherwise returns number
        of possible combinations

        This method is called by count_change().

        Running time: O(C * N)
        This implements a DFS-like graph traversal.  
        There are at most N 'nodes' / table cells, but nodes may be visited 
        multiple times.  Each node stores at most O(C) values, 
        so therefore, at most C children must be visited from each node.

        Space: O(1)
        Does not store anything beyond the count of combinations for
        each amount, recursively.
        Since the method is recursive, the call stack might grow O(N) long in
        the worst case.
        '''
        num_combos = 0
        if last_coin_val is None:
            last_coin_val = amount
        if amount == 0:
            return 0
        if not table[amount - 1]:
            return None  # No solution
        next_coin_vals = table[amount - 1]
        for coin_val in [c for c in next_coin_vals if c <= last_coin_val]:
            if coin_val == amount:
                num_combos += 1
            else:
                num_combos += self.get_num_combinations(table, amount - coin_val, coin_val)
        return num_combos

    def change(self, amount):
        '''
        Get all possible sets of change that could be
        used.

        Calls the fill_table() and get_combinations() methods

        Running time: O(C * N^2)
        Space: O(N^2)
        '''
        table = self.fill_table(amount)
        if not table[-1]:  # no solution
            return None
        combinations = self.get_combinations(table)
        return combinations

    def count_change(self, amount):
        '''
        Get the number of all combinations
        of coins for making change

        Calls fill_table() and get_num_combinations()

        Running time: O(C * N^2)
        Space: See fill_table()
        '''
        table = self.fill_table(amount)
        if not table[-1]:  # no solution
            return None
        return self.get_num_combinations(table, amount)


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

    def test_get_combo_graph(self):
        '''
        test get_combo_graph
        for small example
        '''
        cm = ChangeMaker([25, 10, 5, 1])
        table = cm.fill_table(10)
        vertices = cm.get_combo_graph(table)
        self.assertEquals(len(vertices), len(table))
        n = sum([len(v_list) for v_list in vertices])
        self.assertEquals(n, 17)

    def test_get_combinations(self):
        '''
        Test get_combinations()
        '''
        cm = ChangeMaker([])
        table = [[1], [1], [1], [1], [5, 1], [5, 1], [5, 1], [5, 1], [5, 1], [10, 5, 1]]
        vertices = cm.get_combo_graph(table)
        combinations = cm.get_combinations(table)
        self.assertEquals(len(combinations), 4)

    def test_change_1(self):
        '''
        Test change(), using US coins
        >>> cm = ChangeMaker([25, 10, 5, 1])
        >>> cm.change(8)
        [[1, 1, 1, 5], [1, 1, 1, 1, 1, 1, 1, 1]]
        '''
        cm = ChangeMaker([25, 10, 5, 1])
        combinations = cm.change(8)
        self.assertEqual(len(combinations), 2)
        self.assertTrue([5, 1, 1, 1] in combinations)
        self.assertTrue([1, 1, 1, 1, 1, 1, 1, 1] in combinations)

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
        num_coins = cm.count_change(1)  # should return None
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
        denoms = range(1, 20)
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
