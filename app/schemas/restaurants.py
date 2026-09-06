from pydantic import BaseModel, Field, ConfigDict

class RestaurantBase(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    location: str = Field(min_length=1, max_length=50)
    cuisine: str = Field(min_length=1, max_length=50)
    contact_number: str = Field(min_length=10, max_length=15)


class RestaurantCreate(RestaurantBase):
    pass

class RestaurantResponse(RestaurantBase):
    id: int
    avg_rating: float
    model_config = ConfigDict(from_attributes=True)