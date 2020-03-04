'''
Angel David Cuellar
Carnet 18382
Hoja de trabajo 5

Basado en las paginas 26,27 de la documentacion de SimPy ejemplo 3.5.3
y el ejemplo 4.10.1 de la pagina 43 
'''

import random
import pandas
import simpy
import time
import statistics

RAMc = 100
CPU = 1
RANDOM_SEED = 10
PROCESOS = 50
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
    print("El %s (State: %s) se creo en %d" % (name,state, env.now))
    with RAM.RAMa.get(memoria) as req1:
        yield req1
        state = "READY"
        print("El %s (State: %s) obtiene %s de RAM en %d" % (name,state, memoria, env.now))
        print("%s" %(RAM.RAMa.level))
        siguiente = 0
        while datos >= 3 :
            with RAM.CPU.request() as req2:
                print("El %s (State: %s) espera espacio en CPU en %d" % (name, state, env.now))
                yield req2
                state = "RUNNING"
                print("El %s (State: %s) esta en CPU en %d" % (name,state,env.now))

                datos = datos - VELOCIDAD
                yield env.timeout(1)
                if datos >= 3:
                    siguiente = random.randint(1,2)
                
                
                if siguiente == 1:
                    print ("El %s esta en operaciones I/0 en %d" % (name, env.now))
                    yield env.timeout(IO)
            
        state = "TERMINATED"
        print("El %s (State:%s) en %d" % (name,state , env.now))
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


    
#Empezar la simulacion
print("ESTO ES UNA COMPUTADORA")
random.seed(RANDOM_SEED)
env = simpy.Environment()
RAMm = Memoria_RAM(env)
env.process(generador(env, PROCESOS, INTERVAL, RAMm))
env.run()


print("\n"*2)
print("--------------------RESUMEN DE LO SUCEDIDO--------------------------")
print("")
print("El tiempo promedio de cada proceso fue de ",statistics.mean(tiempo) )
print("con una desviacion estandard de los datos de ",statistics.stdev(tiempo))



