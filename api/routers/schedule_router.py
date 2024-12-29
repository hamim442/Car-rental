from fastapi import APIRouter, Depends, HTTPException
from queries.schedule_queries import(ScheduleQueries, ScheduleCreationError,
ScheduleDatabaseError,
ScheduleDoesNotExist)
from models.schedule import Schedule, ScheduleRequest
from utils.authentication import try_get_jwt_user_data
from models.jwt import JWTUserData

router = APIRouter(tags=["Schedule"], prefix = "/api/schedules")


@router.post("/")
def create_schedule(
    Schedule: ScheduleRequest,
    user: JWTUserData = Depends(try_get_jwt_user_data),
    queries: ScheduleQueries = Depends()
) -> Schedule:
    try:
        new_schedule = queries.create_schedule(Schedule, user.id)
        return new_schedule
    except ScheduleCreationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ScheduleDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    