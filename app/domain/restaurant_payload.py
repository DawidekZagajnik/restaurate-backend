from pydantic import BaseModel, validator


class RestaurantPayload(BaseModel):
    name: str
    description: str
    address: str

    @validator("name")
    def validate_name(cls, value):
        if len(value) > 30:
            raise ValueError("Given restaurant name is too long.")
        return value

    @validator("address")
    def validate_address(cls, value):
        if len(value) > 50:
            raise ValueError("Given restaurant address is too long.")
        return value

    @validator("description")
    def validate_description(cls, value):
        if len(value) > 200:
            raise ValueError("Given restaurant description is too long.")
        return value
