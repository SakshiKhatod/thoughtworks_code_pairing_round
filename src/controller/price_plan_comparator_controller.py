# price_plan_controller.router
from http import HTTPStatus
from typing import Dict, List

from fastapi import APIRouter, HTTPException, Path, Query

from ..models.models import OPENAPI_EXAMPLES, PricePlanComparisons
from ..service.account_service import AccountService
from ..service.electricity_reading_service import ElectricityReadingService
from ..service.price_plan_service import PricePlanService
from .electricity_reading_controller import repository as readings_repository


class PricePlanConroller:
    def __init__(self):
        self._price_plan_service = PricePlanService()
        self._account_service = AccountService()
        self._electricity_reading_service = ElectricityReadingService(readings_repository)
        self.router = APIRouter(
            prefix="/price-plans",
            tags=["Price Plan Comparator Controller"],
        )
        self._initialize_routes()

    def _initialize_routes(self):
        self.router.get(
            "/compare-all/{smart_meter_id}",
            response_model=PricePlanComparisons,
            description="Compare prices for all plans for a given meter",
        )(self.compare)
        self.router.get(
            "/recommend/{smart_meter_id}",
            response_model=List[Dict],
            description="View recommended price plans for usage",
        )(self.recommend)

    def compare(self, smart_meter_id: str = Path(openapi_examples=OPENAPI_EXAMPLES)):
        # readings = readings_repository.find(smart_meter_id)
        # get readings from Electricity service and remove that part from get_list... function

        readings = self._electricity_reading_service.retrieve_readings_for(smart_meter_id)
        list_of_spend_against_price_plans = self._price_plan_service.get_list_of_spend_against_each_price_plan_for(
            readings
        )

        if len(list_of_spend_against_price_plans) < 1:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

        pricePlanId = self._account_service.get_price_plan(smart_meter_id)
        if not pricePlanId:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No price plan found for this smart meter ID")
        else:
            return {
                "pricePlanId": pricePlanId,
                "pricePlanComparisons": list_of_spend_against_price_plans,
            }

    def recommend(
        self,
        smart_meter_id: str = Path(openapi_examples=OPENAPI_EXAMPLES),
        limit: int = Query(description="Number of items to return", default=None),
    ):
        readings = self._electricity_reading_service.retrieve_readings_for(smart_meter_id)
        list_of_spend_against_price_plans = self._price_plan_service.get_list_of_spend_against_each_price_plan_for(
            readings, limit=limit
        )
        return list_of_spend_against_price_plans


price_plan_conroller = PricePlanConroller()
router = price_plan_conroller.router
