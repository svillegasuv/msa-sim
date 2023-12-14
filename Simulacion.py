import random
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from Calle import Calle
from Ciudad import Ciudad
from BuscaCaminos import BuscaCaminos

class Simulacion: 
    # Instance attribute
    def __init__(self, ITER, TAM_X,TAM_Y,INIT_X,INIT_Y,DEST_X,DEST_Y,RATIO_X,RATIO_Y,escenario):
        self.ITER = ITER
        self.TAM_X = TAM_X 
        self.TAM_Y = TAM_Y
        self.INIT_X = INIT_X
        self.INIT_Y = INIT_Y
        self.DEST_X = DEST_X
        self.DEST_Y = DEST_Y
        self.RATIO_X = RATIO_X
        self.RATIO_Y = RATIO_Y
        self.graphData = {}
        if(escenario == -1):
            self.escenario = random.randint(0,8)
        else:
            self.escenario = escenario
        self.costosTotales = np.array([])
        self.costosTotalesDesv = np.array([])
        self.bloquesTotales = np.array([])
        self.bloquesTotalesDesv = np.array([])
        self.puntuacionesTotales = np.array([])
        self.puntuacionesTotalesDesv = np.array([])
        self.tiemposTotales = np.array([])
        self.tiemposTotalesDesv = np.array([])
        self.rSomaticas = np.array([])
        self.evalSomaticas = np.array([])
        self.grilla = Ciudad(TAM_X,TAM_Y,RATIO_X,RATIO_Y,1)
        
        
        
        self.initViaje()
    
    def initViaje(self):
        iters = []
        for i in range(0,self.ITER):
            costoTotalPerf = 0
            puntTotalPerf = 0
            tTotalPerf = 0
            bRecorrPerf = 0

            costoTotal = 0
            puntTotal = 0
            tTotal = 0
            bRecorr = 0
            
            

            buscador = BuscaCaminos(self.grilla,self.TAM_X,self.TAM_Y)
            viajePerfecto = buscador.encontrarCamino(self.INIT_X,self.INIT_Y,self.DEST_X,self.DEST_Y)
            #print(viajePerfecto)
            costoTotalPerf += viajePerfecto[len(viajePerfecto) -1].g
            bRecorrPerf = len(viajePerfecto)
            for k in range(0,len(viajePerfecto)):
                tTotalPerf += viajePerfecto[k].getCostoT()
                puntTotalPerf += viajePerfecto[k].getPuntTipo()
            #self.imprimirRuta(viajes)

            #Elegir punto aleatorio en el viaje por el cual desviar
            puntoDesv = random.randint(15,int(len(viajePerfecto)/2))
            oDesv_x = viajePerfecto[puntoDesv].x
            oDesv_y = viajePerfecto[puntoDesv].y
            #Generar nuevo punto de destino aleatorio
            dDesv_x = random.randint(0,self.TAM_X - 1)
            dDesv_y = random.randint(0,self.TAM_Y - 1)
            #Evitar que el punto de desvio sea igual al destino
            while(dDesv_x == self.DEST_X and dDesv_y == self.DEST_Y):
                dDesv_x = random.randint(0,self.TAM_X - 1)
                dDesv_y = random.randint(0,self.TAM_Y - 1)
            #Generar viaje desde desvio a destino aleatorio
            viajeDesv = buscador.encontrarCamino(oDesv_x,oDesv_y,dDesv_x,dDesv_y)
            #Generar origen del viaje final
            oFin_x = viajeDesv[-1].x
            oFin_y = viajeDesv[-1].y
            #Generar viaje final 
            viajeFinal = buscador.encontrarCamino(oFin_x,oFin_y,self.DEST_X,self.DEST_Y)
            #Consolidar viajes para mostrar
            viajeCompleto = []
            viajeCompleto.append(viajePerfecto[:puntoDesv])
            viajeCompleto.append(viajeDesv)
            viajeCompleto.append(viajeFinal)
            #Suma de todos los costos de los viajes individuales
            costoTotal += viajePerfecto[puntoDesv].g + viajeDesv[len(viajeDesv) -1].g + viajeFinal[len(viajeFinal)-1].g
            
            bRecorr = len(viajeCompleto)
            for viaje in viajeCompleto:
                for k in range(0,len(viaje)):
                    tTotal += viaje[k].getCostoT()
                    puntTotal += viaje[k].getPuntTipo()

            
            aceptaViaje = self.reaccionSomatica(costoTotal,tTotal,viajePerfecto[-1].g,tTotalPerf)
            viajeElegido = []
            if(aceptaViaje):
                costoIter = costoTotal
                bRecorrIter = bRecorr
                tTotalIter = tTotal
                pTotalIter = puntTotal
                viajeElegido = viajeCompleto
                #Añadir True a somaticas
                self.evalSomaticas = np.append(self.evalSomaticas,1)
                #print("Acepto Viaje")
                self.costosTotalesDesv = np.append(self.costosTotalesDesv,costoIter)
                self.bloquesTotalesDesv = np.append(self.bloquesTotalesDesv,bRecorrIter)
                self.tiemposTotalesDesv = np.append(self.tiemposTotalesDesv,tTotalIter)
                self.puntuacionesTotalesDesv = np.append(self.puntuacionesTotalesDesv,pTotalIter)
                if(self.escenario == 0):
                    self.imprimirRuta(viajeElegido,oDesv_x,oDesv_y,dDesv_x,dDesv_y,i)
                
            else:
                costoIter = costoTotalPerf
                bRecorrIter = bRecorrPerf
                tTotalIter = tTotalPerf
                pTotalIter = puntTotalPerf
                viajeElegido.append(viajePerfecto)
                #Añadir False a somaticas
                self.evalSomaticas = np.append(self.evalSomaticas,0)
                #Datos perfectos
                self.costosTotales = np.append(self.costosTotales,costoIter)
                self.bloquesTotales = np.append(self.bloquesTotales,bRecorrIter)
                self.tiemposTotales = np.append(self.tiemposTotales,tTotalIter)
                self.puntuacionesTotales = np.append(self.puntuacionesTotales,pTotalIter)
                #print("Rechazo Viaje")
            
            
            

            #print("Iteración: "+str(i+1)+", Costo de viaje: $"+str(costoIter)+", Bloques Recorridos: "+str(bRecorrIter)+", Tiempo de viaje: "+ str(tTotalIter)+", Puntuación Viaje: "+str(pTotalIter))
            
        #Fin de simulación, consolidación de datos
        #Distribucion de caja de reacciones somaticas
        print("Promedios:")
        print("Costos: "+str(np.mean(self.costosTotales))+" Bloques Recorridos: "+str(np.mean(self.bloquesTotales))+" Tiempos: "+str(np.mean(self.tiemposTotales))+" Puntuacion: "+str(np.mean(self.puntuacionesTotales))+" Somatica: "+str(np.mean(self.rSomaticas)))
        iters = {
                
                'Eval Somatica':self.evalSomaticas,
                'Punt Somatica':self.rSomaticas,
            }
        iterNoDesv = {
            'Eval Viajes':self.puntuacionesTotales,
            'Costos':self.costosTotales,
            'Tiempos':self.tiemposTotales,
        }
        iterDesv = {
            'Eval Viajes':self.puntuacionesTotalesDesv,
            'Costos':self.costosTotalesDesv,
            'Tiempos':self.tiemposTotalesDesv,
        }
        
                
        df = pd.DataFrame(iters)
        df.to_csv(r'C:\Users\ST4RDUST\Desktop\city_sim\data\csv\Escenario_'+str(self.escenario)+'.csv', index=False, sep = ',')
        df = pd.DataFrame(iterNoDesv)
        df.to_csv(r'C:\Users\ST4RDUST\Desktop\city_sim\data\csv\Escenario_'+str(self.escenario)+'_NoDesv.csv', index=False, sep = ',')
        df = pd.DataFrame(iterDesv)
        df.to_csv(r'C:\Users\ST4RDUST\Desktop\city_sim\data\csv\Escenario_'+str(self.escenario)+'_Desv.csv', index=False, sep = ',')
        '''''
        proms = {
                'Costos':[np.mean(self.costosTotales)],
                'Aprobacion Somatica':[(np.sum(self.evalSomaticas == 1) / len(self.evalSomaticas)) * 100],
                'Punt Somatica':[np.mean(self.rSomaticas)],
                'Tiempos':[np.mean(self.tiemposTotales)],
                'Eval Viajes':[np.mean(self.puntuacionesTotales)],
            }
        df = pd.DataFrame(proms)
        df.to_csv(r'.\Desktop\city_sim\data\csv\Escenario_'+str(self.escenario)+'_Proms.csv', index=False, sep = ',')
        '''
        
        
        self.graphData = {
                'costos':self.costosTotales,
                'evsomatica':[np.sum(self.evalSomaticas == 0),np.sum(self.evalSomaticas == 1)],
                'rsomatica':self.rSomaticas,
                'tiempos':self.tiemposTotales,
                'evviaje':self.puntuacionesTotales,
            }
        
        self.graphDataDesv = {
                'costos':self.costosTotalesDesv,
                'evsomatica':[np.sum(self.evalSomaticas == 0),np.sum(self.evalSomaticas == 1)],
                'rsomatica':self.rSomaticas,
                'tiempos':self.tiemposTotalesDesv,
                'evviaje':self.puntuacionesTotalesDesv,
            }
        '''''
        
        
            
        plt.figure(1)
        plt.boxplot(self.rSomaticas)
        plt.title("Reacciones Somáticas")
        plt.ylabel("Puntos Reacción Somática")
        
        #Pie Plot de aceptaciones de viaje
        plt.figure(2)
        plt.title("Aprobacion")
        pieData = [np.sum(self.evalSomaticas == 0),np.sum(self.evalSomaticas == 1)]
        plt.pie(pieData,labels=("Rechaza","Acepta"))
        
        #Distribucion de caja de costos totales
        plt.figure(3)
        plt.title("Costos de Viaje")
        plt.ylabel("Costos")
        plt.boxplot(self.costosTotales)
        
        #Distribucion de caja de tiempos totales
        plt.figure(4)
        plt.title("Tiempos de Viaje")
        plt.ylabel("Tiempos")
        plt.boxplot(self.tiemposTotales)
        
        #Distribucion de caja de puntuaciones totales
        plt.figure(5)
        plt.title("Puntuacion de Viajes")
        plt.ylabel("Puntos")
        plt.boxplot(self.puntuacionesTotales)
        
        plt.show()
        '''
        

    def imprimirRuta(self, viajes,oDesv_x,oDesv_y,dDesv_x,dDesv_y,iter):
        imagen = [[0 for x in range(self.TAM_X)] for y in range(self.TAM_Y)] 
        nodos = self.grilla.getNodos()
        for k in range(0,len(viajes)):
            viaje = viajes[k]
            if(viaje != None):
                for n in viaje:
                    nodos[n.y][n.x].traversado += 1
        for i in range(0,self.TAM_Y):
            for j in range(0,self.TAM_X):
                if(nodos[i][j].traversado > 0):
                    if(nodos[i][j].traversado > 1):
                        #print("#", end=" ")
                        imagen[j][i] = 5
                    else:
                        if(i == self.INIT_Y and j == self.INIT_X):
                            #print("U", end=" ")
                            imagen[j][i] = 6
                            continue
                        if(i == self.DEST_Y and j == self.DEST_X):
                            #print("H", end=" ")
                            imagen[j][i] = 7
                            continue
                        #print("*", end=" ")
                        imagen[j][i] = 4
                else:
                    #print(nodos[i][j].tipo, end=" ")
                    imagen[j][i] = nodos[i][j].tipo
            #print()
        #print("\n\n")
        imagen[oDesv_x][oDesv_y] =  6
        imagen[dDesv_x][dDesv_y] =  7
        colors = ['#b7bd13', '#8f2121', '#05d3f7', '#3fc406', '#000000','#757575','#ffffff','#ff0000']
        plt.figure(0)
        cmap = mpl.colors.ListedColormap(colors)
        plt.imshow(imagen, interpolation='none', cmap=cmap)
        #plt.show()
        plt.savefig(r'C:\Users\ST4RDUST\Desktop\city_sim\data\viajes\viaje_'+str(iter)+'.png', dpi=400)
    
    def reaccionSomatica(self, costoTotal, tTotal,costoPerf,tPerf):
        #Procesamiento de variables de entrada
        '''''
        difCosto = costoTotal-costoPerf
        difT = tTotal - tPerf
        prcDifCosto = (costoTotal/costoPerf)
        prcDifT = (tTotal/tPerf)
        print("CostoTotal: "+str(costoTotal)+" CostoPerf: "+str(costoPerf))
        print("Diferencia Costos: "+str(difCosto)+" Porcentaje Dif Costos: "+str(prcDifCosto))
        print("tTotal: "+str(tTotal)+" tPerf: "+str(tPerf))
        print("Diferencia Tiempos: "+str(difT)+" Porcentaje Dif Tiempos: "+str(prcDifT))
        print()
        '''
        prcDifCosto = (costoTotal/costoPerf)
        prcDifT = (tTotal/tPerf)
        #Definicion de escenario
        #print(prcDifCosto)
        costoNorm = 1000*prcDifCosto
        tStand = 1000*prcDifT
        #print(tStand)
        puntPas2 = random.randint(600,1500)
        factImp1 = 0.3
        factImp2 = 0.3
        factImp3 = 0.3
        umbral = random.randint(1000,1800)
        if(self.escenario == 0):
            factImp1 = 0.9
        elif(self.escenario == 1):
            factImp2 = 0.9
        elif(self.escenario == 2):
            factImp3 = 0.9
        elif(self.escenario == 3):
            factImp1 = 0.9
            umbral= umbral*0.9 #10% por debajo del umbral
        elif(self.escenario == 4):
            factImp2 = 0.9
            umbral= umbral*0.9 #10% por debajo del umbral
        elif(self.escenario == 5):
            factImp3 = 0.9
            umbral= umbral*0.9 #10% por debajo del umbral
        elif(self.escenario == 6):
            factImp1 = 0.9
            umbral= umbral*1.1 #10% por encima del umbral
        elif(self.escenario == 7):
            factImp2 = 0.9
            umbral= umbral*1.1 #10% por encima del umbral
        elif(self.escenario == 8):
            factImp3 = 0.9
            umbral= umbral*1.1 #10% por encima del umbral
        else:
            factImp3 = 0.9

        #Funcion somatica
        descuento = costoNorm*random.uniform(0.85, 1)
        factorCaos = random.uniform(0.8, 1.1)
        #print(factorCaos)
        #print(tNorm,puntPas2,descuento)
        FSom = (((tStand)*factImp1)+((puntPas2)*factImp2)+((descuento)*factImp3))*(factorCaos)
        self.rSomaticas = np.append(self.rSomaticas,FSom)
        #print("Funcion Somática: "+str(FSom))
        #print(FSom)
        #print(umbral)
        #print(FSom)

        if(FSom < umbral):
            return True
        else:
            return False

'''''
Ecuaciones sobre como se determinan tiempo costo y puntos
Eliminar calles dañada
Capítulo 4 incorpora definicion del problema, objetivos metodologia
Cap 7 abs 8 absorbe 9 y 10
Tabla que le da valores a las variables de simulacion

Objetivos pasa a Casos de Estudio
Objetivo general pasa a caso general

cap 7 cambia a diseño de escenario

'''