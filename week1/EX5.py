#EX 5

#Find three sum problem 
def FindZeroSum(mylist):

    if type(mylist) != type([]):
        return 'Invalid data type'

    nums_list = []
    sum_list = []
    nums_list_2 = []
    result = ''

    #iterate first number
    for i in range(len(mylist)):

        #iterate second number
        for j in range(i+1, len(mylist)):

            #list of first two numbers
            nums_list.append([mylist[i], mylist[j]])

            #list of two sum
            sum_list.append(mylist[i] + mylist[j])

    #iterate thrid number
    for i in range(len(mylist)):

        #iterate first two sum
        for j in range(len(sum_list)):

            #if the third number is inverse of two sum
            if mylist[i] == -sum_list[j] and mylist[i] != nums_list[j][0] and mylist[i] != nums_list[j][1]:
                nums_list_2.append(sorted([nums_list[j][0], nums_list[j][1],mylist[i]]))
                break

    nums_list_2.sort()
    nums_list_2.append([])

    #remove repeat cases

    #iterate the result
    for i in range(len(nums_list_2)):
        if i == len(nums_list_2)-1:
            result = result[:-1]
            print(result)

            if result == '':
                result = 'There are no number that can be sum into 0.'
            return result

        if nums_list_2[i] != nums_list_2[i+1]:
            result += '(%d, %d, %d),'%(nums_list_2[i][0], nums_list_2[i][1], nums_list_2[i][2])