#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from builtins import range
from tabulate import tabulate

BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[93m"
YEL = "\e[93mLight"
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
            print(RED+"A paridade de um dos bytes nao bateu!"+NOC)
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
        print(RED+"Paridade do BCC nao bateu!"+NOC, bcc, m[len(m) - 8:], NOC)
        return False

    if (getParity(wholeParity) != m[len(m) - 1]):
        print(RED+"Paridade de todas as paridades não bateu!")
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
    print(tabulate(table, ["LETRA","ASCII","BINARIO", "PARIDADE"],"grid"))
    print("Mensagem formada:\n" + m_colored)

    return returnMessage

def interference(m, i):
    lm = list(m)
    changed = False
    if (random.randrange(100) < i): #50 porcento de chance de interferência
        position = random.randrange(len(lm))
        lm[position] = ('1' if lm[position] == '0' else '0')# troca o valor
        changed = True

    return changed, "".join(lm)

percent = int(input("(digitar \"sair\" para sair) \n Qual porcentagem da mensagem sofrer interferencia e ter um byte alterado?\n"))
message = input("Mensagem:\n")
while message != "sair":
    message = formMessage(message)
    OK = False
    changed = False
    while not OK:
        changed, messageErrored = interference(message, percent)
        print(BLUE+"Mensagem sofreu interferencia:\n" + NOC + messageErrored if changed else BLUE+ "Mensagem nao sofreu interferencia."+NOC)
        OK = checkMessage(messageErrored)
        print(GREEN+"Mensagem OK"+NOC if OK else RED+"Nao Ok. Enviando novamente..."+NOC)

    message = input("Mensagem:\n")


