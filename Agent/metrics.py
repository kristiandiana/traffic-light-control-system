import traci
import sumolib
import os
import time

'''
metrics:
        - average wait time (in seconds)
        - number of times a vehicle comes to a complete stop
        - level of congestion (# of queued cars)
        - speed (indicator of flow + congestion)
        - position (indicator of vehicle density and clusters)
'''
log = "traffic_data_log.txt"

def initialize_log():
    with open(log, mode='w') as file:
        file.write("Traffic Simulation Data Log\n")
        file.write("=" * 40 + "\n\n")

def log_traffic_data(step, congestion_level, avg_wait_time, stops, vehicle_data):
    with open(log, mode='a') as file:
        file.write(f"Step: {step}\n")
        file.write(f"Congestion Level: {congestion_level}\n")
        file.write(f"Avg Wait Time: {avg_wait_time}\n")
        file.write(f"Total Stops: {stops}\n")
        file.write("vehicle Data:\n")
        for data in vehicle_data:
            file.write(f"  Vehicle ID: {data['vehicle_id']}, Speed: {data['speed']}, Position: {data['position']}\n")
        file.write("-" * 40 + "\n\n")

def calculate_congestion(lane_ids):
    congestion = 0
    
    # number of vehicles in all lanes
    for lane_id in lane_ids:
        num_vehicles_in_lane = traci.lane.getLastStepVehicleNumber(lane_id)
        congestion += num_vehicles_in_lane
    
    return congestion

def calculate_avg_wait_time(lane_ids):
    wait_times = []
    
    # total wait time of cars in all lanes
    for lane_id in lane_ids:
        # total wait time of all cars in one lane
        for vehicle_id in traci.lane.getLastStepVehicleIDs(lane_id):
            wait_time = traci.vehicle.getWaitingTime(vehicle_id)
            wait_times.append(wait_time)
    
    avg_wait_time = sum(wait_times)/len(wait_times) if wait_times else 0
    
    return avg_wait_time

def calculate_total_stops(lane_ids):
    total_stops = 0
    for lane_id in lane_ids:
        stops_in_lane = traci.lane.getLastStepHaltingNumber(lane_id)
        total_stops += stops_in_lane

    return total_stops

def get_vehicle_speed_position():
    vehicle_data = []
    vehicle_ids = traci.vehicle.getIDList()

    if vehicle_ids is None:
        print("No vehicles in the simulation")
    
    for vehicle_id in vehicle_ids:
        speed = traci.vehicle.getSpeed(vehicle_id)
        position = traci.vehicle.getPosition(vehicle_id)
        vehicle_data.append({"vehicle_id": vehicle_id, "speed": speed, "position": position})

    return vehicle_data

if __name__ == "__main__":
    sumo_binary = sumolib.checkBinary('sumo-gui')
    sumo_config = os.path.join(os.path.dirname(__file__), '../Networks/demo_net/demo.sumocfg')
    traci.start([sumo_binary, "--start", "-c", sumo_config])

    lane_ids = traci.lane.getIDList()

    initialize_log()

    step = 0
    while step < 186:
        traci.simulationStep()

        congestion_level = calculate_congestion(lane_ids)
        avg_wait_time = calculate_avg_wait_time(lane_ids)
        stops = calculate_total_stops(lane_ids)
        vehicle_data = get_vehicle_speed_position()

        log_traffic_data(step, congestion_level, avg_wait_time, stops, vehicle_data)

        print("Congestion Level: ", congestion_level)
        print("Avg Wait Time: ", avg_wait_time)
        print("Total stops: ", stops)

        for data in vehicle_data:
            print(f"Vehicle ID: {data['vehicle_id']}, Speed: {data['speed']}, Position: {data['position']}")
        
        #time.sleep(0.2)
        step += 1

    traci.close()