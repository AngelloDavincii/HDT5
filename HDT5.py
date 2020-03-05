'''
Angel David Cuellar
Carnet 18382
Hoja de trabajo 5

Basado en las paginas 26,27 de la documentacion de SimPy ejemplo 3.5.3
y el ejemplo 4.10.1 de la pagina 43 
'''

import random
import simpy
import statistics

#PARAMETROS PARA CAMBIAR
RAMc = 100
CPU = 1
RANDOM_SEED = 5
PROCESOS = 50
INTERVAL = 10
VELOCIDAD = 3
IO = 1
tiempo = []

#Se crea clase para guardar memoria RAM y CPU
class Memoria_RAM:

    def __init__(self, env):
        self.CPU = simpy.Resource(env, capacity = CPU)
        self.RAMa = simpy.Container(env, init = RAMc, capacity = RAMc)
  

    
def procesof(env, name,state,RAM):
    inicio = env.now
    memoria = random.randint(1,10) #RAM que se va a utilizar  
    datos = random.randint(1,10) #Acciones a realizar en el CPU
    print("El %s (State: %s) se creo en %d" % (name,state, env.now))
    with RAM.RAMa.get(memoria) as req1:#Se retira la RAM a utilizar
        yield req1
        state = "READY"#Pasa a estado de ready
        print("El %s (State: %s) obtiene %s de RAM en %d" % (name,state, memoria, env.now))
        siguiente = 0
        while datos >= 3 :#mientras aun hayan 3 datos o mas datos a tratar
            with RAM.CPU.request() as req2:#Se requiere atencion del CPU
                print("El %s (State: %s) espera espacio en CPU en %d" % (name, state, env.now))
                yield req2
                state = "RUNNING"
                print("El %s (State: %s) esta en CPU en %d" % (name,state,env.now))

                datos = datos - VELOCIDAD#Se procesa en el cpu las instrucciones
                yield env.timeout(1)
                
                if datos >= 3:#se genera numero random para ver si seguir corriendo o hacer I/O
                    siguiente = random.randint(1,2)
                
                #Hace operaciones I/O
                if siguiente == 1:
                    state = "WAIT"
                    print ("El %s esta en operaciones I/0 en %d" % (name, env.now))
                    yield env.timeout(IO)
                if siguiente == 0:
                    datos = 0
            
        state = "TERMINATED"
        print("El %s (State:%s) en %d" % (name,state , env.now))
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


    
#Empezar la simulacion
print("ESTO ES UNA COMPUTADORA")
random.seed(RANDOM_SEED)#Se le coloca semilla al random para poder hacer comparaciones
env = simpy.Environment()#Se crea el envirnment
RAMm = Memoria_RAM(env) #Se renombra la memoriaRAM
env.process(generador(env, PROCESOS, INTERVAL, RAMm))#Se crea el proceso
env.run()#Se corre hasta que se acaben los procesos

#RESUMEN
#VER EL ARCHIVO DE ESTADISTICAS PARA VER MEJOR EL RESUMEN Y COMO SE OBTUVIERON PLOTS
print("\n"*2)
print("--------------------RESUMEN DE LO SUCEDIDO--------------------------")
print("")
print("El tiempo promedio de cada proceso fue de ",statistics.mean(tiempo) )
print("con una desviacion estandard de los datos de ",statistics.stdev(tiempo))



