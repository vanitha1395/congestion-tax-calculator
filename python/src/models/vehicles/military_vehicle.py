from models.vehicles.vehicle import Vehicle

class MilitaryVehicle(Vehicle):
    def get_vehicle_type(self) -> str:
        return "Military Vehicle"