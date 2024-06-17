from models.vehicles.vehicle import Vehicle

class ForeignVehicle(Vehicle):
    def get_vehicle_type(self) -> str:
        return "Foreign vehicle"