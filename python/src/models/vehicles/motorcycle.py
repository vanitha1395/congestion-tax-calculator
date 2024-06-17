from models.vehicles.vehicle import Vehicle

# Extends motorcycle from vehicle.
class Motorcycle(Vehicle):
    def get_vehicle_type() -> str:
        return "Motorcycle"

