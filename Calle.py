class Calle:
 
    # class attribute

 
    # Instance attribute
    def __init__(self, padre,x,y,g,h):
        self.padre = padre
        self.x = x
        self.y = y
        self.g = g
        self.trueG = g
        self.h = h
        self.tipo = 0
        self.costo_viaje = 0
        self.traversado = 0

    ''''
    Tipos:
    0: Calle normal
    1: Calle Insegura :0
    2: Calle le turistica
    3: Calle Congestionada
    4: Calle rápida (?)
    '''
    def getCosto(self,prefTipo):
        if(self.tipo == 0):
            return self.costo_viaje+prefTipo[0]
        elif(self.tipo == 1):
            return self.costo_viaje+prefTipo[1]
        elif(self.tipo == 2):
            return self.costo_viaje+prefTipo[2]
        elif(self.tipo == 3):
            return self.costo_viaje+prefTipo[3]
        else:
            return self.costo_viaje+prefTipo[0]
            
    def getCostoAlt(self):
        
        if(self.tipo == 0):
            return self.costo_viaje
        elif(self.tipo == 1):
            return self.costo_viaje
        elif(self.tipo == 2):
            return self.costo_viaje
        elif(self.tipo == 3):
            return self.costo_viaje
        else:
            return self.costo_viaje

    def getCostoT(self):
        
        if(self.tipo == 0):
            return 1
        elif(self.tipo == 1):
            return 1
        elif(self.tipo == 2):
            return 1.5
        elif(self.tipo == 3):
            return 0.5
        else:
            return 1
    
    def getPuntTipo(self):
        
        if(self.tipo == 0):
            return 2
        elif(self.tipo == 1):
            return -2
        elif(self.tipo == 2):
            return 5
        elif(self.tipo == 3):
            return 4
        else:
            return 1

    #def __eq__(self,other):
 
# Driver code
# Object instantiation
#Rodger = Calle("",0,0,0,0)

 
# Accessing class attributes
#print("Rodger is a {}".format(Rodger.__class__.attr1))
#print("Tommy is also a {}".format(Tommy.__class__.attr1))
 
# Accessing instance attributes
#print("My name is {}".format(Rodger.tipo))
#print(Rodger.getCosto())
#print("My name is {}".format(Tommy.name))