import EX6
import unittest
from unittest.mock import patch

#mock input test
class MixTenMatrixInputTest(unittest.TestCase):

    #first matrix
    matrix_dimension_input_1 = "4"
    matrix_dataset_11 = "1 3 5 7"
    matrix_dataset_21 = "2 4 8 2"
    matrix_dataset_31 = "6 3 1 1"
    matrix_dataset_41 = "2 3 5 6"

    #second matrix
    matrix_dimension_input_2 = "5"
    matrix_dataset_12 = "2 2 2 2 2"

    #input 1 matrix
    @patch('builtins.input', side_effect=[
        "1", 
        matrix_dimension_input_1,
        matrix_dataset_11,
        matrix_dataset_21,
        matrix_dataset_31,
        matrix_dataset_41,
    ])
    def test_one_matrix(self, mock_input):
        mock_table_amount = mock_input()
        mock_matrix_dimension_1 = mock_input()
        matrix_11 = mock_input()
        matrix_21 = mock_input()
        matrix_31 = mock_input()
        matrix_41 = mock_input()
    
        self.assertTrue(
            mock_table_amount == '1' and 
            mock_matrix_dimension_1 == '4' and
            matrix_11 == '1 3 5 7' and 
            matrix_21 == '2 4 8 2' and 
            matrix_31 == '6 3 1 1' and 
            matrix_41 == '2 3 5 6')

    #input 2 matrix
    @patch('builtins.input', side_effect=[
        "2", 
        matrix_dimension_input_1,
        matrix_dataset_11,
        matrix_dataset_21,
        matrix_dataset_31,
        matrix_dataset_41,
        matrix_dimension_input_2,
        matrix_dataset_12,
        matrix_dataset_12,
        matrix_dataset_12,
        matrix_dataset_12,
        matrix_dataset_12])
    def test_two_matrix(self, mock_input):
        mock_table_amount = mock_input()
        mock_matrix_dimension_1 = mock_input()
        matrix_11 = mock_input()
        matrix_21 = mock_input()
        matrix_31 = mock_input()
        matrix_41 = mock_input()
        mock_matrix_dimension_2 = mock_input()
        matrix_12 = mock_input()
        matrix_22 = mock_input()
        matrix_32 = mock_input()
        matrix_42 = mock_input()
        matrix_52 = mock_input()

        self.assertTrue(
            mock_table_amount == '2' and 
            mock_matrix_dimension_1 == '4' and
            matrix_11 == '1 3 5 7' and 
            matrix_21 == '2 4 8 2' and 
            matrix_31 == '6 3 1 1' and 
            matrix_41 == '2 3 5 6' and
            mock_matrix_dimension_2 == '5' and
            matrix_12 == '2 2 2 2 2' and
            matrix_22 == '2 2 2 2 2' and
            matrix_32 == '2 2 2 2 2' and
            matrix_42 == '2 2 2 2 2' and
            matrix_52 == '2 2 2 2 2')     

#test output
class MixTenMatrixUnitTest(unittest.TestCase):

    #first matrix
    matrix_dimension_input_1 = "4"
    matrix_dataset_11 = "1 3 5 7"
    matrix_dataset_21 = "2 4 8 2"
    matrix_dataset_31 = "6 3 1 1"
    matrix_dataset_41 = "2 3 5 6"

    #seconds matrix
    matrix_dimension_input_2 = "4"
    matrix_dataset_12 = "1 2 3 4"

    #thrid matrix
    matrix_dimension_input_3 = "5"
    matrix_dataset_13 = "1 2 3 4 5"
    matrix_dataset_23 = "6 7 8 9 0"
    matrix_dataset_33 = "2 4 6 8 0"
    matrix_dataset_43 = "1 3 5 7 9"
    matrix_dataset_53 = "1 1 1 1 1"

    #fourth matrix
    matrix_dimension_input_4 = "5"
    matrix_dataset_14 = "2 2 2 2 2"

    #4x4 matrix not repeat --- 1 matrix
    @patch('builtins.input', side_effect=[
        "1", 
        matrix_dimension_input_1,
        matrix_dataset_11,
        matrix_dataset_21,
        matrix_dataset_31,
        matrix_dataset_41])
    def test_4x4_matrix_not_repeat(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, [7])
    
    #5x5 matrix not repeat --- 1 matrix
    @patch('builtins.input', side_effect=[
        "1", 
        matrix_dimension_input_3,
        matrix_dataset_13,
        matrix_dataset_23,
        matrix_dataset_33,
        matrix_dataset_43,
        matrix_dataset_53])
    def test_5x5_matrix_not_repeat(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, [7])
    
    #4x4 matrix repeat --- 1 matrix
    @patch('builtins.input', side_effect=[
        "1", 
        matrix_dimension_input_2,
        matrix_dataset_12,
        matrix_dataset_12,
        matrix_dataset_12,
        matrix_dataset_12])
    def test_4x4_matrix_repeat(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, [4])
    
    #5x5 matrix repeat --- 1 matrix
    @patch('builtins.input', side_effect=[
        "1", 
        matrix_dimension_input_4,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14])
    def test_4x4_matrix_repeat(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, [10])
    
    #test table amount input

    #can't convert to int
    @patch('builtins.input', side_effect=[
        "A", 
        matrix_dimension_input_4,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14])
    def test_invalid_table_input(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, 'Invalid table amount')

    #negative integer
    @patch('builtins.input', side_effect=[
        "-1", 
        matrix_dimension_input_4,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14])
    def test_invalid2_table_input(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, 'Invalid table amount')

    #blank
    @patch('builtins.input', side_effect=[
        "", 
        matrix_dimension_input_4,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14])
    def test_blank_table_input(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, 'Invalid table amount')
    
    #none
    @patch('builtins.input', side_effect=[
        None, 
        matrix_dimension_input_4,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14])
    def test_null_table_input(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, 'Invalid table amount')
    
    #test matrix dimension

    #can't convert to int
    @patch('builtins.input', side_effect=[
        "1", 
        "A",
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14])
    def test_invalid_dimension_input(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, 'Invalid matrix dimension')
    
    #negative integer
    @patch('builtins.input', side_effect=[
        "1", 
        "-1",
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14])
    def test_invalid2_dimension_input(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, 'Invalid matrix dimension')
    
    #blank 
    @patch('builtins.input', side_effect=[
        "1", 
        "",
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14])
    def test_blank_dimension_input(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, 'Invalid matrix dimension')
    
    #none
    @patch('builtins.input', side_effect=[
        "1", 
        None,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14])
    def test_null_dimension_input(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, 'Invalid matrix dimension')

    #test dataset input

    #dataset element is not 0-9
    @patch('builtins.input', side_effect=[
        "1", 
        matrix_dimension_input_4,
        "-1 0 1 2 3",
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14,
        matrix_dataset_14])
    def test_negative_dataset_input(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, 'Invalid dataset')
    
    #blank dataset element
    @patch('builtins.input', side_effect=[
        "1", 
        matrix_dimension_input_4,
        " ",
        "",
        "  ",
        "    ",
        "."])
    def test_blank_dataset_input(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, 'Invalid dataset')
    
    #alphabet dataset element
    @patch('builtins.input', side_effect=[
        "1", 
        matrix_dimension_input_4,
        "A B C D A",
        "E F G H A",
        "I J K L A",
        "U P K S E",
        "K O I M H"])
    def test_invalid_dataset_input(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, 'Invalid dataset')
    
    #none dataset element
    @patch('builtins.input', side_effect=[
        "1", 
        matrix_dimension_input_4,
        None,
        None,
        None,
        None,
        None])
    def test_None_dataset_input(self, mock_inputs):
        check = EX6.MixTenMatrix()
        self.assertEqual(check, 'Invalid dataset')

#run this code if and only if it's the main file
if __name__ == '__main__':
    unittest.main()