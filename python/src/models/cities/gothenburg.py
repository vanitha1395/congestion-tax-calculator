from models.cities.city import City
import config

class Gothenburg(City):
    def get_tool_fee_schedule() -> list:
        return config.gothenburg_toll_fee_schedule

    def get_city_name():
        return "gothenburg"
