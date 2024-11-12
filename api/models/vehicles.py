from pydantic import BaseModel

class Vehicle(BaseModel):
    id: int
    brand: str
    model: str
    horsepower: int
    price: int

class VehicleRequest(BaseModel):
    brand: str
    model: str
    horsepower: int
    price: int