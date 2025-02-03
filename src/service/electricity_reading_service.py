from datetime import datetime, timedelta

from ..domain.electricity_reading import ElectricityReading
from .time_converter import _unix_time_of


class ElectricityReadingService:
    def __init__(self, repository):
        self.electricity_reading_repository = repository
        return

    def store_reading(self, json):
        readings = list(map(lambda x: ElectricityReading(x), json["electricityReadings"]))
        return self.electricity_reading_repository.store(json["smartMeterId"], readings)

    def clear_all_readings(self):
        return self.electricity_reading_repository.clear()

    def retrieve_readings_for(self, smart_meter_id):
        return self.electricity_reading_repository.find(smart_meter_id)

    def retrieve_last_days_readings(self, readings, number_days):
        current_time = datetime.now()
        last_days = current_time - timedelta(days=number_days)
        print(last_days)
        last_days_readings = [reading for reading in readings if reading.time > _unix_time_of(last_days)]
        return last_days_readings
