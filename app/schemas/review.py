from pydantic import BaseModel, ConfigDict, Field

class ReviewBase(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    body: str = Field(min_length=1, max_length=500)
    rating: int = Field(ge=1, le=5)

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    user_id: int         
    restaurant_id: int    
    sentiment_label: str 
    sentiment_score: float
    model_config = ConfigDict(from_attributes=True)