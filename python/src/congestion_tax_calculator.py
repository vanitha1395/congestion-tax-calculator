from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict

from models.vehicles.vehicle import Vehicle
from models.vehicles.car import Car
from models.vehicles.motorbike import Motorbike
from models.vehicles.emergency_vehicle import EmergencyVehicle
from models.vehicles.motorcycle import Motorcycle
from models.vehicles.military_vehicle import MilitaryVehicle
from models.vehicles.bus import Bus
from models.vehicles.foreign_vehicle import ForeignVehicle

from models.cities.city import City
from models.cities.gothenburg import Gothenburg

# configurable parameters imported
import config

class CongestionCalculator:
    def __init__(self, city, vehicle_type):
        self.city = self.create_city(city.lower())
        self.vehicle = self.create_vehicle(vehicle_type)

    ## Factory method for creating appropriate city object
    def create_city(self, city_name_str):
        # dict can be extended with new cities
        cities = {
            "gothenburg": Gothenburg
        }
        return cities[city_name_str]

    # Factory method for creating respective vehicle object
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

    """
    Calculates toll for respective vehicle and time based on the city
    """
    def get_toll_fee(self, date: datetime, vehicle: Vehicle) -> int:
        if self.is_toll_free_date(date) or self.is_toll_free_vehicle(vehicle):
            return 0
        date_obj = datetime.fromisoformat(date)
        time_obj = date_obj.time()

        toll_schedule = self.city.get_tool_fee_schedule()

        for start_time, end_time, fee in toll_schedule:
            if start_time <= time_obj < end_time:
                return fee

        return 0

    """
    Identify if toll free vehicles using this method
    """
    def is_toll_free_vehicle(self, vehicle: Vehicle) -> bool:

        # vehicle name present in toll free vehicle list
        vehicle_type = vehicle.get_vehicle_type()
        vehicle_type = vehicle_type.lower()
        if vehicle_type in config.toll_free_vehicles:
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

        if year == 2023:
            if month == 1 and day == 1 or month == 3 and (day == 28 or day == 29) or month == 4 and (day == 1 or day == 30) or month == 5 and (day == 1 or day == 8 or day == 9) or month == 6 and (day == 5 or day == 6 or day == 21) or month == 7 or month == 11 and day == 1 or month == 12 and (day == 24 or day == 25 or day == 26 or day == 31):
                return True

        return False

    # This func had error in calculating date wise, so its fixed in below function.
    # def get_tax(self, dates: list):
    #     interval_start = dates[0]
    #     total_fee = 0
    #     for date in dates:
    #         travel_date = datetime.fromisoformat(date)
    #         interval_date = datetime.fromisoformat(interval_start)
    #         next_fee = self.get_toll_fee(date, self.vehicle)
    #         temp_fee = self.get_toll_fee(interval_start, self.vehicle)

    #         diff_in_seconds = travel_date.timestamp() - interval_date.timestamp()
    #         minutes = diff_in_seconds / 60

    #         if minutes <= 60:
    #             if total_fee > 0:
    #                 total_fee = total_fee - temp_fee
    #             if next_fee >= temp_fee:
    #                 temp_fee = next_fee
    #             total_fee = total_fee + temp_fee
    #         else:
    #             total_fee = total_fee + next_fee
    #             interval_start = date
    #     if total_fee > 60:
    #         total_fee = 60
    #     return total_fee

    def get_tax_with_date(self, datetime_str_list: list):

        # Create a dictionary to store the toll for each date
        toll_by_date = defaultdict(int)

        # Create a dictionary to store the last charged time for each date
        last_charged_time = {}

        # Iterate over the datetime string list
        for dt_str in datetime_str_list:
            # Convert the string to a datetime object
            dt = datetime.fromisoformat(dt_str)

            # Get the date from the datetime object
            date = dt.date()

            # Calculate the toll for the current datetime
            toll = self.get_toll_fee(dt_str, self.vehicle)

            # Check if the current datetime is within 60 minutes of the last charged time for the same date
            if date in last_charged_time:
                last_charged_dt = last_charged_time[date]
                time_diff = dt - last_charged_dt
                if time_diff < timedelta(hours=1):
                    continue  # Skip this datetime as it falls within the 60-minute window

            # Add the toll to the corresponding date in the dictionary
            toll_by_date[date] += toll

            # Update the last charged time for the current date
            last_charged_time[date] = dt

        # Cap the total toll at 60 per day
        for date, toll in toll_by_date.items():
            if toll > 60:
                toll_by_date[date] = 60

        return sum(toll_by_date.values())