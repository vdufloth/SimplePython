#!/usr/bin/python
# -*- coding: utf-8 -*-

BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[93m'
NOC = '\033[0m'

s = input()
allBytes = []
parityString = ''
message= ''
message_colored=''

def getParity(s):
    p=0
    for digit in s:
        p += int(digit)        
    return str(int((p % 2 != 0)))

def checkMessage(m):
    bcc = ''
    _byte = ''
    allBytesc = []
    for i in range(0, len(m), 8):
        _byte = m[i:i+7]        
        allBytesc.append(_byte)

        parity = getParity(_byte)
        # print(_byte, parity)
        if m[i+7] != parity:
            print(m[i+7], '!=', parity)
            return 0
       
    for i in range(0,7):
        byteToCheck = ''
        for j in range (0, len(allBytesc)):
            byteToCheck += allBytesc[j][i]
        bcc += getParity(byteToCheck)
    print(bcc, 'm', m[len(m)-8:])
    # if (bcc != m[len(m)-8:])
    return 1

for c in (s):
    n = ord(c) #transforma no inteiro ASCII
    parity = ''
    b = bin(n) #transforma em binario
    b = b[2:] #remove o 0b
    allBytes.append(b)
    parity = getParity(b)
    message += b + parity
    message_colored += b  + GREEN + parity + NOC

    print(c, n, b, parity)

# allBytes[1][1] + allBytes[2][1] + allBytes [3][1] ate len
#depois all bytes [1][2] ate 7
bcc = ''
for i in range(0,7):
    byteToCheck = ''
    for j in range (0, len(allBytes)):
        byteToCheck += allBytes[j][i]
    bcc += getParity(byteToCheck)

bccParity = getParity(bcc)
message += bcc + bccParity
message_colored += BLUE + bcc + GREEN + bccParity + NOC
print('=   ',bcc, bccParity)
print(message_colored)
print(message)

checkMessage(message)
# print(checkMessage())


