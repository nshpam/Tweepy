def MixTenMatrix():
    data_dict = {} # dictionary of matrix
    temp_list = []; data_list = []; row_list = []; col_list = []

    table_amount = int(input('table amount: ')) #amount of the matrix

    if table_amount <= 0:
        return 'Invalid table amount'
    #create matrix with dictionary
    for i in range(table_amount):
        matrix_dimension = int(input('matrix dimension: ')) # input matrix
        data_list = []
        for j in range(matrix_dimension):
            matrix_dataset = input('matrix dataset: ') #input data of matrix row by row
            
            #remove space
            for k in range(len(matrix_dataset)):
                if matrix_dataset[k] != " ":
                    temp_list.append(matrix_dataset[k])
        
            data_list.append(temp_list)
            temp_list = []
        data_dict[i] = data_list
        
    #summation algorithm
    def sum_row(row_matrix, size):
        result = 0
        count = 0
        for j in range(size):
            result = int(row_matrix[j])
            for k in range(j+1,size):
                result += int(row_matrix[k])
                if result == 10:
                    count += 1
                    break
        return count

    #matrix calculation
    for i in range(len(data_dict)):
        
        matrix = data_dict[i]
        
        #reset count
        count_col = 0; count_row = 0; count_tr = 0; count_tc = 0;
        
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

        print(count_tr+count_tc)    #result
    # count = count_tc+count_tr
    # return count

# print(mix_ten_matrix())
