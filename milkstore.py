import simpy
import random
def customer(env, name, cashiers):
    milk_required = random.randint(1, 5)
    print(f'{name}: Arrives at time: {env.now:2f}, and requires {milk_required}L milk')
    yield env.timeout(milk_required)
    print(f'{name}: finishes retrieving the milk at time: {env.now: .2f}.')
    with cashiers.request() as cashier_req:
        yield cashier_req
        print(f'{name}: gets a cashier at time: {env.now : 2f}.')
        yield env.timeout(2)
        print(f'{name}: Leaves at time: {env.now: 2f}')
def customer_generator(env, cashiers):
    cust_number = 1
    while True:
        random_inter_arrival_time = random.expovariate(lambd=2)
        yield env.timeout(random_inter_arrival_time)
        env.process(customer(env=env, name=f"customer {cust_number}", cashiers=cashiers))
        cust_number += 1

env = simpy.Environment()
cashiers = simpy.Resource(env=env, capacity=2)
env.process(customer_generator(env=env, cashiers=cashiers))
env.run(until=10)