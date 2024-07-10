import simpy
import random

def coffee_machine(env):
    while True:
        print(f"Coffee machine ready to use at {env.now: .2f}.")
        random_interrarival_time=100
        yield env.timeout(random_interrarival_time)
        print(f"Coffee over! call worker at {env.now: .2f}.")
        yield env.process(refilling(env, worker))

def clean_floor(env, worker):
    time_to_clean =120
    while True:
        try:
            while time_to_clean:
                print(f"Cleaning started at {env.now: .2f} and time to clean={time_to_clean: .2f}.")
                with worker.request(priority=2) as req:
                    yield req
                    start =env.now
                    yield env.timeout(time_to_clean)
                    print(f"Cleaning finished at {env.now: .2f}.")
                    time_to_clean=120
        except simpy.Interrupt:
            current_time=env.now
            time_to_clean=current_time-start
            if time_to_clean==0:
                time_to_clean=120
            print(f"Cleaning process interrupted at {env.now: .2f} and time left to clean = {time_to_clean: .2f}.")

def refilling(env, worker):

    with worker.request(priority=1) as req:
        yield req
        print(f"Refilling process started at time: {env.now: .2f}.")
        yield env.timeout(15)
        print(f"Refillied. Machine ready to use at {env.now: .2f}.")

env=simpy.Environment()
worker=simpy.PreemptiveResource(env, capacity=1)
env.process(coffee_machine(env))
env.run(until=24*60)
















