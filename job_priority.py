import numpy as np
import simpy
import random
import numpy as numpy

jobs={}
stats ={'cycle_times':
            {
                1:[],
                2:[]
            }
            }
def job_arrival(env,workers):
    i=0
    while True:
        i+=1
        yield env.timeout(random.expovariate(1/10))
        job_prio=np.random.choice([1,2], p=[0.2,0.8])
        name=i
        jobs[name]=env.now
        env.process(process_job(env, name, job_prio,workers))

        if i>100:
            break

def process_job(env, name, job_prio, workers):
    with workers.request(priority=job_prio) as req:
        yield req
        yield env.timeout(20)

    print(f'Job {name} with priority {job_prio} finished at {env.now}')
    jobs[name]=env.now-jobs[name]
    stats['cycle_times'][job_prio].append(jobs[name])

env=simpy.Environment()
workers=simpy.PriorityResource(env, capacity=1)
env.process(job_arrival(env, workers))
env.run()