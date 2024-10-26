import traci
import sumolib
import time
import os

'''
Run this file to have the simulation automatically run. 
'''

# SUMO binary (either sumo-gui or sumo depending on whether you want to see the GUI or not)
sumo_binary = sumolib.checkBinary('sumo-gui')  # Use 'sumo-gui' if you want to see the GUI

# Path to your SUMO configuration file (.sumocfg)
sumo_config = os.path.join(os.path.dirname(__file__), '../Networks/demo_net/demo.sumocfg')


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

            # You can add your custom logic here
            time.sleep(0.1)
            
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

            # Retrieve and print traffic light data
            traffic_light_ids = traci.trafficlight.getIDList()
            print(f"Number of traffic lights: {len(traffic_light_ids)}")
            for tl_id in traffic_light_ids:

                # Get the current phase (green, yellow, red) of the traffic light
                current_phase = traci.trafficlight.getPhase(tl_id)

                # Get remaining time in the current phase
                remaining_time = traci.trafficlight.getNextSwitch(tl_id) - traci.simulation.getTime()

                print(f"Traffic Light Id: {tl_id}. Current phase: {current_phase}, Time remaining {remaining_time} seconds")

                ### CONTROLLING TRAFFIC LIGHT THROUGH TRACI 
                if step == 60:
                    traci.trafficlight.setPhase(tl_id, 1)
                    traci.trafficlight.setPhaseDuration(tl_id, 3)
                if step == 63:
                    traci.trafficlight.setPhase(tl_id, 0)
                    traci.trafficlight.setPhaseDuration(tl_id, 20)
                    print("Updated traffic light status through TraCI!")
            
            print("&&&&&&&&&&&&&&&&&&&&&&&&")


    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the TraCI connection
        traci.close()

if __name__ == "__main__":
    run_sumo()
