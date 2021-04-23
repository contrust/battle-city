import random
a = []
for i in range(0,14):
    n = []
    count = 0
    for j in range(0,14):
        r = random.randint(0,1)
        g = random.randint(0,3)
        if i==12 and j==5 or i==12 and j==6 or i==12 and j==7 or i==13 and j==5 or i==13 and j==6 or i==13 and j==7 or i==13 and j==4:
            n.append('.')
            continue
        try:
            if r == 0 or count > 4 or (a[i-1][j+1]=='0' and a[i-1][j+1]=='0'):
                if g==0 or g==1 or g==2:
                    n.append('.')
                else:
                    n.append('1')
            else:
                n.append('0')
                count+=1
        except:
            if r == 0 or count > 5:
                if g==0 or g==1 or g==2:
                    n.append('.')
                else:
                    n.append('1')
            else:
                n.append('0')
                count+=1
    a.append(n)
for x in a:
    print(x,',')

