#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from builtins import range
from tabulate import tabulate

BLUE = "\033[94m"
GREEN = "\033[92m"
YEL = "\033[93m"
NOC = "\033[0m"

def getParity(s):
    p = 0
    for digit in s:
        p += int(digit)
    return str(int((p % 2 != 0)))

def checkMessage(m):
    _byte = ''
    allBytes = []
    wholeParity = ''

    for i in range(0, len(m), 8):
        _byte = m[i:i + 7]
        allBytes.append(_byte)
        parity = getParity(_byte)
        wholeParity += parity
        if m[i + 7] != parity:
            print(YEL+"One of the byte's parity did not match!"+NOC)
            return False

    wholeParity = wholeParity[0:len(wholeParity) - 1] #remove o do bcc
    bcc = ''
    for i in range(0, 7):
        byteToCheck = ''
        for j in range(0, len(allBytes) - 1): # - 1 para ignorar o próprio BCC
            byteToCheck += allBytes[j][i]
        bcc += getParity(byteToCheck)

    bcc += getParity(bcc) # adicionar sua paridade ao final
    if (bcc != m[len(m) - 8:]):
        print(YEL+"BCC parity did not match!"+NOC, bcc, m[len(m) - 8:], NOC)
        return False

    if (getParity(wholeParity) != m[len(m) - 1]):
        print(YEL+"All-Parities Parity did not match!")
        return False

    return True

def formMessage(m):
    table = []
    tablefmt = "grid"

    allBytes = []
    m_colored = ''
    returnMessage = ''
    for c in (m):
        n = ord(c)  # transforma no inteiro ASCII
        b = bin(n)  # transforma em binario
        b = b[2:]  # remove o b
        allBytes.append(b)
        parity = getParity(b)
        returnMessage += b + parity
        m_colored += b + GREEN + parity + NOC

        table.append([c, n, b, parity])

    bcc = ''
    for i in range(0, 7):
        byteToCheck = ''
        for j in range(0, len(allBytes)):
            byteToCheck += allBytes[j][i]
        bcc += getParity(byteToCheck)

    bccParity = getParity(bcc)
    table.append(["BCC","-", bcc, bccParity])

    returnMessage += bcc + bccParity
    m_colored += BLUE + bcc + GREEN + bccParity + NOC
    print(tabulate(table, ["LETTER","ASCII","BINARY", "PARITY"],"grid"))
    print("Message formed: " + m_colored)

    return returnMessage

def interference(m, i):
    lm = list(m)
    changed = False
    if (random.randrange(100) < i):
        position = random.randrange(len(lm))
        lm[position] = ('1' if lm[position] == '0' else '0')#change the value
        changed = True

    return changed, "".join(lm)

percent = int(input("(Type \"exit\" to exit) \n Percent chance of message having one byte changed:\n"))
message = input("Message:\n")
while message != "exit":
    message = formMessage(message)
    OK = False
    changed = False
    while not OK:
        changed, messageErrored = interference(message, percent)
        print(BLUE+"Message was changed!\n" + NOC + messageErrored if changed else BLUE+ "Message was not changed."+NOC)
        OK = checkMessage(messageErrored)
        print(GREEN+"Message OK"+NOC if OK else YEL+"Not OK. Sending again..."+NOC)

    message = input("Mensagem:\n")
