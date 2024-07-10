import simpy
import random

def customer(env, name):
    print(f'{name}: Arrives at time {env.now:.2f}')
    yield env.timeout(30)
    print(f'{name}: Details entered at time: {env.now:.2f}')
    yield env.timeout(60)
    print(f'{name}: Cash retrieved at time: {env.now:.2f}')

def customer_generator(env):
    cust_number=1
    while True:
        random_inter_arrival_time=random.uniform(1,3)*60
        yield env.timeout(random_inter_arrival_time)
        env.process(customer(env=env, name=f"Customer {cust_number}"))
        cust_number+=1

random.seed(2)

env=simpy.Environment()

env.process(customer_generator(env=env))

env.run(until=10*60)