from datetime import datetime, time
from enum import Enum

from models.vehicles.vehicle import Vehicle
from models.vehicles.car import Car
from models.vehicles.motorbike import Motorbike
from models.vehicles.emergency_vehicle import EmergencyVehicle
from models.vehicles.motorcycle import Motorcycle
from models.vehicles.military_vehicle import MilitaryVehicle
from models.vehicles.bus import Bus
from models.vehicles.foreign_vehicle import ForeignVehicle

import json

toll_free_vehicles = [
    "emergency vehicle",
    "bus",
    "diplomat vehicle",
    "motorcyles",
    "military vehicle",
    "foreign vehicle"
]

class CongestionCalculator:
    def __init__(self, city, vehicle_type):
        self.city = city
        self.vehicle = self.create_vehicle(vehicle_type)

    def create_vehicle(self, vehicle_type: str) -> Vehicle:
        vehicle_types = {
            "car": Car,
            "motorbike": Motorbike,
            "motorcycle": Motorcycle,
            "emergency vehicle" : EmergencyVehicle,
            "military vehicle" : MilitaryVehicle,
            "bus" : Bus,
            "foreign vehicle": ForeignVehicle
        }
        return vehicle_types[vehicle_type]

    def get_toll_fee(self, date: datetime, vehicle: Vehicle) -> int:
        if self.is_toll_free_date(date) or self.is_toll_free_vehicle(vehicle):
            return 0
        date_obj = datetime.fromisoformat(date)
        time_obj = date_obj.time()

        tool_fee_schedule = [
            (time(6, 0), time(6, 29), 8),
            (time(6, 30), time(6, 59), 13),
            (time(7, 0), time(7, 59), 18),
            (time(8, 0), time(8, 29), 13),
            (time(8, 30), time(14, 59), 8),
            (time(15, 00), time(15, 29), 13),
            (time(15, 30), time(16, 59), 18),
            (time(17, 00), time(17, 59), 13),
            (time(18, 00), time(18, 29), 8),
        ]

        for start_time, end_time, fee in tool_fee_schedule:
            if start_time <= time_obj < end_time:
                return fee

        return 0

    def is_toll_free_vehicle(self, vehicle: Vehicle) -> bool:

        # vehicle name present in toll free vehicle list
        vehicle_type = vehicle.get_vehicle_type()
        vehicle_type = vehicle_type.lower()
        if vehicle_type in toll_free_vehicles:
            return True

        # return not toll free vehicle
        return False

        vehicle_type = vehicle.get_vehicle_type(vehicle)
        return vehicle_type == TollFreeVehicles.MOTORCYCLE.name.capitalize() or vehicle_type == TollFreeVehicles.TRACTOR.name.capitalize() or vehicle_type == TollFreeVehicles.EMERGENCY.name.capitalize() or vehicle_type == TollFreeVehicles.DIPLOMAT.name.capitalize() or vehicle_type == TollFreeVehicles.FOREIGN.name.capitalize() or vehicle_type == TollFreeVehicles.MILITARY.name.capitalize()

    def is_toll_free_date(self, date: datetime):
        date_obj = datetime.fromisoformat(date)
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day

        if date_obj.weekday() == 5 or date_obj.weekday() == 6:
            return True

        if year == 2013:
            if month == 1 and day == 1 or month == 3 and (day == 28 or day == 29) or month == 4 and (day == 1 or day == 30) or month == 5 and (day == 1 or day == 8 or day == 9) or month == 6 and (day == 5 or day == 6 or day == 21) or month == 7 or month == 11 and day == 1 or month == 12 and (day == 24 or day == 25 or day == 26 or day == 31):
                return True

        return False

    def get_tax(self, dates: list):
        interval_start = dates[0]
        total_fee = 0
        for date in dates:
            travel_date = datetime.fromisoformat(date)
            interval_date = datetime.fromisoformat(interval_start)
            next_fee = self.get_toll_fee(date, self.vehicle)
            temp_fee = self.get_toll_fee(interval_start, self.vehicle)

            diff_in_seconds = travel_date.timestamp() - interval_date.timestamp()
            minutes = diff_in_seconds / 60

            if minutes <= 60:
                if total_fee > 0:
                    total_fee = total_fee - temp_fee
                if next_fee >= temp_fee:
                    temp_fee = next_fee
                total_fee = total_fee + temp_fee
            else:
                total_fee = total_fee + next_fee
        if total_fee > 60:
            total_fee = 60
        return total_fee
