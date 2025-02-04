import traci
import traci.constants as tc
import time
sumoCmd = ["sumo-gui", "-c", "Korsning.sumocfg", "--start"]
traci.start(sumoCmd)
step = 0
# print(traci.trafficlight.getRedYellowGreenState("J4"))
#traci.trafficlight.setRedYellowGreenState("J4", "GGGGGG")
traci.junction.subscribeContext("J4", tc.CMD_GET_VEHICLE_VARIABLE, 42, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])
print(traci.junction.getContextSubscriptionResults("J4"))
while step < 1000:
    traci.simulationStep()
    step += 1
    time.sleep(1)
    print(traci.junction.getContextSubscriptionResults("J4"))

traci.close()