import os
import psycopg
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from psycopg.errors import UniqueViolation
from models.manufactures import Manufacture
from utils.exceptions import (
    ManufactureDatabaseError,
    DatabaseURLException,
)


database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your enviroment"
    )

pool = ConnectionPool(database_url)

class ManufactureQueries:

    def get_all_manufactures(self) -> list[Manufacture]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Manufacture)) as cur:
                    result = cur.execute(
                        """--sql
                        SELECT * FROM manufactures;
                        """
                    )
                    manufactures = result.fetchall()
                    return manufactures
        except psycopg.Error as e:
            print(f"Error retrieving all manufactures: {e}")
            raise ManufactureDatabaseError("Error retrieving all manufactures")
