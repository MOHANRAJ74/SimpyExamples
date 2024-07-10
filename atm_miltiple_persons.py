import simpy

CUST_INTER_ARR_TIME= 2*60

def customer(env, name):
    print(f'{name}: Arrives at time {env.now}')
    yield env.timeout(30)
    print(f'{name}: Details entered at time: {env.now}')
    yield env.timeout(60)
    print(f'{name}: Cash retrieved at time: {env.now}')

def customer_generator(env, cust_inter_arr_time):
    cust_number=1
    while True:
        yield env.timeout(cust_inter_arr_time)
        env.process(customer(env=env, name=f"Customer {cust_number}"))
        cust_number+=1

env=simpy.Environment()

env.process(customer_generator(env=env, cust_inter_arr_time=CUST_INTER_ARR_TIME))

env.run(until=10*60)