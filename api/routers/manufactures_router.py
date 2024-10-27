from fastapi import APIRouter, Depends, HTTPException
from queries.manufactures_queries import ManufactureQueries, ManufactureDatabaseError
from models.manufactures import Manufacture



router = APIRouter(tags=['Manufacture'], prefix="/api/manufactures")


@router.get("/")
async def get_all_manufactures(
    queries: ManufactureQueries = Depends()
) -> list[Manufacture]:
    try:
        manufactures = queries.get_all_manufactures()
        return manufactures
    except ManufactureDatabaseError:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve manufactures."
        )