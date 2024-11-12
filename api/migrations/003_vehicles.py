steps = [
    [
        # "Up" SQL statement
        """--sql
            CREATE TABLE vehicles (
                id SERIAL PRIMARY KEY NOT NULL,
                brand VARCHAR(100) NOT NULL,
                model VARCHAR(100) NOT NULL,
                horsepower INTEGER NOT NULL,
                price INTEGER NOT NULL,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
            );
        """,
        # "Down" SQL statement
        """--sql
            DROP TABLE vehicles;
        """,
    ],
]
