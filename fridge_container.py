import simpy
import random

def customer(env, name, cashiers, fridge):
    milk_required=random.randint(1,5)
    print(f'{name}:  Arrives at time: {env.now: .2f}, and requires {milk_required}L milk.')

    with fridge['resource'].request() as fridge_req:
        yield fridge_req
        yield env.timeout(milk_required)
        yield fridge['milk_container'].get(milk_required)

    print(f'{name}: finishes retrieving the milk at time: {env.now: .2f}. Fridge has {fridge["milk_container"].level}L milk remaining')
    with cashiers.request() as cashier_req:
        yield cashier_req
        print(f'{name}: gets a cashier at time: {env.now: .2f}')
        yield env.timeout(2)
        print(f'{name}: leaves at time: {env.now: .2f}')

def customer_generator(env, cashiers, fridge):
    cust_number=1
    while True:
        random_inter_arrival_time=random.expovariate(lambd=2)
        yield env.timeout(random_inter_arrival_time)
        env.process(customer(env=env, name=f"customer {cust_number}", cashiers=cashiers, fridge=fridge))
        cust_number +=1

random.seed(2)

env=simpy.Environment()

cashiers=simpy.Resource(env=env, capacity=2)

fridge={'resource': simpy.Resource(env=env, capacity=1), 'milk_container': simpy.Container(env=env, capacity=50, init =15) }

env.process(customer_generator(env=env, cashiers=cashiers, fridge=fridge))

env.run(until=30)



























