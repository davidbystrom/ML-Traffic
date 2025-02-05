import numpy as np
from stable_baselines3 import DQN
from Gui import TrafficEnv

# Load the environment
env = TrafficEnv()

# Load the trained model
model = DQN.load("traffic_light_model")


def evaluate_model(model, env, num_episodes=10, render=False):
    total_rewards = []
    waiting_times = []

    for episode in range(num_episodes):
        obs, _ = env.reset()
        done = False
        episode_reward = 0
        episode_wait_time = 0

        while not done:
            if render:
                env.render()
                
            # Predict action from model
            action, _ = model.predict(obs, deterministic=True)  # Ensure deterministic evaluation
            
            obs, reward, done, _, _ = env.step(action)
            episode_reward += reward
            episode_wait_time += obs[0]  # Collect waiting time

        total_rewards.append(episode_reward)
        waiting_times.append(episode_wait_time)
        print(f"Episode {episode + 1}: Reward = {episode_reward}, Waiting Time = {episode_wait_time}")

    env.close()
    
    avg_reward = np.mean(total_rewards)
    avg_wait_time = np.mean(waiting_times)
    print(f"\nAverage Reward over {num_episodes} episodes: {avg_reward}")
    print(f"Average Waiting Time: {avg_wait_time}")

    return avg_reward, avg_wait_time

evaluate_model(model, env, num_episodes=2, render=False)
