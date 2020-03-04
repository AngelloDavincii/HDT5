'''
Angel David Cuellar
Carnet 18382
Hoja de trabajo 5

Basado en las paginas 26,27 de la documentacion de SimPy ejemplo 3.5.3
y el ejemplo 4.10.1 de la pagina 43 
'''

import random
import pandas as pd
from tabulate import tabulate
import simpy
import statistics
import matplotlib.pyplot as plt

RAMc = 100
CPU = 1
RANDOM_SEED = 10
PROCESOS = [25,50,100,150,200,250,300]
INTERVAL = 10
VELOCIDAD = 3
IO = 1
tiempo = []

class Memoria_RAM:

    def __init__(self, env):
        self.CPU = simpy.Resource(env, capacity = CPU)
        self.RAMa = simpy.Container(env, init = RAMc, capacity = RAMc)
        #self.mon_proc = env.process(self.pantalla(env))

    
def procesof(env, name,state,RAM):
    inicio = env.now

    memoria = random.randint(1,10)   
    datos = random.randint(1,10)
    with RAM.RAMa.get(memoria) as req1:
        yield req1
        state = "READY"
       
        siguiente = 0
        while datos >= 3 :
            with RAM.CPU.request() as req2:
                
                yield req2
                state = "RUNNING"
            
                datos = datos - VELOCIDAD
                yield env.timeout(1)
                if datos >= 3:
                    siguiente = random.randint(1,2)
                
                
                if siguiente == 1:
                    
                    yield env.timeout(IO)
            
        state = "TERMINATED"
        RAM.RAMa.put(memoria)
    fin = env.now
    tiempo.append(fin - inicio)
        
    
def generador(env, numero, intervalo, RAM):
    for i in range(numero+1):
        state = "WAIT"
        
        p = procesof(env, "Proceso %02d" % i, state, RAM)
        env.process(p)
        t = random.expovariate(1.0 / intervalo)
        yield env.timeout(t)
print("--------------------RESUMEN DE LO SUCEDIDO--------------------------")

def resumen(diccionario):
    encabezado = ["Procesos","Promedio","Desviacion"]
    df= pd.DataFrame(diccionario, columns = ["Cantidad_de_Procesos","Promedio","Desviacion"])
    print (tabulate(df, headers = encabezado, tablefmt = "grid"))
    df.plot(x = "Cantidad_de_Procesos", y = "Promedio", kind ="scatter")
    plt.show()
    
#Empezar la simulacion
def procesando():
    datos = {"Cantidad_de_Procesos":[],"Promedio":[],"Desviacion":[]}
    for i in PROCESOS:
        random.seed(RANDOM_SEED)
        env = simpy.Environment()
        RAMm = Memoria_RAM(env)
        env.process(generador(env, i, INTERVAL, RAMm))
        env.run()
        
        
        a = statistics.mean(tiempo)
        b = statistics.stdev(tiempo)
        datos["Cantidad_de_Procesos"].append(i)
        datos["Promedio"].append(a)
        datos["Desviacion"].append(b)

    return datos

revista = procesando()
resumen(revista)





