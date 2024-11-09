import traci
import sumolib
import os
import time

sumo_binary = sumolib.checkBinary('sumo-gui')

sumo_config = os.path.join(os.path.dirname(__file__), '../Networks/demo_net/demo.sumocfg')

def traffic_light_agent():
    traci.start([sumo_binary, "--start", "-c", sumo_config])
    traffic_light_id = traci.trafficlight.getIDList()[0]

    #traci.trafficlight.setProgram(traffic_light_id, "off") # Disables the default traffic lights pattern 
    num_phases = len(traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id))
    print(num_phases)

    step = 0
    try:
        while step < 200:
            traci.simulationStep()
            step+=1

            if step == 50:
                if num_phases > 0:
                    #Change to green for up-down direction (Phase 0)
                    traci.trafficlight.setPhase(traffic_light_id, 0)
                    traci.trafficlight.setPhaseDuration(traffic_light_id, 15) #Stay green for 15 steps
                    print("Changed to Phase 0 at step 50")

            elif step == 100:
                if num_phases > 1:
                    #Change to green for left-right direction (Phase 2)
                    traci.trafficlight.setPhase(traffic_light_id, 2)
                    traci.trafficlight.setPhaseDuration(traffic_light_id, 20) #Stay green for 15 steps
                    print("Changed to Phase 2 at step 100")

            elif step == 150:
                if num_phases > 0:
                    traci.trafficlight.setPhase(traffic_light_id, 0)
                    traci.trafficlight.setPhaseDuration(traffic_light_id, 15) #Stay green for 10 steps
                    print("Changed to Phase 0 at step 150")
            
            current_phase = traci.trafficlight.getPhase(traffic_light_id)
            remaining_time = traci.trafficlight.getNextSwitch(traffic_light_id) - traci.simulation.getTime()

            print(f"Step {step}: Traffic Light ID: {traffic_light_id}, Current Phase: {current_phase}, Remaining Time: {remaining_time:.2f} seconds ")
        
            vehicle_ids = traci.vehicle.getIDList()
            print(f"     Number of Vehicles - {len(vehicle_ids)}")
    except Exception as e:
        print(f"An error occured: {e}")

    finally:
        traci.close()

if __name__ == "__main__":
    traffic_light_agent()