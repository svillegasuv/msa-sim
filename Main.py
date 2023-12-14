import random
from Simulacion import Simulacion
import matplotlib.pyplot as plt
import numpy as np
#Sim = Simulacion(100,20,20,0,0,19,19,0.20,0.20,4)
MAGNA_ITER = 1
ITER = 100
TAM_X = 50
TAM_Y = 50
TIPO_SIM = 0

def generateGraphs(graphData,graphDataDesv):
    plt.figure(1)
    figureData = []
    labelData = []
    for i in range(0,9):
        #print(graphData[i]['rsomatica'])
        figureData.append(graphData[i]['rsomatica'])
        labelData.append('E'+str(i+1))
    plt.boxplot(figureData,labels=labelData)
    plt.title("Reacciones Somáticas")
    plt.ylabel("Puntos Reacción Somática")
    plt.xlabel('Escenarios')
    plt.savefig(r'C:\Users\ST4RDUST\Desktop\city_sim\data\ReaccionesSomaticas.png', dpi=400)
    
    #Pie Plot de aceptaciones de viaje
    plt.figure(2)
    aprobados = []
    rechazados = []
    for i in range(0,9):
        aprobados.append(graphData[i]['evsomatica'][1])
        rechazados.append(graphData[i]['evsomatica'][0])
    b1 = plt.barh(labelData, aprobados, color="green")
    b2 = plt.barh(labelData, rechazados, left=aprobados, color="red")
    plt.legend([b1, b2], ["Aprueba", "Desaprueba"], title="Reacción Somática", loc="upper right")
    plt.gca().invert_yaxis()
    plt.xlabel("Cantidad de Aprobación de Segundo Pasajero")
    plt.ylabel("Escenarios")
    plt.title("Aprobacion de Segundo Pasajero (De "+str(ITER)+")")
    plt.savefig(r'C:\Users\ST4RDUST\Desktop\city_sim\data\Aprobacion.png', dpi=400)
    
    #Distribucion de caja de costos totales
    plt.figure(3)
    figureData = []
    for i in range(0,9):
        figureData.append(graphData[i]['costos'])
    plt.boxplot(figureData,labels=labelData)
    plt.title("Costos de Viaje sin desvío")
    plt.ylabel("Costos")
    plt.xlabel('Escenarios')
    plt.savefig(r'C:\Users\ST4RDUST\Desktop\city_sim\data\CostosTotales.png', dpi=400)
    
    #Distribucion de caja de costos totales con desvío
    plt.figure(4)
    figureData = []
    for i in range(0,9):
        figureData.append(graphDataDesv[i]['costos'])
    plt.boxplot(figureData,labels=labelData)
    plt.title("Costos de Viaje con desvío")
    plt.ylabel("Costos")
    plt.xlabel('Escenarios')
    plt.savefig(r'C:\Users\ST4RDUST\Desktop\city_sim\data\CostosTotalesDesv.png', dpi=400)
    
    #Distribucion de caja de tiempos totales
    plt.figure(5)
    figureData = []
    for i in range(0,9):
        figureData.append(graphData[i]['tiempos'])
    plt.boxplot(figureData,labels=labelData)
    plt.title("Tiempos de Viaje sin desvío")
    plt.ylabel("Tiempos")
    plt.xlabel('Escenarios')
    plt.savefig(r'C:\Users\ST4RDUST\Desktop\city_sim\data\TiemposTotales.png', dpi=400)
    
    #Distribucion de caja de tiempos totales con desvío
    plt.figure(6)
    figureData = []
    for i in range(0,9):
        figureData.append(graphDataDesv[i]['tiempos'])
    plt.boxplot(figureData,labels=labelData)
    plt.title("Tiempos de Viaje con desvío")
    plt.ylabel("Tiempos")
    plt.xlabel('Escenarios')
    plt.savefig(r'C:\Users\ST4RDUST\Desktop\city_sim\data\TiemposTotalesDesv.png', dpi=400)
    
    
    #Distribucion de caja de puntuaciones totales
    plt.figure(7)
    figureData = []
    for i in range(0,9):
        figureData.append(graphData[i]['evviaje'])
    plt.boxplot(figureData,labels=labelData)
    plt.title("Evaluación de Viajes sin desvío")
    plt.ylabel("Puntos")
    plt.xlabel('Escenarios')
    plt.savefig(r'C:\Users\ST4RDUST\Desktop\city_sim\data\EvalViajes.png', dpi=400)
    
    #Distribucion de caja de puntuaciones totales con desvío
    plt.figure(8)
    figureData = []
    for i in range(0,9):
        figureData.append(graphDataDesv[i]['evviaje'])
    plt.boxplot(figureData,labels=labelData)
    plt.title("Evaluación de Viajes con desvío")
    plt.ylabel("Puntos")
    plt.xlabel('Escenarios')
    plt.savefig(r'C:\Users\ST4RDUST\Desktop\city_sim\data\EvalViajesDesv.png', dpi=400)
    
    #plt.show()

#Origen 0 y Destino al otro borde
if(TIPO_SIM == 0):
    for i in range(0,MAGNA_ITER):
        graphData = []
        graphDataDesv = []
        for escenario in range(0,9):
            print("Escenario "+str(escenario)+":")
            data = Simulacion(ITER,TAM_X,TAM_Y,0,0,(TAM_X-1),(TAM_Y-1),0.20,0.20,escenario)
            graphData.append(data.graphData)
            graphDataDesv.append(data.graphDataDesv)
        generateGraphs(graphData,graphDataDesv)
        
if(TIPO_SIM == 1):
    #Origen y Destino Aleatorios
    for i in range(0,MAGNA_ITER):
        origX = random.randint(0,TAM_X - 1)
        origY = random.randint(0,TAM_Y - 1)
        destX = random.randint(0,TAM_X - 1)
        destY = random.randint(0,TAM_Y - 1)
        #Si el origen y el destino son el mismo, volver a generar
        while(origX == destX and origY == destY):
            origX = random.randint(0,TAM_X - 1)
            origY = random.randint(0,TAM_Y - 1)
            destX = random.randint(0,TAM_X - 1)
            destY = random.randint(0,TAM_Y - 1)
        for escenario in range(0,8):
            print("Escenario "+str(escenario)+":")
            Sim = Simulacion(ITER,TAM_X,TAM_Y,origX,origY,destX,destY,0.20,0.20,escenario)

#Conclusiones.
#-	Nivel de cumplimiento de objetivos.
#-	Limitaciones del presente estudio.
#-	Indicar tres posibles líneas de trabajo futuro o continuidad del actual trabajo.

''''
Discusión:
-	Referirte a los hallazgos derivados de los resultados.
-	En qué escenario(s) el agente pasajero 1 acepta el desvío de ruta. ¿qué implicancias tiene lo anterior? ¿qué beneficios potenciales para el agente pasajero 1, agente pasajero 2, y para la empresa de transporte?
-	¿Cuál es el nivel de aplicabilidad de la propuesta a un escenario real dentro de una ciudad? ¿Qué condiciones serían necesarias para aquello?
- Cuál es el efecto de uso de un marcador somático artificial
'''