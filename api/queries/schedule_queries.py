import os
import psycopg
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from models.schedule import Schedule, ScheduleRequest
from utils.exceptions import (ScheduleCreationError, 
    ScheduleDatabaseError, ScheduleDoesNotExist, DatabaseURLException)

database_url = os.environ.get("DATABASE_URL")
if database_url is None:
    raise DatabaseURLException(
        "You forgot to define DATABASE_URL in your enviroment"
    )

pool = ConnectionPool(database_url)

class ScheduleQueries:
   
    def get_all_schedules(self, user_id: int) -> list[Schedule]:
        try:
             with pool.connection() as conn:
                 with conn.cursor(row_factory=class_row(schedule)) as cur:
                     result = cur.execute(
                        """--sql
                        SELECT *
                        FROM schedules
                        WHERE user_id = %s;
                        """,
                        (user_id,),
                     )
                     schedules = result.fetchall()
                     return schedules
        except psycopg.Error as e:
            print(f"Error retriving all schedules: {e}")
            raise ScheduleDatabaseError("Error retriving all schedules")
        
    def create_schedule(self, schedule: ScheduleRequest, user_id: int) -> Schedule:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(Schedule)) as cur:
                    result = cur.execute(
                        """--sql
                        INSERT INTO schedules (
                            vehicle_id,
                            start_date,
                            end_date,
                            user_id
                        )
                        VALUES (
                            %(vehicle_id)s,
                            %(start_date)s,
                            %(end_date)s,
                            %(user_id)s
                        )
                        RETURNING *;
                        """,
                        {
                            "vehicle_id": schedule.vehicle_id,
                            "start_date": schedule.start_date,
                            "end_date": schedule.end_date,
                            "user_id": user_id
                        }
                    )
                    new_schedule = result.fetchone()
                    if new_schedule is None:
                        raise ScheduleCreationError("Error creating vehicle.")
                    return new_schedule
        except psycopg.Error as e:
            print(f"Error creating schedule: {e}")
            raise ScheduleCreationError("Error creating schedule")
       
       
       