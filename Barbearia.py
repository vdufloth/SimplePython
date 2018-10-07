
import random
import threading
import time
import queue

nCadeiras = 0
clientesC = queue.Queue()
clientesB = queue.Queue()
cortandoCabelo = False
DormindoB = True
DormindoC = True
clienteID = 0
esperarB = threading.Condition()
esperarC = threading.Condition()

class Barbeiro(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run (self):
        global DormindoB, esperarB
        while True:
            esperarB.acquire()
            if clientesB.empty():
                print('-Barbeiro: Nenhum cliente... vou dormir')
                DormindoB = True
                esperarB.wait()

            i = clientesB.get()
            esperarB.release()
            print('-Barbeiro: Atendendo cliente %i'%(i))
            time.sleep(random.randint(1,5))
            print('-Barbeiro: Atendimento terminado para o cliente %i'%(i))

class Cabeleireiro(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def run (self):
        global DormindoC, esperarC
        while True:
            esperarC.acquire()
            if clientesC.empty():
                print('-Cabeleireiro: Nenhum cliente... vou dormir')
                DormindoC = True
                esperarC.wait()

            i = clientesC.get()
            esperarC.release()
            print('-Cabeleireiro: Atendendo cliente %i'%(i))
            time.sleep(random.randint(1,5))
            print('-Cabeleireiro: Atendimento terminado para o cliente %i'%(i))


class produtoraDeClientes(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global clienteID, DormindoC, DormindoB, esperarC
        while True:
            esperarC.acquire()
            esperarB.acquire()
            if (clientesC.qsize() + clientesB.qsize()) < nCadeiras:
                if (bool(random.getrandbits(1))):
                    esperarB.release()
                    clientesC.put(clienteID)
                    print('-Cliente %i: Cheguei para cortar o cabelo!' % (clienteID))
                    if DormindoC:
                        esperarC.notify()
                        esperarC.release()
                        DormindoC = False
                        print('-Cliente %i: Acordando o cabeleireiro... mas que folgado...'%(clienteID))
                else:
                    esperarC.release()
                    clientesB.put(clienteID)
                    print('-Cliente %i: Cheguei para fazer a barba!' % (clienteID))
                    if DormindoB:
                        esperarB.notify()
                        esperarB.notify()
                        esperarB.release()
                        DormindoB = False
                        print('-Cliente %i: Acordando o barbeiro... mas que folgado...' % (clienteID))

                clienteID += 1
            else:
                print('-Cliente: Muito Cheio... Indo Embora')
            time.sleep(random.randint(1,3))

def main():
    global nCadeiras
    nCadeiras = 5
    b = Barbeiro()
    c = Cabeleireiro()
    b.start()
    c.start()
    p = produtoraDeClientes()
    p.start()

main()