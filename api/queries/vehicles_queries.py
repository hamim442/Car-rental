import os
import psycopg
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from psycopg.errors import UniqueViolation
from models.vehicles import Vehicle
from utils.exceptions import (
    VehicleDataBaseError, DatabaseURLException
)


database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your enviroment"
    )

pool = ConnectionPool(database_url)

class VehicleQueries:

    def get_all_vehicles(self) -> list[Vehicle]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Vehicle)) as cur:
                    result = cur.execute(
                        """--sql
                        SELECT * FROM vehicles;
                        """
                    )
                    vehicles = result.fetchall()
                    return vehicles
        except psycopg.Error as e:
            print(f"Error retriving all vehicles: {e}")
            raise VehicleDataBaseError("Error retriving all vehicles")