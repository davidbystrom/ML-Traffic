from stable_baselines3 import DQN
from TrafficEnv import TrafficEnv

env = TrafficEnv()

model = DQN.load("traffic_light_model")
obs, _ = env.reset()
done = False

while not done:
    action, _ = model.predict(obs)
    obs, reward, done, _, _= env.step(action)
