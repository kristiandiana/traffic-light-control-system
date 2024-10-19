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
sumo_config = os.path.join(os.path.dirname(__file__), "test2.sumocfg")

# Define TraCI setup
def run_sumo():
    # Start the SUMO simulation using TraCI
    traci.start([sumo_binary, "--start", "-c", sumo_config])

    # Simulation loop
    step = 0
    try:
        while step < 1000:  # Run for 1000 steps (you can adjust this as needed)
            traci.simulationStep()  # Advance the simulation by one step
            step += 1

            # You can add your custom logic here
            time.sleep(1)
            
            # Example: Get the number of vehicles in the network
            vehicle_ids = traci.vehicle.getIDList()
            print(f"Step {step}: Number of vehicles - {len(vehicle_ids)}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the TraCI connection
        traci.close()

if __name__ == "__main__":
    run_sumo()
