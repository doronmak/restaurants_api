from pydantic import BaseModel


class Restaurant(BaseModel):
    name: str
    type: str
    phone: str
    location: list
