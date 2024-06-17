from models.vehicles.vehicle import Vehicle

class Bus(Vehicle):
    def get_vehicle_type() -> str:
        return "Bus"