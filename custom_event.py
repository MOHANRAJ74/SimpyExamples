import simpy
import random

def coffee_machine(env):
    while True:
        print(f"Coffee machine ready to use at {env.now: .2f}.")
        random_running_out_of_coffee=random.uniform(60,180)
        yield env.timeout(random_running_out_of_coffee)
        print(f"coffee over! call operator at {env.now:.2f}")
        refill=env.event()
        print(f"Created refill event. Refill triggered attribute: {refill.triggered} at {env.now:.2f}")

        env.process(refilling(env, refill))
        yield refill

def refilling(env, refill):
    refill_time=15
    yield  env.timeout(refill_time)
    refill.succeed()
    print(f"Created refill event.Refill triggered attribute: {refill.triggered} at {env.now:.2f}")

    clean_floor_time=5
    yield env.timeout(clean_floor_time)
    print(f"Floor cleaned. Operator leaves at {env.now: .2f}")

env=simpy.Environment()
env.process(coffee_machine(env))
env.run(until=24*60)
