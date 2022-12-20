import EX4
import unittest

class FindRepeatUnitTest(unittest.TestCase):

    #not sort
    def test_one_repeat_not_sort(self):
        check = EX4.FindRepeat([1,2,3,4,3])
        assert check == 'Yes : There are 1 repeat numbers. The repeated indexes are [2, 4]' #expect that result will be this value
    def test_two_repeat_not_sort(self):
        check = EX4.FindRepeat([1,2,3,4,3,4])
        assert check == 'Yes : There are 2 repeat numbers. The repeated indexes are [2, 3, 4, 5]'
    def test_no_repeat_not_sort(self):
        check = EX4.FindRepeat([1,2,4,3])
        assert check == 'No'
    def test_all_repeat_not_sort(self):
        check = EX4.FindRepeat([1,2,3,1,2,3])
        assert check == 'Yes : There are 3 repeat numbers. The repeated indexes are [0, 1, 2, 3, 4, 5]'

    #sorted
    def test_one_repeat_sorted(self):
        check = EX4.FindRepeat([1,2,3,3,4])
        assert check == 'Yes : There are 1 repeat numbers. The repeated indexes are [2, 3]'
    def test_two_repeat_sorted_consecutive(self):
        check = EX4.FindRepeat([1,1,2,2,3,4])
        assert check == 'Yes : There are 2 repeat numbers. The repeated indexes are [0, 1, 2, 3]'
    def test_no_repeat_sorted(self):
        check = EX4.FindRepeat([1,2,3,4])
        assert check == 'No'
    def test_all_repeat_sorted(self):
        check = EX4.FindRepeat([1,1,2,2,3,3])
        assert check == 'Yes : There are 3 repeat numbers. The repeated indexes are [0, 1, 2, 3, 4, 5]'

    #null
    def test_blank(self):
        check = EX4.FindRepeat([])
        assert check == 'No'
    def test_none(self):
        check = EX4.FindRepeat(None)
        assert check == 'No'

if __name__ == '__main__':
    unittest.main()