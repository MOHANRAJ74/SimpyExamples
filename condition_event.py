import simpy
import random
def customer(env, name, cashiers, fridge):
    milk_required=random.randint(1,5)
    print(f'{name}:  Arrives at time: {env.now: .2f}, and requires {milk_required}L milk.')

    with fridge['resource'].request() as fridge_req:
        res=yield fridge_req | env.timeout(10, value='timeout_10')
        # print(res)
        if fridge_req in res:
            yield env.timeout(milk_required)
            yield fridge['milk_container'].get(milk_required)
        else:
            print(f'{name}: left without buying milk at time: {env.now:.2f}.')
            return

    print(f'{name}: finishes retrieving the milk at time: {env.now: .2f}. Fridge has {fridge["milk_container"].level}L milk remaining')
    with cashiers.request() as cashier_req:
        yield cashier_req
        print(f'{name}: gets a cashier at time: {env.now: .2f}')
        yield env.timeout(2)
        print(f'{name}: leaves at time: {env.now: .2f}')

def customer_generator(env, cashiers, fridge):
    cust_number=1
    while True:
        random_inter_arrival_time=random.expovariate(lambd=0.5)
        yield env.timeout(random_inter_arrival_time)
        env.process(customer(env=env, name=f"customer {cust_number}", cashiers=cashiers, fridge=fridge))
        cust_number +=1

def fridge_control_process(env, fridge):
    while True:
        if fridge['milk_container'].level<5:
            yield env.process(fridge_refill_process(env, fridge))

        yield env.timeout(random.uniform(10,20))

def fridge_refill_process(env, fridge):
    print(f"Fridge refill process called at time {env.now: .2f}. Fridge has {fridge['milk_container'].level}L milk.")
    yield env.timeout(2)
    to_refill=15-fridge['milk_container'].level
    print(f"Fridge has {fridge['milk_container'].level}L milk. Fridge filled with {to_refill}L milk.")
    yield fridge['milk_container'].put(to_refill)

random.seed(2)

env=simpy.Environment()

cashiers=simpy.Resource(env=env, capacity=2)

fridge={'resource': simpy.Resource(env=env, capacity=1), 'milk_container': simpy.Container(env=env, capacity=50, init =15) }

env.process(customer_generator(env=env, cashiers=cashiers, fridge=fridge))

env.run(until=60)










