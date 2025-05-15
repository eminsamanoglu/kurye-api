from haversine import haversine

WEIGHTS = {
    "distance": 0.4,
    "time": 0.3,
    "workload": 0.2,
    "complexity": 0.1
}

def calculate_score(courier, order_location):
    distance_km = haversine(courier["location"], order_location)
    time_minutes = distance_km / 0.4 * 60

    distance_score = 1 / (distance_km + 0.01)
    time_score = 1 / (time_minutes + 1)
    workload_score = 1 / (courier["current_workload"] + 1)
    complexity_score = 1 / (courier["route_complexity"] + 1)

    final_score = (
        WEIGHTS["distance"] * distance_score +
        WEIGHTS["time"] * time_score +
        WEIGHTS["workload"] * workload_score +
        WEIGHTS["complexity"] * complexity_score
    )
    
    return final_score

def find_best_courier(order, couriers):
    best_score = -1
    best_courier = None
    for courier in couriers:
        score = calculate_score(courier, order["restaurant_location"])
        courier["score"] = score
        if score > best_score:
            best_score = score
            best_courier = courier
    return best_courier
