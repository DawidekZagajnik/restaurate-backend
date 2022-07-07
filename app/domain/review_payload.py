from pydantic import BaseModel


class ReviewPayload(BaseModel):
    content: str
    rate: int
    restaurantId: int
