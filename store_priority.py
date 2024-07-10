#list of random vegatables
import random
import simpy

#Produer Process
def producer(env,store):
    while True:
        yield env.timeout(2)
        vegetable_name='potato'
        expires_in=env.now+random.randint(1,10)
        vegetable=simpy.PriorityItem(priority=expires_in, item=vegetable_name)
        yield store.put(vegetable)
        print(f'Produced {vegetable} at {env.now: .2f}.')

def customer(name,env, store):
    print(f'Customer {name} arrives and requests potato at time {env.now: .2f}.')
    vegetable=yield store.get()
    print(f'Customer {name} got {vegetable} at {env.now: 2f} and leaves.')

def customer_generator(env,store):
    i=0
    while True:
        yield env.timeout(1)
        env.process(customer(name=i, env=env, store=store))
        i+=1

env=simpy.Environment()

store=simpy.Store(env, capacity=5)

#start producer
env.process(producer(env, store))

#start customer generator process
env.process(customer_generator(env, store))

env.run(until=20)