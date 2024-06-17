from models.vehicles.vehicle import Vehicle


class EmergencyVehicle(Vehicle):
    def get_vehicle_type() -> str:
        return "Emergency Vehicle"

