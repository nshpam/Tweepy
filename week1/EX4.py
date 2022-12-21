#Find the repeat number from the list
#type of test_list is list
def FindRepeat(test_list):
    templist = []
    index_list = []
    count_i = 0
    count_j = 0
    count_repeat = 0
    check = False
    send_text = ''

    #check type of input which can only be list to continue processing
    if type(test_list) != type([]):
        send_text = 'No'
        print(send_text)
        return send_text

    #iterate element from input list
    for i in test_list:

        #templist will store the element that is not i yet
        templist = test_list[count_i+1:]
        
        #check if list is empty 
        if templist == []:
            break
            
        #index for templist
        count_j = count_i+1
        
        #iterate element from templist
        for j in templist:

        #found the duplicate number
            if i == j:
                check = True

                #count the repeat number
                count_repeat += 1
                index_list.append(count_i)
                index_list.append(count_j)
                count_j = 0
                break
            count_j+=1
        
        #index for test_list
        count_i+=1

    #not found the duplicate number
    if check != True:
        send_text = 'No'
        print(send_text)
    
    #found the duplicate number
    else:
        index_list.sort()
        send_text = 'Yes : There are %d repeat numbers. The repeated indexes are %s'%(count_repeat, str(index_list))
        print (send_text)
    
    #for unittest
    return send_text