import simpy
env=simpy.Environment()

def customer(env):
  yield env.timeout(30)
  print(f'Details entered at time: {env.now}')
  yield env.timeout(60)
  print(f'Cash retrived at time: {env.now}')

env.process(customer(env=env))
env.run()
