from flask import Flask, request, jsonify
from flask_cors import CORS
from haversine import haversine

app = Flask(__name__)
CORS(app)  # CORS izinleri

WEIGHTS = {
    "distance": 0.4,
    "time": 0.3,
    "workload": 0.2,
    "complexity": 0.1
}

def calculate_score(courier, order_location):
    distance_km = haversine(courier["location"], order_location)
    time_minutes = distance_km / 0.4 * 60  # Ortalama hız: 24 km/h

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
        print(f"Kurye {courier['courier_id']} puanı: {score:.4f}")
        if score > best_score:
            best_score = score
            best_courier = courier
    return best_courier

@app.route('/')
def home():
    return "Taşıyıcı Express Kurye Atama API çalışıyor."

@app.route('/assign', methods=['POST'])
def assign():
    data = request.json
    if not data or "order" not in data or "couriers" not in data:
        return jsonify({"error": "Eksik veri"}), 400

    best = find_best_courier(data["order"], data["couriers"])
    return jsonify({"assigned_courier": best})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
