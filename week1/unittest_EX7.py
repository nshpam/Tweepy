import EX7
import unittest
from unittest.mock import patch, mock_open

class EqnSolveInputTest(unittest.TestCase):
    
    txt_file = '16 200 -10\n12\n70\n1\n999\n50\n20\n1000\n150\n300\n200\n90\n900\n40\n140\n130\n30'

    #check file input
    with patch('builtins.open', mock_open(read_data= txt_file)):
        def test_txt_file_input(self):
            with open('file.txt') as f:
                check = EX7.EqnSolve(f)
                self.assertEqual(check, ['16 200 -10\n', '12\n', '70\n', '1\n', '999\n', '50\n', '20\n', '1000\n', '150\n', '300\n', '200\n', '90\n', '900\n', '40\n', '140\n', '130\n', '30'])W

if __name__ == '__main__':
    unittest.main()