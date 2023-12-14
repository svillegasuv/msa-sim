import random
from Calle import Calle
from Ciudad import Ciudad

class BuscaCaminos: 
    MAX_TIPOS = 5
    # Instance attribute
    def __init__(self, grilla,TAM_X,TAM_Y):
        self.nodos = grilla.getNodos()
        self.TAM_X = TAM_X 
        self.TAM_Y = TAM_Y
        self.DEST_X = None
        self.DEST_Y = None
        self.abierto = []
        self.cerrado = []
        self.camino = []
        self.actual = None
        self.prefTipo = []

    def encontrarCamino(self,INIT_X,INIT_Y,DEST_X,DEST_Y):
        #Refresco de variables
        self.DEST_X = DEST_X 
        self.DEST_Y = DEST_Y
        self.prefTipo = []
        for i in range(0,BuscaCaminos.MAX_TIPOS):
            self.prefTipo.append(random.randint(-50,500))
        self.abierto = []
        self.cerrado = []
        self.camino = []
        self.actual = Calle(None, INIT_X, INIT_Y,0,0)
        self.actual.tipo = self.nodos[self.actual.x][self.actual.y].tipo
        self.cerrado.append(self.actual)
        self.ingVecinosADisp()
        while(self.actual.x != DEST_X or self.actual.y != DEST_Y):
            #if(not self.abierto):
            #    return None
            self.actual = self.abierto[0]
            self.abierto.pop(0)
            self.cerrado.append(self.actual)
            self.ingVecinosADisp()
        self.camino.insert(0,self.actual)
        while(self.actual.x != INIT_X or self.actual.y != INIT_Y):
            self.actual = self.actual.padre
            self.camino.insert(0,self.actual)
        return self.camino
    
    #Verificar si se ha interactuado con bloque de grilla
    def encVecinosEnLista(self,lista, nodo): 
        for i in lista:
            if(i.x == nodo.x and i.y == nodo.y):
                return True
        #Si no se encontro equivalencia
        return False
 
    def ingVecinosADisp(self):
        for x in range(-1,2):
            for y in range(-1,2):
                if(x != 0 and y != 0):
                    continue #Evitar movimiento diagonal
                
                nodo = Calle(self.actual, self.actual.x+x,self.actual.y+y,self.actual.g,self.distancia(x,y))
                if((x != 0 or y != 0)
                and self.actual.x+x >= 0 and self.actual.x+x < self.TAM_X #Verificar que no salgo de los bordes de la grilla
                and self.actual.y+y >= 0 and self.actual.y+y < self.TAM_Y
                and self.nodos[self.actual.y+y][self.actual.x+x].getCosto(self.prefTipo) != -1 #Verificar si puede desplazarse
                and not self.encVecinosEnLista(self.abierto, nodo) and not self.encVecinosEnLista(self.cerrado,nodo)):
                    gAux = nodo.padre.g+1.0 # Horizontal/vertical cost = 1.0
                    gAux += self.nodos[self.actual.y+y][self.actual.x+x].getCosto(self.prefTipo)
                    nodo.g = gAux
                    trueGAux = nodo.padre.trueG+1.0
                    trueGAux += self.nodos[self.actual.y+y][self.actual.x+x].getCostoAlt()
                    nodo.trueG = trueGAux
                    nodo.tipo = self.nodos[nodo.x][nodo.y].tipo
                    self.abierto.append(nodo)
        self.abierto.sort(key=lambda x: x.g,)
    
    def distancia(self,dx,dy):
        return abs(self.actual.x+dx - self.DEST_X) + abs(self.actual.y+dy - self.DEST_Y)
