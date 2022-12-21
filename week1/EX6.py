#EX 6

#summation algorithm for row and column
def sum_row(row_matrix, size):
    result = 0
    count = 0

    #iterate row element by size
    for j in range(size):
        result = int(row_matrix[j])

        #iterate row element that is not j
        for k in range(j+1,size):
            result += int(row_matrix[k])

            #sum element until result is 10
            if result == 10:
                count += 1
                break
    return count

def MixTenMatrix():
    data_dict = {} # dictionary of matrix
    temp_list = []; data_list = []; row_list = []; col_list = []; count = []

    table_amount = input('table amount: ') #amount of the matrix

    #catch ValueError and TypeError from table amount input
    try:
        table_amount = int(table_amount)
    except (ValueError, TypeError):
        return 'Invalid table amount'
    if table_amount <= 0:
        return 'Invalid table amount'

    #iterate each matrix from table
    for i in range(table_amount):
        matrix_dimension = input('matrix dimension: ') # input matrix

        #catch ValueError and TypeError from matrix dimension input
        try:
            matrix_dimension = int(matrix_dimension)
        except (ValueError, TypeError):
            return 'Invalid matrix dimension'
        if matrix_dimension <= 0:
            return 'Invalid matrix dimension'

        data_list = []
        #iterate each dataset
        for j in range(matrix_dimension):
            matrix_dataset = input('matrix dataset: ') #input data of matrix row by row
            
            #catch TypeError from matrix dataset input
            if type(matrix_dataset) != type("A") or matrix_dataset.strip() == "":
                return 'Invalid dataset'

            #remove space
            for k in range(len(matrix_dataset)):
                if matrix_dataset[k] != " ":
                    #catch ValueError and TypeError from matrix dataset input
                    try:
                        num = int(matrix_dataset[k])
                    except (ValueError, TypeError):
                        return 'Invalid dataset'
                    if not (0 <= int(matrix_dataset[k]) <= 9):
                        return 'Invalid dataset'

                    temp_list.append(num)
        
            data_list.append(temp_list)
            temp_list = []
        data_dict[i] = data_list

    #matrix calculation
    #iterate each element in dataset
    for i in range(len(data_dict)):
        
        matrix = data_dict[i]
        
        #reset count
        count_col = 0; count_row = 0; count_tr = 0; count_tc = 0
        
        while count_col != (len(matrix)):
            
            #column system
            col_list.append(matrix[count_row][count_col])
            
            #row system
            row_list.append(matrix[count_col][count_row])
            count_row +=1
            
            if count_row == (len(matrix)):
                
                #index system
                count_row = 0
                count_col += 1

                #row summation
                count_tr += sum_row(row_list, len(matrix))
                row_list = []
                
                #column summation
                count_tc += sum_row(col_list, len(matrix))
                col_list = []

        #result
        print(count_tr+count_tc)

        #for unittest
        count.append(count_tr+count_tc)
    return count