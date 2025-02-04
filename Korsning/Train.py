from stable_baselines3 import DQN
from TrafficEnv import TrafficEnv

env = TrafficEnv()
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)
model.save("traffic_light_model")
