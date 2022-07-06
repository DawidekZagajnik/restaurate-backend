from pydantic import BaseModel


class RestaurantPayload(BaseModel):
    name: str
    description: str
    ownerId: int
