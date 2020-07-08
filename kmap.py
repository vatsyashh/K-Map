# CSE 101 - IP HW2
# K-Map Minimization 
# Name:Pruthwiraj Nanda
# Roll Number:2018075
# Section:A
# Group:03
# Date:19-10-2018

from copy import *

def binary_covertor(no,bits):   #takes decimal integer and the no. of bits as input, returns the correspoding binary of the given no. of bits.
    a=bin(no)
    b=a[2:]
    bits=int(bits)
    ln=len(b)
    while ln<bits:
        b='0'+b
        ln=ln+1
    return b


def dict_append(dict1, dict2):    #add two dictionaries and return a new dictionary with the keys and values of both dict1 and dict2.
    Dict = {**dict1, **dict2} 
    return Dict


def PIchecker(a,b,numVar):    #check if two minterms a and b forms an implicant... returns True if yes.
    n=0
    for i in range(numVar):
        if a[i]==b[i]:
            continue
        else:
            n=n+1
    if n==1:
        return True
    else:
        return False


def _forcommon(a,b,numVar):    #compares an Implicant of 2 terms a and b....and place _ in place of the different bit.
    for i in range(numVar):
        if a[i]=='_':
            continue
        elif a[i]!=b[i]:
            new=a[:i] + '_' + a[(i+1):]         
        elif a[i]==b[i]:
            continue
    return new


def binary_to_equation(a):      #Converts the binaries of essential Prime Implicants into equation.
    if a==None:
        return '0'
    if a=='____' or a=='___' or a=='__' or a=='_':
        return '1'

    var=['w','x','y','z']
    eq=''
    k=0
    
    for i in a:
        if i=='0':
            eq+=var[k]+"'"
            k=k+1
        elif i=='1':
            eq+=var[k]
            k=k+1
        else:
            k=k+1
    return eq


def minFunc(numVar, stringIn):     #our main function to implement k-map taking number of variables and stringIn
    a=stringIn.replace('(',' ')      #replacing the parenthesis and ',' by spaces
    b=a.replace(')',' ')
    stringIn=b.replace(',' , ' ')
    if 'd' in stringIn:
        mint=stringIn[:(stringIn.find('d')-1)].split()
        dc=stringIn[(stringIn.find('d')+1):].split()
    else:
        mint=stringIn.split()
        dc=[]
    Minterms={}         #appending all the minterms in a dictionary with keys as the minterms and values as their binary
    for i in mint:
        i=int(i)
        a=i
        i=binary_covertor(i,numVar)
        Minterms['m%s'%a ]=i
    

    Dont_cares={}           #appending all the don't cares in a dictionary with keys as the minterms and values as their binary
    for i in dc:
        i=int(i)
        a=i
        i=binary_covertor(i,numVar)
        Dont_cares['m%s'%a ]=i
#    print(Dont_cares)
     
    Terms= dict_append(Minterms,Dont_cares)   #Terms is a dictionary having all the minterms and don't cares as the keys and their corresponding binaries as the values.
                                                 
    



    D0={} ; D1={} ; D2={} ; D3={} ; D4={}   #Grouping terms with 0,1,2.. no. of 1(s) (in binary) in D0,D1,D2.... respectively.
    for i in Terms:
        if Terms[i].count('1')==0:
            D0[i]=Terms[i]
        elif Terms[i].count('1')==1:
            D1[i]=Terms[i]
        elif Terms[i].count('1')==2:
            D2[i]=Terms[i]
        elif Terms[i].count('1')==3:
            D3[i]=Terms[i]
        elif Terms[i].count('1')==4:
            D4[i]=Terms[i]



    Grp0=[D0,D1,D2,D3,D4] 
#    print('Grp0=',Grp0)
    Grp0copy=deepcopy(Grp0)         #Creating a deep copy to trace the uncombined terms left in the Grp0.

    Grp1=[{} for i in range(len(Grp0)-1)]       #Grp1 contains PIs of 2 minterms i.e. 1 '_'
    for i in Grp0[:-1]:
        nxtelement=Grp0[Grp0.index(i)+1]
        for j in nxtelement:
            for k in i:
                x=i[k]
                y=nxtelement[j]
                if PIchecker(x,y,numVar):
                    Grp1[Grp0.index(i)][str(k+'-'+j)]=_forcommon(x,y,numVar)  #appending the terms combining into next level list Grp1

                    if k in Grp0copy[Grp0.index(i)]:     #deleting the combined terms from the deep copy so as to track the uncombined terms as PI0
                        del Grp0copy[Grp0.index(i)][k]
                    if j in Grp0copy[Grp0.index(i)+1]:
                        del Grp0copy[Grp0.index(i)+1][j]
    Grp1=[i for i in Grp1 if i!={}]                      #removing the empty dictionaries.
#    print('Grp1=',Grp1)
    Grp0copy=[i for i in Grp0copy if i!={}]            
    PI0=Grp0copy
#    print('PI0=', PI0)
    

    Grp1copy=deepcopy(Grp1)                            ##Creating a deep copy to trace the uncombined terms left in the Grp1
    binaries=[]
    Grp2=[{} for i in range(len(Grp1)-1)]               #Grp2 contain PIs of 4 minterms i.e. 2 '_'
    
    for i in Grp1[:-1]:
        nxtelement=Grp1[Grp1.index(i)+1]
        for j in nxtelement:
            for k in i:
                x=i[k]
                y=nxtelement[j]
                if PIchecker(x,y,numVar):

                    if k in Grp1copy[Grp1.index(i)]:
                        del Grp1copy[Grp1.index(i)][k]
                    if j in Grp1copy[Grp1.index(i)+1]:
                        del Grp1copy[Grp1.index(i)+1][j]
                    binary=_forcommon(x,y,numVar)
                    if binary not in binaries:
                        binaries.append(binary)
                        Grp2[Grp1.index(i)][str(k+'-'+j)]=_forcommon(x,y,numVar)       #appending the terms combining into next level list Grp2
    Grp2=[i for i in Grp2 if i!={}]
    Grp1copy=[i for i in Grp1copy if i!={}]
#    print('Grp2=',Grp2)
    PI1=Grp1copy
#    print ('PI1=',PI1)



    Grp2copy=deepcopy(Grp2)                         #Creating a deep copy to trace the uncombined terms left in the Grp2
    binaries=[]
    Grp3=[{} for i in range(len(Grp2)-1)]
    
    for i in Grp2[:-1]:
        nxtelement=Grp2[Grp2.index(i)+1]
        for j in nxtelement:
            for k in i:
                x=i[k]
                y=nxtelement[j]
                if PIchecker(x,y,numVar):

                    if k in Grp2copy[Grp2.index(i)]:
                        del Grp2copy[Grp2.index(i)][k]
                    if j in Grp2copy[Grp2.index(i)+1]:
                        del Grp2copy[Grp2.index(i)+1][j]
                    binary=_forcommon(x,y,numVar)
                    if binary not in binaries:
                        binaries.append(binary)
                        Grp3[Grp2.index(i)][str(k+'-'+j)]=_forcommon(x,y,numVar)           #appending the terms combining into next level list Grp3
    Grp3=[i for i in Grp3 if i!={}]
    Grp2copy=[i for i in Grp2copy if i!={}]
#    print('Grp3=',Grp3)
    PI2=Grp2copy
#    print ('PI2=',PI2)


    Grp3copy=deepcopy(Grp3)                             #Creating a deep copy to trace the uncombined terms left in the Grp3
    binaries=[]
    Grp4=[{} for i in range(len(Grp3)-1)]
    
    for i in Grp3[:-1]:
        nxtelement=Grp3[Grp3.index(i)+1]
        for j in nxtelement:
            for k in i:
                x=i[k]
                y=nxtelement[j]
                if PIchecker(x,y,numVar):

                    if k in Grp3copy[Grp3.index(i)]:
                        del Grp3copy[Grp3.index(i)][k]
                    if j in Grp3copy[Grp3.index(i)+1]:
                        del Grp3copy[Grp3.index(i)+1][j]
                    binary=_forcommon(x,y,numVar)
                    if binary not in binaries:
                        binaries.append(binary)
                        Grp4[Grp3.index(i)][str(k+'-'+j)]=_forcommon(x,y,numVar)
    Grp4=[i for i in Grp4 if i!={}]
    PI3=Grp3copy
    Grp3copy=[i for i in Grp3copy if i!={}]
#    print('Grp4=',Grp4)
#    print( 'PI3=',PI3)
    
    All=[PI0,PI1,PI2,PI3,Grp4]             #converting our dictionaries inside the list ALL into string and then nested lists.
    All=[i for i in All if i!=[]]
    PI=[]
    for i in All:
        for j in i:
            j=list(j.items())
            PI.append(j)
#    print('PI=',PI)

    AllPIs=[]
    for i in PI:
        for j in i:
            AllPIs.append(list(j))
#    print("AllPIs=",AllPIs)             #We got the all pssible PIs assuming Don't Cares as 1


#Implementing Petrick's method to find essential PIs out of all PIs.


    EPI=[i[0] for i in AllPIs]
    A=list(map(lambda k : k.replace('-',' '),EPI))
    k=''
    for i in A:
        k+=' '+i
    
    A=list(k.split())           #A contains all the minterms (including don't cares) from AllPIs. If a minterm occurs in 2 PIs it is written twice in A.

    a=deepcopy(A)     
#    print(A)
    for i in a:
       for j in Dont_cares:
           if i==j:
                A.remove(i)         #Removing Don't cares from the list of all minterms              
    
    S=list(set(A))     #S contains all the minterms once.
    S.sort()
#    print('minerms to be covered=',S)
    

    essentials=[]
    for i in AllPIs:
        a=i[0].replace('-',' ')
        l=list(a.split())
        for j in l:
            if A.count(j)==1:
                if i in essentials:
                    continue
                else:
                    essentials.append(i)    #finding those PIs whose any of the constituent minterms is not repeating in any other PI and appending them in essentials list.
#    print('essentials(single occurence)=', essentials)

    if essentials!=[]:
        for i in essentials:                # Updating the minterms uncovered list(S) by deleting the just covered minterms from it.
            x=i[0].replace('-',' ')
            L=list(x.split())
            for y in L:
                if y in S:
                    del S[S.index(y)]
    uncovered_minterms=S                #Updated uncovered minterms list.
#    allpis=deepcopy(AllPIs)
    LeftPIs=[]
    for i in AllPIs[:]:
        if i not in essentials:
            LeftPIs.append(i)              #Appending all the PIs which aren't essential (essential due to single occurence of any of their constituent minterm)
           
#    print('LeftPIs=',LeftPIs)
#    print ('uncovered minterms=%s'%uncovered_minterms)


#using a while loop which will iterate uptil all the minterms are covered.
    while uncovered_minterms !=[]:
        maybeEPI=[]         
        considerable=[]     #Those PIs from LeftPIs which have atleast one uncovered minterm 
        for i in uncovered_minterms:
            for j in LeftPIs:
                if i in j[0]:
                    maybeEPI.append(j)      #maybeEPI contains PIs n times each, where n is the no. of uncovered minterms that PI has.
                if i in j[0]:
                    if j not in considerable:
                        considerable.append(j)     #considerable contains the same PIs each once 
 
        frequency=[]
        for i in considerable:                      
            a=maybeEPI.count(i)
#            print('count of %s is %s' %(i,a))
            frequency.append(a)                     #frequency list contains the frequency of the occurences of PIs in maybeEPI at same index no. as the PI.
#        print(frequency)
        m=max(frequency)
        ind=frequency.index(m)                      #figuring out which PI has max frequency i.e. which will cover max no. of uncovered minterms, that will be an essential PI.
        essentials.append(considerable[ind])        #appending that PI to essential and deleting it from considerabele.
        del considerable[ind]


        if essentials!=[]:
            for i in essentials:                    #updating the uncovered terms 
                x=i[0].replace('-',' ')
                L=list(x.split())
                for y in L:
                    if y in uncovered_minterms:
                        del uncovered_minterms[uncovered_minterms.index(y)]     #Deleting the terms covered by the new selected Essential PI from uncovered minterms list.    
#    print('uncovered_minterms=',uncovered_minterms)      #this should be an empty list


   
#    print ('essentials=%s'%essentials)


    Ans=''
    expressions=[]
    for i in essentials:
        a=binary_to_equation(i[1])         #converting the essential PIs into vari
        expressions.append(a)
        expressions.sort()
    for j in expressions:
        Ans+='+'+j

    return Ans[1:]
print(minFunc(3,'(3,4,7) d(1,2,5,6)'))
