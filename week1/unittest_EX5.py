import EX5
import unittest

class FindZeroSumUnitTest(unittest.TestCase):

    #test sorted and not sorted
    def test_not_sorted(self):
        check = EX5.FindZeroSum([0,-1,2,-3,1,-2])
        assert check == '(-3, 1, 2),(-2, 0, 2),(-1, 0, 1)'
    def test_sorted(self):
        check = EX5.FindZeroSum([-3,-2,-1,0,1,2])
        assert check == '(-3, 1, 2),(-2, 0, 2),(-1, 0, 1)'

    #test repeat
    def test_not_sorted_repeated(self):
        check = EX5.FindZeroSum([0,-1,2,-3,1,-2,-1])
        assert check == '(-3, 1, 2),(-2, 0, 2),(-1, 0, 1)'
    def test_sorted_repeated(self):
        check = EX5.FindZeroSum([-3,-2,-1,0,0,1,2])
        assert check == '(-3, 1, 2),(-2, 0, 2),(-1, 0, 1)'
    def test_all_repeated(self):
        check = EX5.FindZeroSum([-3,-3,-3,-3,-3])
        assert check == 'There are no number that can be sum into 0.'
    
    #test data type
    def test_empty_list(self):
        check = EX5.FindZeroSum([])
        assert check == 'There are no number that can be sum into 0.'
    def test_none(self):
        check = EX5.FindZeroSum(None)
        assert check == 'Invalid data type'
    def test_invalid_type(self):
        check = EX5.FindZeroSum('')
        assert check == 'Invalid data type'

if __name__ == '__main__':
    unittest.main()