'''
Utilizar fila e threads para criar N threads ao Crawler
'''

import requests
import threading

semaforoBuscar = threading.Semaphore(1)
#parabuscar e navegados tem que ser globais e protegidos por semaforo
navegados = []
paraBuscar = []
errors = []
maximoPaginas = 1000
nivelMaximo = 5
nThreads = 1

class BuscarLinksNaWeb(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        global navegados, semaforoNavegados,nThreads,\
        paraBuscar, maximoPaginas, nivelMaximo, errors

        self.id = id
        nThreads = nThreads - 1

    def getProximaPagina(self, pagina):
        inicio = pagina.find('href="http')
        if inicio == -1:
            return None, 0
        inicio += 6
        fim = pagina.find('"', inicio)
        url = pagina[inicio:fim]

        return url, fim

    def getTodosLinks(self, pagina):
        lista = []
        while True:
            url, fim = self.getProximaPagina(pagina)
            if url:
                lista.append(url)
                pagina = pagina[fim:]
            else:
                break
        return lista

    def getPagina(self, url):
        f = requests.get(url)
        html = f.text
        return html

    def cascataDeLinks(self, al):
        print("THREAD %i:ALL LINKS"%(self.id))
        for s in al:
            print("     ", s)
        print("FIM")

    def run(self):
        print('THREAD %i iniciado '%(self.id))
        while paraBuscar:
            if nThreads > 0 and len(paraBuscar) > 2 : # se tiver apenas 1 link, esse mesmo thread faz
                novoThread()
            else:
                if (maximoPaginas != -1) and (len(navegados) > maximoPaginas):
                    print("THREAD %i finalizado: página %i/%i e depth %i/%i" % (self.id, len(navegados) + 1, maximoPaginas, depth + 1, nivelMaximo))
                    break
                proximo = popParaBuscar()
                url = proximo[0]
                depth = proximo[1]

                if nivelMaximo > -1 and depth >= nivelMaximo:
                    print("THREAD", self.id, "Nível máximo:",proximo)
                    continue

                try:
                    if url not in navegados and url not in errors:
                        print("THREAD %i Buscando página %i de %i com depth %i de %i: %s" % (self.id, len(navegados) + 1, maximoPaginas, depth + 1, nivelMaximo, url))
                        allLinks = self.getTodosLinks(self.getPagina(url))

                        print('THREAD %i Encontrado %i links' % (self.id,len(allLinks)))

                        for l in allLinks:
                            addParaBuscar(l, depth + 1)

                        #self.cascataDeLinks(allLinks)
                        mostrarParaBuscar(self.id)
                        addNavegado(url)

                except:
                    semaforoBuscar.acquire()
                    errors.append(url)
                    print("THREAD %i Não foi possível buscar página %s" %(self.id, url))
                    semaforoBuscar.release()

def mostrarParaBuscar(id):
    semaforoBuscar.acquire()
    print("THREAD %i: PARA BUSCAR:"%(id))
    for s in paraBuscar:
        print("Nivel", s[1], "URL", s[0])
    print("FIM")
    semaforoBuscar.release()

def mostrarLinksNavegados():
    semaforoBuscar.acquire()
    print("Links Navegados:")
    for s in navegados:
        print("URL", s)

    print("FIM")
    semaforoBuscar.release()

def novoThread():
    global paraBuscar, nThreads
    t = BuscarLinksNaWeb(nThreads)  # nThreads como ID
    t.start()

def popParaBuscar():
    global paraBuscar
    semaforoBuscar.acquire()
    proximaPagina = paraBuscar.pop()
    semaforoBuscar.release()
    return proximaPagina

def addNavegado(s):
    global navegados
    semaforoBuscar.acquire()
    navegados.append(s)
    semaforoBuscar.release()

def addParaBuscar(s, n):
    global paraBuscar
    semaforoBuscar.acquire()
    paraBuscar.append([s,n])
    semaforoBuscar.release()

def Main():
    global nThreads, maximoPaginas, nivelMaximo, paraBuscar

    paraBuscar.append(["https://codereview.stackexchange.com/questions/26165/accessing-a-global-list",0]) #input('Pagina inicial: ')
    nThreads = int(input("Maximo de Threads: "))
    maximoPaginas = int(input("Maximo de Paginas: "))
    nivelMaximo = int(input("Nível Maximo: "))
    novoThread()

Main()