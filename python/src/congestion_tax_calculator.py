from datetime import datetime, time
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

        if year == 2013:
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
        # Create a dictionary to store the tax for each date
        tax_by_date = defaultdict(int)
        interval_date = datetime_str_list[0]

        # Iterate over the datetime list
        for dt_str in datetime_str_list:

            # Convert the string to a datetime object
            dt = datetime.fromisoformat(dt_str)
            interval_dt = datetime.fromisoformat(interval_date)

            # Get the date from the datetime object
            date = dt.strftime('%Y-%m-%d')

            # Calculate the toll for the current datetime
            toll = self.get_toll_fee(dt_str, self.vehicle)

            # Check if there's a previous datetime within one hour
            previous_dt_str = None
            for prev_dt_str in datetime_str_list:
                if prev_dt_str < dt_str:
                    previous_dt = datetime.fromisoformat(prev_dt_str)
                    time_diff = dt - previous_dt
                    if time_diff.total_seconds() < 3600:
                        previous_dt_str = prev_dt_str
                        break

            if previous_dt_str:
                previous_dt = datetime.fromisoformat(previous_dt_str)
                previous_toll = self.get_toll_fee(previous_dt, self.vehicle)
                if previous_toll > toll:
                    toll = previous_toll

            # Add the toll to the corresponding date in the dictionary
            tax_by_date[date] += toll


            # Cap the total tax at 60
            if tax_by_date[date] > 60:
                tax_by_date[date] = 60

        # Calculate the total tax by summing the taxes for each date
        total_tax = sum(tax_by_date.values())


        return total_tax