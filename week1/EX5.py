mylist = [0,-1,2,-3,1,-2]
num = 0
mylist.sort()
result = ''

for i in range(len(mylist)):
  
    #finish
    if i == len(mylist)-1:
        print(result[:-1])
        break
        
    num = mylist[i]+mylist[i+1]
    
    #find the last element
    for j in range(len(mylist)):
        if mylist[j] == -num:
            result += "(%d %d %d),"%(mylist[i],mylist[i+1],mylist[j])
