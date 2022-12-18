mylist = [1,1,2]
templist = []
count = 0
check = False

for i in mylist:
    templist = mylist[count+1:]
    count+=1
    
    #checking list is empty
    if templist == []:
        break
    
    #found the duplicate number
    for j in templist:
        if i == j:
            check = True

if check != True:
    print('No')
else:
    print ('Yes')
