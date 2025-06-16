from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
import math



class AddressComponent(BaseModel):
    long_name: str
    short_name: str
    types: List[str]

class Location(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)

class PlusCode(BaseModel):
    global_code: Optional[str]
    compound_code: Optional[str]

class Address(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_input: str
    formatted_address: str
    address_components: List[AddressComponent]
    location: Location
    place_id: str
    plus_code: Optional[PlusCode]

class UserPreferences(BaseModel):
    service_type: str
    max_budget: float = Field(..., gt=0)
    max_distance: float = Field(..., gt=0)
    min_rating: float = Field(..., ge=1, le=5)

class User(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid4()))
    address: Address
    preferences: UserPreferences

class ServiceProvider(BaseModel):
    provider_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    service_type: str
    address: Address
    cost: float = Field(..., gt=0)
    rating: float = Field(..., ge=1, le=5)
    available: bool = True

class Recommendation(BaseModel):
    provider: ServiceProvider
    score: float
    explanation: str

class RecommendationResponse(BaseModel):
    recommendations: List[Recommendation] = Field(..., description="List of recommended service providers")
    total_providers_considered: int = Field(..., description="Total number of providers evaluated")
    filters_applied: List[str] = Field(..., description="List of filters applied (e.g., service_type, budget)")
    message: str = Field(..., description="Summary message for the response")    