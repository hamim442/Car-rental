from pydantic import BaseModel
from datetime import date

class Schedule(BaseModel):
    id: int
    vehicle_id: int 
    start_date: date
    end_date: date
    user_id: int

class ScheduleRequest(BaseModel):
    vehicle_id: int
    start_date: date
    end_date: date