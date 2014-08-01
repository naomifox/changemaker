'''
Change Maker

'''

import unittest

class ChangeMaker:
    '''
    Class to compute all the ways to make change
    '''

    def __init__(self, coin_denoms):
        '''
        Initialize coin_denoms
        '''
        self.coin_denoms = coin_denoms

    def change(self, amount):
        '''
        Get all possible sets of change that could be 
        used
        '''
        return None

    def count_change(self, amount):
        '''
        Get the number of all combinations
        of coins for making change
        '''
        return None

class TestChangeMaker(unittest.TestCase):

    def test_change_1(self):
        '''
        >>> cm = ChangeMaker([25, 10, 5, 1])
        >>> cm.change(8)
        [[5, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
        '''
        cm = ChangeMaker([25, 10, 5, 1])
        combinations = cm.change(8)
        self.assertEqual(len(combinations), 2)
        self.assertEqual(len(combinations[0]), 4)
        self.assertEqual(len(combinations[1]), 8)


if __name__ == '__main__':
    unittest.main()


                
        
        
        
