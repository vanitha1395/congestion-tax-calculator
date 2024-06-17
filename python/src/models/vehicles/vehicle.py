from abc import ABC, abstractmethod

class Vehicle:
    @abstractmethod
    def get_vehicle_type(self) -> str:
        pass
