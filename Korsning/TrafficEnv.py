import gymnasium as gym
import numpy as np
from gymnasium import spaces
import traci
import traci.constants as tc
import time
import subprocess
import random

class TrafficEnv(gym.Env):
    def __init__(self):
        super(TrafficEnv, self).__init__()
        self.action_space = spaces.Discrete(5)  # Example: 0 = red, 1 = green
        self.observation_space = spaces.Box(low=0, high=100, shape=(5,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)  # Ensure compatibility with Gym's reset()
        try:
            traci.close()
        except:
            pass
        subprocess.run(["python", "randomTrips.py", "-n", "Korsning.net.xml", "-b", "0", "-e", "1000",  "--random", "--period", str(random.uniform(0.1, 0.5)), "--trip-attributes", "type='test'", "--edge-permission", "passenger", "--validate"])
        traci.start(["sumo", "-c", "Korsning.sumocfg", "--time-to-teleport", "-1"])
        traci.junction.subscribeContext("J4", tc.CMD_GET_VEHICLE_VARIABLE, 42, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])
        initial_observation = np.array([0, 0, 0, 0, 0], dtype=np.float32)
        return initial_observation, {}

    def step(self, action):
        last_light = traci.trafficlight.getRedYellowGreenState("J4")
        # if action == 1:
        #     traci.trafficlight.setRedYellowGreenState("J4", "G")
        # elif action == 2:
        #     traci.trafficlight.setRedYellowGreenState("J4", "y")
        # else:
        #     traci.trafficlight.setRedYellowGreenState("J4", "r")
        # array = ['GGGGGG', 'GGGGGr', 'GGGGrG', 'GGGGrr', 'GGGrGG', 'GGGrGr', 'GGGrrG', 'GGGrrr', 'GGrGGG', 'GGrGGr', 'GGrGrG', 'GGrGrr', 'GGrrGG', 'GGrrGr', 'GGrrrG', 'GGrrrr', 'GrGGGG', 'GrGGGr', 'GrGGrG', 'GrGGrr', 'GrGrGG', 'GrGrGr', 'GrGrrG', 'GrGrrr', 'GrrGGG', 'GrrGGr', 'GrrGrG', 'GrrGrr', 'GrrrGG', 'GrrrGr', 'GrrrrG', 'Grrrrr', 'rGGGGG', 'rGGGGr', 'rGGGrG', 'rGGGrr', 'rGGrGG', 'rGGrGr', 'rGGrrG', 'rGGrrr', 'rGrGGG', 'rGrGGr', 'rGrGrG', 'rGrGrr', 'rGrrGG', 'rGrrGr', 'rGrrrG', 'rGrrrr', 'rrGGGG', 'rrGGGr', 'rrGGrG', 'rrGGrr', 'rrGrGG', 'rrGrGr', 'rrGrrG', 'rrGrrr', 'rrrGGG', 'rrrGGr', 'rrrGrG', 'rrrGrr', 'rrrrGG', 'rrrrGr', 'rrrrrG', 'rrrrrr']
        array =  [ "rrrrrr", "GrGrGr", "GrrrGG", "GGGrrr", "rrGGGr"]
        traci.trafficlight.setRedYellowGreenState("J4", array[action])

        traci.simulationStep()
        # time.sleep(0.05)
        
        # Reward: Minimize vehicle waiting time
        # waiting_time = sum(traci.edge.getLastStepHaltingNumber(edge) for edge in traci.edge.getIDList())
        # reward = -waiting_time
        waiting_times = 0
        subscription_results = traci.junction.getContextSubscriptionResults("J4")
        if subscription_results:
            for _, variables in subscription_results.items():
                waiting_time = variables[tc.VAR_WAITING_TIME]
                waiting_times += waiting_time
                # print(f"Vehicle {vehicle_id} waiting time: {waiting_time}")
        diff = diff_letters(last_light, array[action])
        
        reward = - diff * 0.5 - waiting_times * 2 - traci.simulation.getEmergencyStoppingVehiclesNumber() * 0 - traci.simulation.getCollidingVehiclesNumber() * 1000

        # Observation: Vehicles on edges
        e4 = traci.edge.getLastStepVehicleNumber("-E4")
        e3 = traci.edge.getLastStepVehicleNumber("-E3")
        e2 = traci.edge.getLastStepVehicleNumber("E2")
        
        obs = np.array([waiting_times, e4, e3, e2, action], dtype=np.float32)
        done = False
        # done = traci.simulation.getMinExpectedNumber() == 0
        if traci.simulation.getMinExpectedNumber() == 0:
            # Restart
            traci.close()
            obs, _ = self.reset()
            done = True
        return obs, reward, done, False, {}

    

    def close(self):
        traci.close()

# python randomTrips.py -n Korsning.net.xml -b 0 -e 1000 -p 5 --trip-attributes="type='test'" --additional-file Korsning.rou.xml --edge-permission passenger --validate

def diff_letters(a,b):
        return sum ( a[i] != b[i] for i in range(len(a)) )