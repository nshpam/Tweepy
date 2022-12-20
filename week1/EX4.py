def FindRepeat(test_list):
    templist = []
    index_list = []
    count_i = 0
    count_j = 0
    count_repeat = 0
    check = False
    send_text = ''

    if type(test_list) != type([]):
        send_text = 'No'
        print(send_text)
        return send_text

    for i in test_list:
        templist = test_list[count_i+1:]
        
        #checking list is empty
        if templist == []:
            break
        count_j = count_i+1
        
        #found the duplicate number
        for j in templist:
            if i == j:
                check = True
                count_repeat += 1
                index_list.append(count_i)
                index_list.append(count_j)
                count_j = 0
                break
            count_j+=1
        count_i+=1

    if check != True:
        send_text = 'No'
        print(send_text)
    else:
        index_list.sort()
        send_text = 'Yes : There are %d repeat numbers. The repeated indexes are %s'%(count_repeat, str(index_list))
        print (send_text)
    
    return send_text