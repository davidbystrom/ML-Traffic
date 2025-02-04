import gymnasium as gym
import numpy as np
from gymnasium import spaces
import traci
import traci.constants as tc

class TrafficEnv(gym.Env):
    def __init__(self):
        super(TrafficEnv, self).__init__()
        self.action_space = spaces.Discrete(3)  # Example: 0 = red, 1 = green
        self.observation_space = spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)  # Ensure compatibility with Gym's reset()
        traci.start(["sumo", "-c", "Rakljus.sumocfg"])
        traci.junction.subscribeContext("J1", tc.CMD_GET_VEHICLE_VARIABLE, 42, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])
        initial_observation = np.array([0], dtype=np.float32)
        return initial_observation, {}

    def step(self, action):
        if action == 1:
            traci.trafficlight.setRedYellowGreenState("J1", "G")
        elif action == 2:
            traci.trafficlight.setRedYellowGreenState("J1", "y")
        else:
            traci.trafficlight.setRedYellowGreenState("J1", "r")
        traci.simulationStep()
        
        # Reward: Minimize vehicle waiting time
        # waiting_time = sum(traci.edge.getLastStepHaltingNumber(edge) for edge in traci.edge.getIDList())
        # reward = -waiting_time
        waiting_times = 0
        subscription_results = traci.junction.getContextSubscriptionResults("J1")
        if subscription_results:
            for _, variables in subscription_results.items():
                waiting_time = variables[tc.VAR_WAITING_TIME]
                waiting_times += waiting_time
                # print(f"Vehicle {vehicle_id} waiting time: {waiting_time}")
        reward = -waiting_times - traci.simulation.getEmergencyStoppingVehiclesNumber() * 100
        
        obs = np.array([waiting_times], dtype=np.float32)
        done = traci.simulation.getMinExpectedNumber() == 0
        return obs, reward, done, False, {}

    def close(self):
        traci.close()