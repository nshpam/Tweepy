#EX 7

def EqnSolve(myfile):
    A = []
    data_dict = {}

    try:
        myfile = myfile.readlines()
    except (TypeError, ValueError):
        return 'Invalid file type'
    # myfile = open("file.txt", "r").readlines()
    # print(myfile)

    #create a list of data from file.txt
    for i in range(len(myfile)):
        if i == 0:
            eqn = myfile[i].strip().split()
            continue
        A.append(int(myfile[i]))

    #find x1, x2, x3, x4
    for i in range(len(A)):
        for j in range(i+1,len(A)):
                for k in range(j+1,len(A)):
                        if A[i]-A[j]+A[k] == int(eqn[1]) and A[i]-A[j] in A:
                            data_dict['x1'] = A[i]-A[j]
                            data_dict['x2'] = A[k]
                            data_dict['x3'] = A[j]
                            data_dict['x4'] = A[i]

    #find x5, x6, x7, x8
    for i in range(len(A)):
        for j in range(i+1,len(A)):
                for k in range(j+1,len(A)):
                    if A[i] in data_dict.values() or A[j] in data_dict.values() or A[k] in data_dict.values():
                        break
                    if A[i]-A[j]+A[k] == int(eqn[2]) and A[j]-A[i] in A:
                            data_dict['x5'] = A[i]
                            data_dict['x6'] = A[j]-A[i]
                            data_dict['x7'] = A[j]
                            data_dict['x8'] = A[k]

    #output
    for i in range(len(data_dict)):
        print(list(data_dict.values())[i])
    
    return myfile

# EqnSolve()