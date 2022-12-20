import EX6
import unittest
from unittest.mock import patch

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

    #third matrix
    matrix_dimension_input_2 = "5"
    matrix_dataset_12 = "2 2 2 2 2"

if __name__ == '__main__':
    unittest.main()