import environs

env = environs.Env()
q = env.read_env()
print((q))
