'''
Created on 13 Mar 2018

@author: harri
'''
#List containing ASCII characters
alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','@']
#List containing hexadecimal variables.
hextable=['60','61','62','63','64','65','66','67','68','69','6A','6B','6C','6D','6E','6F','70','71','72','73','74','75','76','77','78','79','7A','40']

def hexEncrypt(passw):
    global alphabet, hextable
    try:
        newpass=['0x']
        for i in range(len(passw)):
            curval=passw[i]
            for j in range(len(alphabet)):
                if curval == alphabet[j]:
                    newpass.append(hextable[j])
    except:
        IndexError
    return (''.join(newpass))

def hexDecrypt(passw):
    try:
        newpass=[]
        for i in range(len(passw)):
            #I don't even know what the fuck happened here.
            if i == 0:
                curval=str((passw[i])+(passw[i+1]))
            else:
                curval=str((passw[i*2])+(passw[(i*2)+1]))
            for j in range(len(hextable)):
                if curval == hextable[j]:
                    newpass.append(alphabet[j])
    except:
        IndexError
    return (''.join(newpass))

print(hexEncrypt("testtest"))