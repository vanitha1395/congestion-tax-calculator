from abc import ABC, abstractmethod

# using abstract base class(ABC) for making a abstract class based on which
# various cities can be built.

class City(ABC):
    def __init__(self, city):
        self.city_name = city

    @abstractmethod
    def get_tool_fee_schedule(self) -> list:
        pass