from .constants.constant import (
    MOST_EVIL_PRICE_PLAN_ID,
    MOST_EVIL_PRICE_PLAN_ID_UNIT_RATE,
    NUM_METERS,
    NUM_READINGS_AGAINST_METER,
    RENEWBLES_PRICE_PLAN_ID,
    RENEWBLES_PRICE_PLAN_ID_UNIT_RATE,
    STANDARD_PRICE_PLAN_ID,
    STANDARD_PRICE_PLAN_ID_UNIT_RATE,
)
from .controller.electricity_reading_controller import service as electricity_reading_service
from .domain.price_plan import PricePlan
from .enums.enum import ElectricitySupllier
from .generator.electricity_reading_generator import generate_electricity_readings
from .service.price_plan_service import PricePlanService

# DR_EVILS_DARK_ENERGY_ENERGY_SUPPLIER = "Dr Evil's Dark Energy"
# THE_GREEN_ECO_ENERGY_SUPPLIER = "The Green Eco"
# POWER_FOR_EVERYONE_ENERGY_SUPPLIER = "Power for Everyone"

# MOST_EVIL_PRICE_PLAN_ID = "price-plan-0"
# RENEWBLES_PRICE_PLAN_ID = "price-plan-1"
# STANDARD_PRICE_PLAN_ID = "price-plan-2"

# NUM_METERS = 10
# NUM_READINGS_AGAINST_METER = 5


def _populate_random_electricity_readings():
    for index in range(NUM_METERS):
        smartMeterId = f"smart-meter-{index}"
        electricity_reading_service.store_reading(
            {
                "smartMeterId": smartMeterId,
                "electricityReadings": generate_electricity_readings(NUM_READINGS_AGAINST_METER),
            }
        )


def _populate_price_plans():
    price_plans = [
        PricePlan(
            MOST_EVIL_PRICE_PLAN_ID,
            ElectricitySupllier.DR_EVILS_DARK_ENERGY_ENERGY_SUPPLIER,
            MOST_EVIL_PRICE_PLAN_ID_UNIT_RATE,
        ),
        PricePlan(
            RENEWBLES_PRICE_PLAN_ID,
            ElectricitySupllier.THE_GREEN_ECO_ENERGY_SUPPLIER,
            RENEWBLES_PRICE_PLAN_ID_UNIT_RATE,
        ),
        PricePlan(
            STANDARD_PRICE_PLAN_ID,
            ElectricitySupllier.POWER_FOR_EVERYONE_ENERGY_SUPPLIER,
            STANDARD_PRICE_PLAN_ID_UNIT_RATE,
        ),
    ]
    PricePlanService.store_price_plan_details(PricePlanService, price_plans)
    # price_plan_repository.store(price_plans)


def initialize_data():
    _populate_random_electricity_readings()
    _populate_price_plans()
