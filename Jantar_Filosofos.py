'''
Esse é um problema clássico de concorrência. Considere n filósofos que passam a vida pensando e comendo. Partilham
uma mesa redonda, cada um com um prato e um garfo. A comida é uma massa escorregadia e, por isso, os filósofos
somente conseguem comer com dois garfos

Entretanto, só temos um garfo para cada um. Dessa forma, ele pega o garfo da esquerda e, depois, o garfo da direita.
Quando conseguir pegar os dois garfos, ele consegue comer. A ordem de execução é a seguinte (em loop infinito)

- Filósofo pensa
- Filósofo pega garfo esquerdo
- Filósofo pega garfo direito
- Filósofo come
- Filósofo libera garfo direito
- Filósofo libera garfo esquerdo

Exercício 1:
Implemente um programa em Python utilizando threads e lock para simular o jantar dos filósofos.
Exercício 2:
Permita ao usuário informar o número de filósofos que irão sentar à mesa. A partir disso, crie o número de garfos e
threads correspondentes

'''

import threading
import time
import random

garfos = list()
nFilosofos = 0

class Filosofo(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        global garfos, nFilosofos
        self.id = id

    def pensar(self):
        print("Filósofo %i está pensando...\n" % (self.id))
        time.sleep(random.randint(1, 5))
        print("Filósofo %i terminou de pensar...\n" % (self.id))

    def comer(self):
        print("Filósofo %i obteve os dois garfos e está comendo...\n" % (self.id))
        time.sleep(random.randint(1, 5))

    def run(self):
        print("Filósofo %i sentou-se à mesa...\n"%(self.id))
        while True:
            self.pensar()

            garfos[self.id].acquire()
            print("Filósofo %i pegou o garfo esquerdo...\n" % (self.id))
            garfos[(self.id + 1) % nFilosofos].acquire()
            print("Filósofo %i pegou o garfo direito...\n" % (self.id))

            self.comer()

            garfos[(self.id + 1) % nFilosofos].release()
            print("Filósofo %i liberou o garfo direito...\n" % (self.id))
            garfos[self.id].release()
            print("Filósofo %i liberou o garfo esquerdo...\n" % (self.id))

def Main():
    global garfos, nFilosofos
    filosofos = list()
    nFilosofos = int(input("Numero de filósofos:"))
    for i in range(0, nFilosofos):
        filosofos.append(Filosofo(i))
        garfos.append(threading.Semaphore(1))

    for f in filosofos:
        f.start()


Main()