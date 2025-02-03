from http import HTTPStatus
from typing import Dict

from fastapi import APIRouter, HTTPException, Path, Query

from ..models.models import OPENAPI_EXAMPLES
from ..service.account_service import AccountService
from ..service.electricity_reading_service import ElectricityReadingService
from ..service.price_plan_service import PricePlanService
from .electricity_reading_controller import repository as readings_repository


class UsageController:
    def __init__(self):
        self._price_plan_service = PricePlanService()
        self._account_service = AccountService()
        self._electricity_reading_service = ElectricityReadingService(readings_repository)
        self.router = APIRouter(
            prefix="/usage_cost",
            tags=["Price Plan Comparator Controller"],
        )
        self._initialize_routes()

    def _initialize_routes(self):
        self.router.get(
            "/get_usage_cost/{smart_meter_id}",
            response_model=Dict,
            description="Compare prices for all plans for a given meter",
        )(self.get_usage_cost)

    def get_usage_cost(
        self,
        smart_meter_id: str = Path(openapi_examples=OPENAPI_EXAMPLES),
        number_days: int = Query("No of days before you want usage"),
    ):
        print(1)
        readings = self._electricity_reading_service.retrieve_readings_for(smart_meter_id)
        if not readings:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No readings found for this smart meter ID")

        pricePlanId = self._account_service.get_price_plan(smart_meter_id)

        if not pricePlanId:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No price plan found for this smart meter ID")

        last_week_readings = self._electricity_reading_service.retrieve_last_days_readings(readings, number_days)
        print(last_week_readings)

        if not last_week_readings:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No readings found")
        usage_cost_list = self._price_plan_service.get_list_of_spend_against_each_price_plan_for(
            last_week_readings, limit=None
        )
        # print(usage_cost_list)
        # [{'price-plan-2': 0.5873877551020407}, {'price-plan-1': 1.1747755102040813}, {'price-plan-0': 5.873877551020406}]

        cost_for_required_price_plan = 0
        for cost in usage_cost_list:
            if pricePlanId in cost:
                cost_for_required_price_plan = cost[pricePlanId]

        return {"total_usage_cost": cost_for_required_price_plan}


usage_controller = UsageController()
router = usage_controller.router
