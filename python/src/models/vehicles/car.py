from models.vehicles.vehicle import Vehicle

# extends car from vehicle.
class Car(Vehicle):
    def get_vehicle_type() -> str:
        return "Car"
