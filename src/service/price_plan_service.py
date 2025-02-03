from functools import reduce

from ..repository.price_plan_repository import price_plan_repository
from .time_converter import time_elapsed_in_hours


def calculate_time_elapsed(readings):
    min_time = min(map(lambda r: r.time, readings))
    max_time = max(map(lambda r: r.time, readings))
    return time_elapsed_in_hours(min_time, max_time)


class PricePlanService:
    def __init__(self):
        pass
        # self.electricity_reading_service = ElectricityReadingService(reading_repository)

    def store_price_plan_details(self, price_plans):
        price_plan_repository.store(price_plans)

    def _calculate_average_reading(self, readings):
        sum = reduce((lambda p, c: p + c), map(lambda r: r.reading, readings), 0)
        return sum / len(readings)

    def _cost_from_plan(self, consumed_energy, price_plan):
        cost = {}
        cost[price_plan.name] = consumed_energy * price_plan.unit_rate
        return cost

    def _calculate_consumed_energy(self, average, time_elapsed):
        return average / time_elapsed

    def _cheapest_plans_first(self, price_plans):
        return list(sorted(price_plans, key=lambda plan: plan.unit_rate))

    def get_list_of_spend_against_each_price_plan_for(self, readings, limit=None):
        # readings = self.electricity_reading_service.retrieve_readings_for(smart_meter_id)
        if len(readings) < 1:
            return []

        average = self._calculate_average_reading(readings)
        time_elapsed = calculate_time_elapsed(readings)
        consumed_energy = self._calculate_consumed_energy(average, time_elapsed)
        print(f"Average={average} Time elapsed={time_elapsed} Consumed energy={consumed_energy}")
        price_plans = price_plan_repository.get()
        list_of_spend = list(
            map(
                lambda price_plan: self._cost_from_plan(consumed_energy, price_plan),
                self._cheapest_plans_first(price_plans),
            )
        )
        print(f"List of spend= {list_of_spend}")
        return list_of_spend[:limit]
