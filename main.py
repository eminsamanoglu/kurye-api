from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from logic.assigner import find_best_courier

app = FastAPI()

class Order(BaseModel):
    order_id: int
    restaurant_location: List[float]

class Courier(BaseModel):
    courier_id: int
    location: List[float]
    current_workload: int
    route_complexity: int

class AssignRequest(BaseModel):
    order: Order
    couriers: List[Courier]

@app.post("/assign")
def assign_courier(data: AssignRequest):
    # Pydantic modellerini dict'e çevir
    order = data.order.dict()
    couriers = [c.dict() for c in data.couriers]

    best = find_best_courier(order, couriers)
    return {
        "assigned_courier": best["courier_id"],
        "score": best["score"]
    }
