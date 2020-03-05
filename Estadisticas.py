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
INTERVAL = 1
VELOCIDAD = 3
IO = 1
tiempo = []

class Memoria_RAM:

    def __init__(self, env):
        self.CPU = simpy.Resource(env, capacity = CPU)
        self.RAMa = simpy.Container(env, init = RAMc, capacity = RAMc)
  

    
def procesof(env, name,state,RAM):
    inicio = env.now
    memoria = random.randint(1,10) #RAM que se va a utilizar  
    datos = random.randint(1,10) #Acciones a realizar en el CPU

    with RAM.RAMa.get(memoria) as req1:#Se retira la RAM a utilizar
        yield req1
        state = "READY"#Pasa a estado de ready

        siguiente = 0
        while datos >= 3 :#mientras aun hayan 3 datos o mas datos a tratar
            with RAM.CPU.request() as req2:#Se requiere atencion del CPU
                
                yield req2
                state = "RUNNING"
                

                datos = datos - VELOCIDAD#Se procesa en el cpu las instrucciones
                yield env.timeout(1)
                
                if datos >= 3:#se genera numero random para ver si seguir corriendo o hacer I/O
                    siguiente = random.randint(1,2)
                
                #Hace operaciones I/O
                if siguiente == 1:
                    state = "WAIT"
                    
                    yield env.timeout(IO)
                if siguiente == 0:
                    datos = 0
            
        state = "TERMINATED"
        RAM.RAMa.put(memoria)#Se regresa RAM utilizada
    fin = env.now
    tiempo.append(fin - inicio)#Se calcula tiempo de este processo
        
#Metodo que genera los procesos
def generador(env, numero, intervalo, RAM):
    for i in range(numero+1):
        t = random.expovariate(1.0 / intervalo) #intervalo de creacion   
        state = "WAIT"#se crean con estado de wait
        p =procesof(env, "Proceso %02d" % i, state, RAM)#se crea proceso
        env.process(p)
        yield env.timeout(t)#Tiempo que transcurrio para crear proceso



print("--------------------RESUMEN DE LO SUCEDIDO--------------------------")

def resumen(diccionario):
    encabezado = ["Procesos","Promedio","Desviacion"]
    df= pd.DataFrame(diccionario)
    print (tabulate(df, headers = encabezado, tablefmt = "grid"))
    df.plot(kind = "line",x = "Cantidad_de_Procesos", y = "Promedio", color="red", title = "Con intervalo de 1")
    
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





