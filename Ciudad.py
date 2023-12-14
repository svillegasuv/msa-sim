import random
import numpy as np
from Calle import Calle



class Ciudad: 
    COSTO_BASE = 100
    
    # Instance attribute
    def __init__(self, TAM_X,TAM_Y,RATIO_X,RATIO_Y,TipoGen):
        self.TAM_X = TAM_X
        self.TAM_Y = TAM_Y
        self.RATIO_X = RATIO_X
        self.RATIO_Y = RATIO_Y
        self.TipoGen = TipoGen
        self.nodos = []
        random.seed(100)
        
        #Generar nodos
        for i in range(0,TAM_Y):
            #Genero una fila
            nodos_row = []
            for j in range(0,TAM_X):
                #Lleno la fila de X nodos
                nodo = Calle("",j,i,0,100)
                nodo.costo_viaje = Ciudad.COSTO_BASE
                nodos_row.append(nodo)
            #La añado a la matriz 2D
            self.nodos.append(nodos_row)            
        #Asigno tipos a carreteras
        #Ratios de bloques
        bTam_x = int(self.TAM_X*self.RATIO_X)
        bCant_x = int(1/RATIO_X)
        bTam_y = int(TAM_Y*RATIO_Y)
        bCant_y = int(1/RATIO_Y)

        if(self.TipoGen == 0):
            #Generacion por bloques
            for i in range(0,bCant_y):
                for j in range(0,bCant_x):
                    #Eleccion aleatoria de tipo de bloques
                    tipoSet = random.randint(0,3)
                    for k in range(0,bTam_y):
                        for l in range(0,bTam_x):
                            self.nodos[k+bTam_y*i][l+(bTam_x*j)].tipo=tipoSet
                            #Terminar de rellenar bloques vacios cerca de los bordes
                            #Eje X
                            if(l == (bTam_x-1) and l+(bTam_x*j) != (self.TAM_X-1)):
                                lAux = l+(bTam_x*j)
                                while(lAux < self.TAM_X):
                                    self.nodos[k+bTam_y*i][lAux].tipo=tipoSet
                                    lAux = lAux+1
                            #Eje X
                            if(k == (bTam_y-1) and k+(bTam_y*j) != (self.TAM_Y-1)):
                                kAux = k+(bTam_x*i)
                                while(kAux < self.TAM_Y):
                                    self.nodos[kAux][l+(bTam_x*j)].tipo=tipoSet
                                    kAux = kAux+1
        if(self.TipoGen == 1):
            #Generacion Aleatoria
            for i in range(0,TAM_Y):
                for j in range(0,TAM_X):
                    #Eleccion aleatoria de tipo de bloques
                    self.nodos[i][j].tipo=random.randint(0,3)

    def getNodos(self):
        #Retorna copia profunda de los nodos
        nodosAux = []
        for i in range(0,self.TAM_Y):
            callesAux = []
            for j in range(0,self.TAM_X):
                costoAux = Ciudad.COSTO_BASE
                tipoAux = self.nodos[i][j].tipo
                nodoAux = Calle("",i,j,0,0)
                nodoAux.costo_viaje = costoAux
                nodoAux.tipo = tipoAux
                callesAux.append(nodoAux)
            nodosAux.append(callesAux)
        return nodosAux

'''''
city = Ciudad(50,50,0.1,0.1,True)
for i in range(0,50):
    for j in range(0,50):
       print(city.nodos[i][j].tipo, end=" ")
    print("")
'''