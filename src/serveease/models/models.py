from pydantic import BaseModel, Field , field_validator
from typing import List, Optional
from uuid import uuid4
import math

class Review(BaseModel):
    text: str
    date: Optional[str] = None
class ServiceProvider(BaseModel):
    provider_id : str
    name: str = Field(...,min_length=3, description="Name of the service provider")
    customer_reviews: List[Review] = []
    service_type: str = Field(...,min_length=3, description="Type of service provided")
    rating: Optional[float] = Field(
        default=None, ge=0, le=5, description="Rating given by the customer (0 to 5)"
    )

class RecommendedServiceProvider(BaseModel):
    provider: ServiceProvider
    score: int = Field(..., ge=1, le=10, description="Score of the service provider based on recommendations")
    reason : str = Field(
        default="", description="Reason for scoring the service provider"
    )
    

class RecommendationResponse(BaseModel):
    recommended_providers: List[RecommendedServiceProvider] = Field(
        default_factory=list, description="List of recommended service providers"
    )

class ServiceProviders(BaseModel):
    service_providers: List[ServiceProvider]