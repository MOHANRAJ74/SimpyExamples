import simpy
import random
import numpy as np

SIM_TIME =34*60*60
WARMUP_TIME= 1*60*60

ct_simulation=[]
ct_replication=[]
waiting_time_simulation=[]
waiting_time_replication=[]
throughput_simulation=[]
def customer(env, name, atm):
    #print(f'{name}: Arrives at time: {env.now: .2f}')
    customer_enter_time=env.now
    with atm.request() as atm_req:
        yield atm_req
        customer_got_atm=env.now
        #print(f'{name}: gets ATM machine at time: {env.noe: .2f}')
        yield env.timeout(30)
        #print('{name}: Details entered at time: {env.now: .2f}')
        yield env.timeout(60)
        #print(f'{name}: Cash retrieved at time: {env.now: .2f}')

    if env.now > WARMUP_TIME:
        waiting_time_replication.append(customer_got_atm-customer_enter_time)
        ct_replication.append(env.now - customer_enter_time)

def customer_generator(env, atm):
    cust_number=1
    while True:
        random_inter_arrival_time=random.uniform(1,3)*60
        yield env.timeout(random_inter_arrival_time)
        env.process(customer(env=env, name=f"customer {cust_number}", atm=atm))
        cust_number+=1

for r in range(50):
    random.seed(r)

    env=simpy.Environment()
    atm=simpy.Resource(env=env, capacity=1)

    env.process(customer_generator(env=env, atm=atm))

    env.run(until=SIM_TIME) #24 hrs

    ct_simulation.append(np.mean(ct_replication))
    waiting_time_simulation.append(np.mean(waiting_time_replication))
    num_customers=len(ct_replication)
    throughput_simulation.append(num_customers/(SIM_TIME - WARMUP_TIME))

    ct_replication=[]
    waiting_time_replication=[]

print(f'Average Cycle Time: {np.mean(ct_simulation)/60: .2f} minutes +/- {np.std(ct_simulation)/60: .2f} minutes')
print(f'Average Waiting Time: {np.mean(waiting_time_simulation)/60: .2f} minutes +/- {np.std(waiting_time_simulation)/60: .2f} minutes')
print(f'Average Throughput Rate: {np.mean(throughput_simulation)*60*60: .2f} customer/hour +/- {np.std(throughput_simulation)*60*60: .2f} customer/hour')
