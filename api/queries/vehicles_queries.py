import os
import psycopg
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from psycopg.errors import UniqueViolation
from models.vehicles import Vehicle, VehicleRequest
from utils.exceptions import (
    VehicleDataBaseError, DatabaseURLException, VehicleCreationError, VehicleDoesNotExist
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
                            "price": vehicle.price, 
                            "user_id": user_id      
                        }
                    )
                    new_vehicle = result.fetchone()
                    if new_vehicle is None:
                        raise VehicleCreationError("Error creating vehicle.")
                    return new_vehicle
        except psycopg.Error as e:
            print(f"Error creating vehicle for user {user_id}: {e}.")
            raise VehicleDataBaseError("Error creating vehicle.")
        
    def delete_vehicle(self, id: int, user_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """--sql
                        DELETE FROM vehicles
                        WHERE id = %s AND user_id = %s;
                        """,
                        (id, user_id),
                    )
                    return cur.rowcount > 0
        except psycopg.Error as e:
            print(f"Error deleting vehicles wiht id {id} from user {user_id}: {e}.")
            raise VehicleDataBaseError(
                f"Error deleteting trip with id {id} for user {user_id}."
            )
        
    def get_vehicle(self, id: int, user_id: int) -> Vehicle:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Vehicle)) as cur:
                    result = cur.execute(
                        """--sql
                        SELECT *
                        FROM vehicles
                        WHERE id = %s AND user_id = %s;
                        """,
                        (id, user_id),
                    )
                    vehicle = result.fetchone()
                    if vehicle is None:
                        raise VehicleDoesNotExist(
                            f"No vehicles with id {id} for user {user_id}"
                        )
                    return vehicle 
        except psycopg.Error as e:
            print(
                f"Error retriving trip with id {id} for user {user_id}: {e}"
            )
            raise VehicleDoesNotExist(
                f"Error retrieving vehicle with id {id} for user {user_id}"
            )
                
