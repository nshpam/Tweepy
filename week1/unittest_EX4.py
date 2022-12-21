import EX4
import unittest

class FindRepeatUnitTest(unittest.TestCase):

    #not sort

    #one repeat
    def test_one_repeat_not_sort(self):
        check = EX4.FindRepeat([1,2,3,4,3])
        assert check == 'Yes : There are 1 repeat numbers. The repeated indexes are [2, 4]' #expect that result will be this value
    
    #two repeat
    def test_two_repeat_not_sort(self):
        check = EX4.FindRepeat([1,2,3,4,3,4])
        assert check == 'Yes : There are 2 repeat numbers. The repeated indexes are [2, 3, 4, 5]'
    
    #no repeat
    def test_no_repeat_not_sort(self):
        check = EX4.FindRepeat([1,2,4,3])
        assert check == 'No'

    #all repeat
    def test_all_repeat_not_sort(self):
        check = EX4.FindRepeat([1,2,3,1,2,3])
        assert check == 'Yes : There are 3 repeat numbers. The repeated indexes are [0, 1, 2, 3, 4, 5]'

    #sorted

    #one repeat
    def test_one_repeat_sorted(self):
        check = EX4.FindRepeat([1,2,3,3,4])
        assert check == 'Yes : There are 1 repeat numbers. The repeated indexes are [2, 3]'
    
    #two repeat
    def test_two_repeat_sorted_consecutive(self):
        check = EX4.FindRepeat([1,1,2,2,3,4])
        assert check == 'Yes : There are 2 repeat numbers. The repeated indexes are [0, 1, 2, 3]'
    
    #no repeat
    def test_no_repeat_sorted(self):
        check = EX4.FindRepeat([1,2,3,4])
        assert check == 'No'
    
    #all repeat
    def test_all_repeat_sorted(self):
        check = EX4.FindRepeat([1,1,2,2,3,3])
        assert check == 'Yes : There are 3 repeat numbers. The repeated indexes are [0, 1, 2, 3, 4, 5]'

    #blank list
    def test_blank(self):
        check = EX4.FindRepeat([])
        assert check == 'No'
    
    #none
    def test_none(self):
        check = EX4.FindRepeat(None)
        assert check == 'No'

#run this code if and only if it's the main file
if __name__ == '__main__':
    unittest.main()