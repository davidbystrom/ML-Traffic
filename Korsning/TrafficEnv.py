import gymnasium as gym
import numpy as np
from gymnasium import spaces
import traci
import traci.constants as tc
import time

class TrafficEnv(gym.Env):
    def __init__(self):
        super(TrafficEnv, self).__init__()
        self.action_space = spaces.Discrete(729)  # Example: 0 = red, 1 = green
        self.observation_space = spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)  # Ensure compatibility with Gym's reset()
        try:
            traci.close()
        except:
            pass
        traci.start(["sumo", "-c", "Korsning.sumocfg", "--time-to-teleport", "-1"])
        traci.junction.subscribeContext("J4", tc.CMD_GET_VEHICLE_VARIABLE, 42, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])
        initial_observation = np.array([0, 0, 0, 0], dtype=np.float32)
        return initial_observation, {}

    def step(self, action):
        last_light = traci.trafficlight.getRedYellowGreenState("J4")
        # if action == 1:
        #     traci.trafficlight.setRedYellowGreenState("J4", "G")
        # elif action == 2:
        #     traci.trafficlight.setRedYellowGreenState("J4", "y")
        # else:
        #     traci.trafficlight.setRedYellowGreenState("J4", "r")
        array = ['GGGGGG', 'GGGGGr', 'GGGGGy', 'GGGGrG', 'GGGGrr', 'GGGGry', 'GGGGyG', 'GGGGyr', 'GGGGyy', 'GGGrGG', 'GGGrGr', 'GGGrGy', 'GGGrrG', 'GGGrrr', 'GGGrry', 'GGGryG', 'GGGryr', 'GGGryy', 'GGGyGG', 'GGGyGr', 'GGGyGy', 'GGGyrG', 'GGGyrr', 'GGGyry', 'GGGyyG', 'GGGyyr', 'GGGyyy', 'GGrGGG', 'GGrGGr', 'GGrGGy', 'GGrGrG', 'GGrGrr', 'GGrGry', 'GGrGyG', 'GGrGyr', 'GGrGyy', 'GGrrGG', 'GGrrGr', 'GGrrGy', 'GGrrrG', 'GGrrrr', 'GGrrry', 'GGrryG', 'GGrryr', 'GGrryy', 'GGryGG', 'GGryGr', 'GGryGy', 'GGryrG', 'GGryrr', 'GGryry', 'GGryyG', 'GGryyr', 'GGryyy', 'GGyGGG', 'GGyGGr', 'GGyGGy', 'GGyGrG', 'GGyGrr', 'GGyGry', 'GGyGyG', 'GGyGyr', 'GGyGyy', 'GGyrGG', 'GGyrGr', 'GGyrGy', 'GGyrrG', 'GGyrrr', 'GGyrry', 'GGyryG', 'GGyryr', 'GGyryy', 'GGyyGG', 'GGyyGr', 'GGyyGy', 'GGyyrG', 'GGyyrr', 'GGyyry', 'GGyyyG', 'GGyyyr', 'GGyyyy', 'GrGGGG', 'GrGGGr', 'GrGGGy', 'GrGGrG', 'GrGGrr', 'GrGGry', 'GrGGyG', 'GrGGyr', 'GrGGyy', 'GrGrGG', 'GrGrGr', 'GrGrGy', 'GrGrrG', 'GrGrrr', 'GrGrry', 'GrGryG', 'GrGryr', 'GrGryy', 'GrGyGG', 'GrGyGr', 'GrGyGy', 'GrGyrG', 'GrGyrr', 'GrGyry', 'GrGyyG', 'GrGyyr', 'GrGyyy', 'GrrGGG', 'GrrGGr', 'GrrGGy', 'GrrGrG', 'GrrGrr', 'GrrGry', 'GrrGyG', 'GrrGyr', 'GrrGyy', 'GrrrGG', 'GrrrGr', 'GrrrGy', 'GrrrrG', 'Grrrrr', 'Grrrry', 'GrrryG', 'Grrryr', 'Grrryy', 'GrryGG', 'GrryGr', 'GrryGy', 'GrryrG', 'Grryrr', 'Grryry', 'GrryyG', 'Grryyr', 'Grryyy', 'GryGGG', 'GryGGr', 'GryGGy', 'GryGrG', 'GryGrr', 'GryGry', 'GryGyG', 'GryGyr', 'GryGyy', 'GryrGG', 'GryrGr', 'GryrGy', 'GryrrG', 'Gryrrr', 'Gryrry', 'GryryG', 'Gryryr', 'Gryryy', 'GryyGG', 'GryyGr', 'GryyGy', 'GryyrG', 'Gryyrr', 'Gryyry', 'GryyyG', 'Gryyyr', 'Gryyyy', 'GyGGGG', 'GyGGGr', 'GyGGGy', 'GyGGrG', 'GyGGrr', 'GyGGry', 'GyGGyG', 'GyGGyr', 'GyGGyy', 'GyGrGG', 'GyGrGr', 'GyGrGy', 'GyGrrG', 'GyGrrr', 'GyGrry', 'GyGryG', 'GyGryr', 'GyGryy', 'GyGyGG', 'GyGyGr', 'GyGyGy', 'GyGyrG', 'GyGyrr', 'GyGyry', 'GyGyyG', 'GyGyyr', 'GyGyyy', 'GyrGGG', 'GyrGGr', 'GyrGGy', 'GyrGrG', 'GyrGrr', 'GyrGry', 'GyrGyG', 'GyrGyr', 'GyrGyy', 'GyrrGG', 'GyrrGr', 'GyrrGy', 'GyrrrG', 'Gyrrrr', 'Gyrrry', 'GyrryG', 'Gyrryr', 'Gyrryy', 'GyryGG', 'GyryGr', 'GyryGy', 'GyryrG', 'Gyryrr', 'Gyryry', 'GyryyG', 'Gyryyr', 'Gyryyy', 'GyyGGG', 'GyyGGr', 'GyyGGy', 'GyyGrG', 'GyyGrr', 'GyyGry', 'GyyGyG', 'GyyGyr', 'GyyGyy', 'GyyrGG', 'GyyrGr', 'GyyrGy', 'GyyrrG', 'Gyyrrr', 'Gyyrry', 'GyyryG', 'Gyyryr', 'Gyyryy', 'GyyyGG', 'GyyyGr', 'GyyyGy', 'GyyyrG', 'Gyyyrr', 'Gyyyry', 'GyyyyG', 'Gyyyyr', 'Gyyyyy', 'rGGGGG', 'rGGGGr', 'rGGGGy', 'rGGGrG', 'rGGGrr', 'rGGGry', 'rGGGyG', 'rGGGyr', 'rGGGyy', 'rGGrGG', 'rGGrGr', 'rGGrGy', 'rGGrrG', 'rGGrrr', 'rGGrry', 'rGGryG', 'rGGryr', 'rGGryy', 'rGGyGG', 'rGGyGr', 'rGGyGy', 'rGGyrG', 'rGGyrr', 'rGGyry', 'rGGyyG', 'rGGyyr', 'rGGyyy', 'rGrGGG', 'rGrGGr', 'rGrGGy', 'rGrGrG', 'rGrGrr', 'rGrGry', 'rGrGyG', 'rGrGyr', 'rGrGyy', 'rGrrGG', 'rGrrGr', 'rGrrGy', 'rGrrrG', 'rGrrrr', 'rGrrry', 'rGrryG', 'rGrryr', 'rGrryy', 'rGryGG', 'rGryGr', 'rGryGy', 'rGryrG', 'rGryrr', 'rGryry', 'rGryyG', 'rGryyr', 'rGryyy', 'rGyGGG', 'rGyGGr', 'rGyGGy', 'rGyGrG', 'rGyGrr', 'rGyGry', 'rGyGyG', 'rGyGyr', 'rGyGyy', 'rGyrGG', 'rGyrGr', 'rGyrGy', 'rGyrrG', 'rGyrrr', 'rGyrry', 'rGyryG', 'rGyryr', 'rGyryy', 'rGyyGG', 'rGyyGr', 'rGyyGy', 'rGyyrG', 'rGyyrr', 'rGyyry', 'rGyyyG', 'rGyyyr', 'rGyyyy', 'rrGGGG', 'rrGGGr', 'rrGGGy', 'rrGGrG', 'rrGGrr', 'rrGGry', 'rrGGyG', 'rrGGyr', 'rrGGyy', 'rrGrGG', 'rrGrGr', 'rrGrGy', 'rrGrrG', 'rrGrrr', 'rrGrry', 'rrGryG', 'rrGryr', 'rrGryy', 'rrGyGG', 'rrGyGr', 'rrGyGy', 'rrGyrG', 'rrGyrr', 'rrGyry', 'rrGyyG', 'rrGyyr', 'rrGyyy', 'rrrGGG', 'rrrGGr', 'rrrGGy', 'rrrGrG', 'rrrGrr', 'rrrGry', 'rrrGyG', 'rrrGyr', 'rrrGyy', 'rrrrGG', 'rrrrGr', 'rrrrGy', 'rrrrrG', 'rrrrrr', 'rrrrry', 'rrrryG', 'rrrryr', 'rrrryy', 'rrryGG', 'rrryGr', 'rrryGy', 'rrryrG', 'rrryrr', 'rrryry', 'rrryyG', 'rrryyr', 'rrryyy', 'rryGGG', 'rryGGr', 'rryGGy', 'rryGrG', 'rryGrr', 'rryGry', 'rryGyG', 'rryGyr', 'rryGyy', 'rryrGG', 'rryrGr', 'rryrGy', 'rryrrG', 'rryrrr', 'rryrry', 'rryryG', 'rryryr', 'rryryy', 'rryyGG', 'rryyGr', 'rryyGy', 'rryyrG', 'rryyrr', 'rryyry', 'rryyyG', 'rryyyr', 'rryyyy', 'ryGGGG', 'ryGGGr', 'ryGGGy', 'ryGGrG', 'ryGGrr', 'ryGGry', 'ryGGyG', 'ryGGyr', 'ryGGyy', 'ryGrGG', 'ryGrGr', 'ryGrGy', 'ryGrrG', 'ryGrrr', 'ryGrry', 'ryGryG', 'ryGryr', 'ryGryy', 'ryGyGG', 'ryGyGr', 'ryGyGy', 'ryGyrG', 'ryGyrr', 'ryGyry', 'ryGyyG', 'ryGyyr', 'ryGyyy', 'ryrGGG', 'ryrGGr', 'ryrGGy', 'ryrGrG', 'ryrGrr', 'ryrGry', 'ryrGyG', 'ryrGyr', 'ryrGyy', 'ryrrGG', 'ryrrGr', 'ryrrGy', 'ryrrrG', 'ryrrrr', 'ryrrry', 'ryrryG', 'ryrryr', 'ryrryy', 'ryryGG', 'ryryGr', 'ryryGy', 'ryryrG', 'ryryrr', 'ryryry', 'ryryyG', 'ryryyr', 'ryryyy', 'ryyGGG', 'ryyGGr', 'ryyGGy', 'ryyGrG', 'ryyGrr', 'ryyGry', 'ryyGyG', 'ryyGyr', 'ryyGyy', 'ryyrGG', 'ryyrGr', 'ryyrGy', 'ryyrrG', 'ryyrrr', 'ryyrry', 'ryyryG', 'ryyryr', 'ryyryy', 'ryyyGG', 'ryyyGr', 'ryyyGy', 'ryyyrG', 'ryyyrr', 'ryyyry', 'ryyyyG', 'ryyyyr', 'ryyyyy', 'yGGGGG', 'yGGGGr', 'yGGGGy', 'yGGGrG', 'yGGGrr', 'yGGGry', 'yGGGyG', 'yGGGyr', 'yGGGyy', 'yGGrGG', 'yGGrGr', 'yGGrGy', 'yGGrrG', 'yGGrrr', 'yGGrry', 'yGGryG', 'yGGryr', 'yGGryy', 'yGGyGG', 'yGGyGr', 'yGGyGy', 'yGGyrG', 'yGGyrr', 'yGGyry', 'yGGyyG', 'yGGyyr', 'yGGyyy', 'yGrGGG', 'yGrGGr', 'yGrGGy', 'yGrGrG', 'yGrGrr', 'yGrGry', 'yGrGyG', 'yGrGyr', 'yGrGyy', 'yGrrGG', 'yGrrGr', 'yGrrGy', 'yGrrrG', 'yGrrrr', 'yGrrry', 'yGrryG', 'yGrryr', 'yGrryy', 'yGryGG', 'yGryGr', 'yGryGy', 'yGryrG', 'yGryrr', 'yGryry', 'yGryyG', 'yGryyr', 'yGryyy', 'yGyGGG', 'yGyGGr', 'yGyGGy', 'yGyGrG', 'yGyGrr', 'yGyGry', 'yGyGyG', 'yGyGyr', 'yGyGyy', 'yGyrGG', 'yGyrGr', 'yGyrGy', 'yGyrrG', 'yGyrrr', 'yGyrry', 'yGyryG', 'yGyryr', 'yGyryy', 'yGyyGG', 'yGyyGr', 'yGyyGy', 'yGyyrG', 'yGyyrr', 'yGyyry', 'yGyyyG', 'yGyyyr', 'yGyyyy', 'yrGGGG', 'yrGGGr', 'yrGGGy', 'yrGGrG', 'yrGGrr', 'yrGGry', 'yrGGyG', 'yrGGyr', 'yrGGyy', 'yrGrGG', 'yrGrGr', 'yrGrGy', 'yrGrrG', 'yrGrrr', 'yrGrry', 'yrGryG', 'yrGryr', 'yrGryy', 'yrGyGG', 'yrGyGr', 'yrGyGy', 'yrGyrG', 'yrGyrr', 'yrGyry', 'yrGyyG', 'yrGyyr', 'yrGyyy', 'yrrGGG', 'yrrGGr', 'yrrGGy', 'yrrGrG', 'yrrGrr', 'yrrGry', 'yrrGyG', 'yrrGyr', 'yrrGyy', 'yrrrGG', 'yrrrGr', 'yrrrGy', 'yrrrrG', 'yrrrrr', 'yrrrry', 'yrrryG', 'yrrryr', 'yrrryy', 'yrryGG', 'yrryGr', 'yrryGy', 'yrryrG', 'yrryrr', 'yrryry', 'yrryyG', 'yrryyr', 'yrryyy', 'yryGGG', 'yryGGr', 'yryGGy', 'yryGrG', 'yryGrr', 'yryGry', 'yryGyG', 'yryGyr', 'yryGyy', 'yryrGG', 'yryrGr', 'yryrGy', 'yryrrG', 'yryrrr', 'yryrry', 'yryryG', 'yryryr', 'yryryy', 'yryyGG', 'yryyGr', 'yryyGy', 'yryyrG', 'yryyrr', 'yryyry', 'yryyyG', 'yryyyr', 'yryyyy', 'yyGGGG', 'yyGGGr', 'yyGGGy', 'yyGGrG', 'yyGGrr', 'yyGGry', 'yyGGyG', 'yyGGyr', 'yyGGyy', 'yyGrGG', 'yyGrGr', 'yyGrGy', 'yyGrrG', 'yyGrrr', 'yyGrry', 'yyGryG', 'yyGryr', 'yyGryy', 'yyGyGG', 'yyGyGr', 'yyGyGy', 'yyGyrG', 'yyGyrr', 'yyGyry', 'yyGyyG', 'yyGyyr', 'yyGyyy', 'yyrGGG', 'yyrGGr', 'yyrGGy', 'yyrGrG', 'yyrGrr', 'yyrGry', 'yyrGyG', 'yyrGyr', 'yyrGyy', 'yyrrGG', 'yyrrGr', 'yyrrGy', 'yyrrrG', 'yyrrrr', 'yyrrry', 'yyrryG', 'yyrryr', 'yyrryy', 'yyryGG', 'yyryGr', 'yyryGy', 'yyryrG', 'yyryrr', 'yyryry', 'yyryyG', 'yyryyr', 'yyryyy', 'yyyGGG', 'yyyGGr', 'yyyGGy', 'yyyGrG', 'yyyGrr', 'yyyGry', 'yyyGyG', 'yyyGyr', 'yyyGyy', 'yyyrGG', 'yyyrGr', 'yyyrGy', 'yyyrrG', 'yyyrrr', 'yyyrry', 'yyyryG', 'yyyryr', 'yyyryy', 'yyyyGG', 'yyyyGr', 'yyyyGy', 'yyyyrG', 'yyyyrr', 'yyyyry', 'yyyyyG', 'yyyyyr', 'yyyyyy']
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
        
        reward = - diff - waiting_times * 5 - traci.simulation.getEmergencyStoppingVehiclesNumber() * 50 - traci.simulation.getCollidingVehiclesNumber() * 2500

        # Observation: Vehicles on edges
        e4 = traci.edge.getLastStepVehicleNumber("-E4")
        e3 = traci.edge.getLastStepVehicleNumber("-E3")
        e2 = traci.edge.getLastStepVehicleNumber("E2")
        
        obs = np.array([waiting_times, e4, e3, e2], dtype=np.float32)
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