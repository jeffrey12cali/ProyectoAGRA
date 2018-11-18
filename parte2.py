import re


g=0
p=9999


while True:
    
    string =input("Enter the string: ")
    #x={}
    y={}
    cadena=re.findall("[a-zA-Z_]+", string)
    if len(cadena)==0:
        p=0
    for i in range (len(cadena)):
        cadena[i]=cadena[i].lower()
    #['yes', 'sir', 'right', 'away', 'sir', 'right', 'sir', 'yes']

    srepeat=list(set(cadena))
    #['away', 'right', 'yes', 'sir']

    print(cadena)
    #print(len(cadena))
    #print(srepeat)

    count=0
    contWords=0
    for i in range(len(srepeat)):
        #x[srepeat[i]]=i
        y[srepeat[i]]=0


    for i in range(len(cadena)):
        
        for j in  range(i,len(cadena)):
            #print(i)

            if y[cadena[j]]==0:
                y[cadena[j]]=1
                count+=1
                if count==len(srepeat):
                    if j-i<p-g:
                        g=i
                        p=j
                    if j-i==p-g:
                        if i < g:
                            g=i
                            p=j
                        else:
                            pass

       
                    #print(i,j)
                    count=0
                    for s in range(len(srepeat)):
                        #x[srepeat[i]]=i
                        y[srepeat[s]]=0

                    break
    print(g,p+1)



            

    #count = len(re.findall("[a-zA-Z_]+", string))
    #print (count)


print ("Terminated")

#ist(set(t))