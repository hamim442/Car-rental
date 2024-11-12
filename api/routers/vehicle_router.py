from fastapi import APIRouter, Depends, HTTPException
from queries.vehicles_queries import VehicleQueries, VehicleDataBaseError, VehicleCreationError
from models.vehicles import Vehicle, VehicleRequest
from utils.authentication import try_get_jwt_user_data
from models.jwt import JWTUserData



router = APIRouter(tags=['Vehicle'], prefix="/api/vehicles")

@router.get("/")
def get_all_vehicles(
    queries: VehicleQueries= Depends()
) -> list[Vehicle]:
    try:
        vehicles = queries.get_all_vehicles()
        return vehicles
    except VehicleDataBaseError:
        raise HTTPException(
            status_code=500, detail="Failed to retrive vehicles"
        )
    
@router.post("/")
def create_vehicle(
    vehicle: VehicleRequest,
    user: JWTUserData = Depends(try_get_jwt_user_data),
    queries: VehicleQueries = Depends(),
) -> Vehicle:
    # Check if the user is logged in
    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated.")

    try:
        new_vehicle = queries.create_vehicle(vehicle, user.id)
        return new_vehicle
    except VehicleCreationError as e:
        raise HTTPException(status_code=400, detail=f"Vehicle creation error: {e}")
    except VehicleDataBaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
