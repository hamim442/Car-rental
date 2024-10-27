from pydantic import BaseModel

class Manufacture(BaseModel):
    id: int
    name: str
    logo_picture_url: str