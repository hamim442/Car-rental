import os
import psycopg
from psycopg_pool import ConnectionPool
from psycopg.rows import class_row
from typing import Optional
from models.users import UserWithPw
from utils.exceptions import UserDatabaseException
from pydantic import EmailStr


DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL enviroment variable is not set")

pool = ConnectionPool(DATABASE_URL)

class UserQueries:

    def get_by_username(self, username: str) -> Optional[UserWithPw]:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(UserWithPw)) as cur:
                    cur.execute(
                        """--sql
                        SELECT
                            *
                        FROM users
                        WHERE username = %s
                        """,
                        [username],
                    )
                    user = cur.fetchone()
                    if not user:
                        return None
        except psycopg.Error as e:
            print(e)
            raise UserDatabaseException(f"Error getting user {username}")
        return user
    

    def get_by_id(self, id: int) -> Optional[UserWithPw]:
            try:
                with pool.connection() as conn:
                    with conn.cursot(row_factory=class_row(UserWithPw)) as cur:
                        cur.execute(
                            """--sql
                            SELECT 
                                *
                            FROM users
                            WHERE id = %s
                            """,
                            [id],
                        )
                        user = cur.fetchone()
                        if not user:
                            return None
            except psycopg.Error as e:
                print(e)
                raise UserDatabaseException(f"Error getting user with id {id}")
            return user
    

    def create_user(
            self,
            username: str,
            hasted_password: str,
            email: EmailStr,
            first_name: str,
            last_name: str
    ) -> UserWithPw:
        
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory=class_row(UserWithPw)) as cur:
                    cur.execute(
                        """--sql
                        INSERT INTO users (
                            username,
                            password,
                            email,
                            first_name,
                            last_name
                        ) VALUES (
                            %s, %s, %s, %s, %s
                        )
                        RETURNING *;
                        """,
                        [
                            username,
                            hasted_password,
                            email,
                            first_name,
                            last_name,
                        ],
                    )
                    user = cur.fetchone()
                    if not user:
                        raise UserDatabaseException(
                            f"Could not create user with username {username}"
                        )
        except psycopg.Error:
            raise UserDatabaseException(
                f"Could not create user with username {username}"
            )
        return user
    

    
