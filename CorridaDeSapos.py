'''
Para esse exercício, será necessário criar 5 threads (1 para cada sapo).
Como o jogo funciona?
- Cada sapo pode pular uma distância randômica de até 50 cm
- Ganha quem chegar ou passar de 200 cm primeiro
- Após cada pulo, escreva quanto o sapo pulou, e a distância percorrida até o momento
- Depois de pular, o sapo precisa ‘descansar’. Dessa forma, implemente um método que faça-o descansar de 1 a
5 segundos (randômico)
'''

import threading
import time
import random

finalizados = 0

class Sapo(threading.Thread):
    def __init__(self, nome):
        threading.Thread.__init__(self)
        self.nome = nome
        self.distancia = 0
        self.pulo = 0
        self.nPulos = 0

    def run(self):
        while (True):
            global finalizados
            self.pulo = random.randint(0,50)
            self.nPulos += 1
            self.distancia += self.pulo
            print("O %s pulou %icm e já percorreu %icm\n" % (self.nome, self.pulo, self.distancia))
            if (self.distancia < 200):
                time.sleep(random.randint(1,5))
            else:
                finalizados += 1
                print("FIM: O %s foi o %i° colocado com %i pulos\n" % (self.nome, finalizados, self.nPulos))
                break

def Main():
    nSapos = 5
    sapos = [Sapo("SAPO_%i"%(i)) for i in range(0, nSapos)]
    print("** INICIO DE CORRIDA **")
    for s in sapos:
        s.start()

Main()