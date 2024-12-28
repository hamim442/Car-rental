from pydantic import BaseModel
from datetime import datetime

class schedule(BaseModel):
    id: int
    vehicles_id: int 
    start_date: datetime
    end_date: datetime
    user_id: int

class ScheduleRequest(BaseModel):
    vehicles_id: int
    start_date: datetime
    end_date: datetime