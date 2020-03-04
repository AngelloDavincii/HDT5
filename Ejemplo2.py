import simpy

#
# el carro se conduce un tiempo y tiene que llegar a cargarse de energia
# luego puede continuar conduciendo
# Debe hacer cola (FIFO) en el cargador

# name: identificacion del carro
# bcs:  cargador de bateria
# driving_time: tiempo que conduce antes de necesitar carga
# charge_duration: tiempo que toma cargar la bateria

def car(env, name, bcs, driving_time, charge_duration):
    # Simulate driving to the BCS
    yield env.timeout(driving_time)

    # Request one of its charging spots
    print('%s arriving at %d' % (name, env.now))
    
    with bcs.request() as req:  #pedimos conectarnos al cargador de bateria
        yield req

        # Charge the battery
        print('%s starting to charge at %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s leaving the bcs at %s' % (name, env.now))
        # se hizo release automatico del cargador bcs
    
    
#
env = simpy.Environment()  #crear ambiente de simulacion
bcs = simpy.Resource(env, capacity=2) #el cargador de bateria soporta 2 carros
                                      #a la vez

# crear los carros
for i in range(5):
    env.process(car(env, 'Car %d' % i, bcs, i*2, 5))

# correr la simulacion
env.run()
    
