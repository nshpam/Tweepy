import EX5
import unittest

class FindZeroSumUnitTest(unittest.TestCase):

    #not sorted
    def test_not_sorted(self):
        check = EX5.FindZeroSum([0,-1,2,-3,1,-2])
        assert check == '(-3, 1, 2),(-2, 0, 2),(-1, 0, 1)'

    #sorted
    def test_sorted(self):
        check = EX5.FindZeroSum([-3,-2,-1,0,1,2])
        assert check == '(-3, 1, 2),(-2, 0, 2),(-1, 0, 1)'

    #test repeat

    #not sorted
    def test_not_sorted_repeated(self):
        check = EX5.FindZeroSum([0,-1,2,-3,1,-2,-1])
        assert check == '(-3, 1, 2),(-2, 0, 2),(-1, 0, 1)'
    
    #sorted
    def test_sorted_repeated(self):
        check = EX5.FindZeroSum([-3,-2,-1,0,0,1,2])
        assert check == '(-3, 1, 2),(-2, 0, 2),(-1, 0, 1)'
    
    #all repeat
    def test_all_repeated(self):
        check = EX5.FindZeroSum([-3,-3,-3,-3,-3])
        assert check == 'There are no number that can be sum into 0.'
    
    #test data type

    #empty list
    def test_empty_list(self):
        check = EX5.FindZeroSum([])
        assert check == 'There are no number that can be sum into 0.'

    #none
    def test_none(self):
        check = EX5.FindZeroSum(None)
        assert check == 'Invalid data type'

    #invalid type
    def test_invalid_type(self):
        check = EX5.FindZeroSum('')
        assert check == 'Invalid data type'

#run this code if and only if it's the main file
if __name__ == '__main__':
    unittest.main()