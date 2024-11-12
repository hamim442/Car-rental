import os
import psycopg
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from psycopg.errors import UniqueViolation
from models.vehicles import Vehicle, VehicleRequest
from utils.exceptions import (
    VehicleDataBaseError, DatabaseURLException, VehicleCreationError
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
        
    def create_vehicle(self, vehicle: VehicleRequest, user_id: int) -> list[Vehicle]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Vehicle)) as cur:
                    result = cur.execute(
                        """--sql
                        INSERT INTO vehicles (
                            brand,
                            model,
                            horsepower,
                            price,
                            user_id
                        )
                        VALUES (
                            %(brand)s,
                            %(model)s,
                            %(horsepower)s,
                            %(price)s,
                            %(user_id)s
                        )
                        RETURNING *;
                        """,
                        {
                            "brand": vehicle.brand,
                            "model": vehicle.model,
                            "horsepower": vehicle.horsepower,
                            "price": vehicle.price,  # Fixed the typo here
                            "user_id": user_id       # Added user_id here
                        }
                    )
                    new_vehicle = result.fetchone()
                    if new_vehicle is None:
                        raise VehicleCreationError("Error creating vehicle.")
                    return new_vehicle
        except psycopg.Error as e:
            print(f"Error creating vehicle for user {user_id}: {e}.")
            raise VehicleDataBaseError("Error creating vehicle.")