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

RAMc = 100
CPU = 1
RANDOM_SEED = 10

PROCESOS = 10
INTERVAL = 10

tileREADY = []
tileWAIT = []

class Memoria_RAM:

    def __init__(self, env):
        self.CPU = simpy.Resource(env, capacity = CPU)
        self.RAMa = simpy.Container(env, init = RAMc, capacity = RAMc)
        #self.mon_proc = env.process(self.pantalla(env))

    
def procesof(env, name,state,RAM):
    
    here = env.nowc
    print("El proceso %s se creo en %s" % (name, here))
    with RAM.RAMs.request() as req:
        yield req
        instrucciones = random.randint(0,10)   
        yield RAM.RAMa.get(instrucciones)
        print("El proceso %s obtiene %s RAM en %s" % (name, instrucciones, env.now))
        
        
    
def generador(env, numero, intervalo, RAM):
    for i in range(numero):
        state = "NEW"
        p = procesof(env, "Proceso %02d" % i, state, RAM)
        env.process(p)
        t = random.expovariate(1.0 / intervalo)
        yield env.timeout(t)

#Empezar la simulacion
print("ESTO ES UNA COMPUTADORA")
random.seed(RANDOM_SEED)
env = simpy.Environment()
RAMm = Memoria_RAM(env)
proceso = env.process(generador(env, PROCESOS, INTERVAL,RAMm))
env.run()


