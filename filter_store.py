import random
import simpy
#list of random vegatables
veggies=['carrot','potato','onion','cabbage']
#Produer Process
def producer(env,store):
    while True:
        yield env.timeout(2)
        vegetable= random.choice(veggies)
        yield store.put(vegetable)
        print(f'Produced {vegetable} at {env.now: .2f}.')

def customer(name,env, store):
    reqd_veg=random.choice(veggies)
    print(f'Customer {name} arrives and requests vegetable {reqd_veg} at time {env.now: .2f}.')
    vegetable=yield store.get(lambda vegetable: vegetable==reqd_veg)
    print(f'Customer {name} got {vegetable} at {env.now: 2f} and leaves.')

def customer_generator(env,store):
    i=0
    while True:
        yield env.timeout(1)
        env.process(customer(name=i, env=env, store=store))
        i+=1

env=simpy.Environment()

store=simpy.FilterStore(env, capacity=5)

#start producer
env.process(producer(env, store))

#start customer generator process
env.process(customer_generator(env, store))

env.run(until=20)