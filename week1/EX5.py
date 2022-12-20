mylist = [0,-1,2,-3,1,-2]

def FindZeroSum(mylist):
    num = 0
    result = ''
    count_first = 0
    count_last = -1

    for i in range(len(mylist)):

        if count_first == int(len(mylist)/2):
            print(result[:-1])
            break
        num  = mylist[count_first] + mylist[count_last]
        
        for j in range(len(mylist)):
            if mylist[j] == -num and mylist[j] != mylist[count_first] and mylist[j] != mylist[count_last]:
                result += "(%d %d %d),"%(mylist[count_last],mylist[count_first],mylist[j])

        count_first+=1
        count_last-=1