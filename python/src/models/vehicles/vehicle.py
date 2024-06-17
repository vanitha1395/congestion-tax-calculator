from abc import ABC, abstractmethod

# Vehicle is a Abstract base class, which can be extended for other vehicles.
class Vehicle:
    @abstractmethod
    def get_vehicle_type(self) -> str:
        pass
