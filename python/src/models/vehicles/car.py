from models.vehicles.vehicle import Vehicle


class Car(Vehicle):
    def get_vehicle_type() -> str:
        return "Car"
