steps = [
    [
        # "Up" SQL Statement
        """--sql
        CREATE TABLE schedules (
            id SERIAL PRIMARY KEY NOT NULL,
            vehicle_id INTEGER NOT NULL REFERENCES vehicles (id),
            start_date TIMESTAMP NOT NULL,
            end_date TIMESTAMP NOT NULL,
            user_id INTEGER NOT NULL REFERENCES users (id)
        )
        """,
        # "Down" SQL statement
        """--sql
            DROP TABLE schedules;
        """,
    ],
]