from pydantic import BaseModel

from datetime import datetime


class AIInsightResponse(BaseModel):

    id: int

    dataset_id: int

    insight_type: str

    title: str

    description: str

    priority: str

    created_at: datetime

    class Config:

        from_attributes = True


class CustomerBehaviorResponse(BaseModel):

    customer: str

    total_spent: float

    purchase_count: int

    segment: str


class ProductRecommendationResponse(BaseModel):

    product: str

    total_quantity: int

    recommendation: str

    priority: str


class DemandSpikeResponse(BaseModel):

    product: str

    average_sales: float

    predicted_sales: float

    spike_detected: bool


class InventorySuggestionResponse(BaseModel):

    product: str

    recommended_stock: int