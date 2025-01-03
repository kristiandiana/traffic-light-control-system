import traci
import sumolib
import time
import os
import random

'''
Run this file to have the simulation automatically run. 
'''

# SUMO binary (either sumo-gui or sumo depending on whether you want to see the GUI or not)
sumo_binary = sumolib.checkBinary('sumo-gui')  # Use 'sumo-gui' if you want to see the GUI

# Path to your SUMO configuration file (.sumocfg)
sumo_config = os.path.join(os.path.dirname(__file__), '../Networks/demo_net/demo.sumocfg')
spawn_rate = 0.3 # 30% chance to spawn a vehicle on each step

# Define TraCI setup
def run_sumo():
    # Start the SUMO simulation using TraCI
    traci.start([sumo_binary, "--start", "-c", sumo_config])

    # Simulation loop
    step = 0
    try:
        while step < 190:  # Running this for 200 steps, but you can make it run indefinitely
            traci.simulationStep()  # Advance the simulation by one step
            step += 1
            
            if random.random() < spawn_rate:
                add_random_vehicle(step)
            
            # Example: Get the number of vehicles in the network
            vehicle_ids = traci.vehicle.getIDList()
            print("")
            print("&&&&&&&&&&&&&&&&&&&&&&&&")
            print(f"Step {step}: Number of vehicles - {len(vehicle_ids)}")

            # get vehicle information for all vehicles currently in the network
            for vehicle_id in vehicle_ids:

                # get variables
                position = traci.vehicle.getPosition(vehicle_id)
                speed = traci.vehicle.getSpeed(vehicle_id)
                route = traci.vehicle.getRoute(vehicle_id)

                print(f"Vehicle id: {vehicle_id}. Position: {position}. Speed: {speed}. Route: {route}")

            control_traffic_lights(step)
            
            time.sleep(0.1)
            
            print("&&&&&&&&&&&&&&&&&&&&&&&&")


    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the TraCI connection
        traci.close()
        
def add_random_vehicle(step):
    vehicle_id = f"veh_{step}_{random.randint(1, 1000)}"
    edges = traci.edge.getIDList()
    random_edge = random.choice(edges) # random road
    
    try:
        traci.vehicle.add(vehID=vehicle_id, routeID=random_edge)
        traci.vehicle.moveTo(vehicle_id, random_edge)
        
        print(f"Added vehicle {vehicle_id} at edge {random_edge}")
    except traci.TraCIException:
        print(f"Failed to add vehicle {vehicle_id} at edge {random_edge}")        
        
def control_traffic_lights(step):
    
    traffic_light_ids = traci.trafficlight.getIDList()
    for tl_id in traffic_light_ids:
        current_phase = traci.trafficlight.getPhase(tl_id)
        remaining_time = traci.trafficlight.getNextSwitch(tl_id) - traci.simulation.getTime()

        if step == 60:
            traci.trafficlight.setPhase(tl_id, 1)
            traci.trafficlight.setPhaseDuration(tl_id, 3)
        if step == 63:
            traci.trafficlight.setPhase(tl_id, 0)
            traci.trafficlight.setPhaseDuration(tl_id, 20)
            print(f"Updated traffic light {tl_id} at step {step}")

if __name__ == "__main__":
    run_sumo()


